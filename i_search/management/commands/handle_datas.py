import base64
import json
import logging
import operator
import re
import string
import sys
import time
from datetime import datetime
from functools import reduce

import requests
from Crypto.Cipher import AES
from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import transaction
from django.db.models import Q
from django.utils import timezone

from arsenal.models import BuildingOwner, LandOwner
from common.util import aes_decrypt, aes_encrypt, get_all_code, pdata_handle, excel_file_write_sheets
from diablo.models import BkeyRegnoList, LkeyRegnoList
from i_search.lbor_parser import get_target_amount_one_str
from i_search.models import (Abiu, Babaco, Citron, Damson, DamsonQuery,
                             info_config)

logger = logging.getLogger(__name__)

batch_size = 5000

class Command(BaseCommand):
    """
    This command will print a command line argument.
    """
    help = 'This command will assign infos processed from inputs to BusinessDealers.'
    
    def add_arguments(self, parser):

        parser.add_argument(
            '-t',
            '--task_type',
            action='store',
            dest='task_type',
            default=None,
            help=''' input data'''
        )

        parser.add_argument(
            '-c',
            '--control',
            action='store',
            dest='control',
            default=False,
            help=''' input update_time'''
        )

    def handle(self, *args, **options):
        if options['task_type'] == 'DU':
            start1 = time.perf_counter()
            try:
                control = options['control']
                case_category_type = {'動產抵押': 1, '附條件買賣': 2, '信託占有': 3}
                case_status_type = {'效期內': 1, '已過效期未註銷': 2}
                target_dict_type = {'': -1, '1、汽車、大型重型機器腳踏車及拖車': 1, '1、總噸位未滿二十噸之動力漁船或未滿五十噸之非動力漁船': 2, '1、漁船以外之小船': 3, '1、機器設備或工具':4}
                save_info = info_config.objects.get(mode_str='damson')
                last_time = timezone.localtime(save_info.last_time).strftime("%Y-%m-%d %H:%M:%S")
                now_time = timezone.now()
                if control:
                    datas = Damson.objects.filter(Q(d6__gt=last_time) | Q(d7__gt=last_time)).exclude(d5=0)
                else:
                    datas = Damson.objects.all()
                create_list = []
                for s, i in enumerate(datas):
                    for data in i.d3:
                        case_category = case_category_type[data['案件類別']] if data['案件類別'] and data['案件類別'] in case_category_type else 0
                        case_status = case_status_type[data['案件狀態']] if data['案件狀態'] and data['案件狀態'] in case_status_type else 0
                        try:
                            target_type = target_dict_type[data['動產擔保交易資料']['標的物種類']] if data['動產擔保交易資料']['標的物種類'] in target_dict_type else 0
                        except:
                            target_type = 0
                        property_type, _ = get_target_amount_one_str(data['抵押權人名稱'])
                        try:
                            guarantee_amount = int(data['動產擔保交易資料']['擔保債權金額'].replace(',', '').replace(' ', '').replace('(新台幣)', ''))
                        except:
                            guarantee_amount = None
                        contract_start_year = str(int(data['動產擔保交易資料']['契約啟始日期'].split('/')[0]) + 1911) if data['動產擔保交易資料']['契約啟始日期'] else None
                        contract_start =  contract_start_year + '-' + '-'.join(data['動產擔保交易資料']['契約啟始日期'].split('/')[1:]) if contract_start_year else None
                        contract_end_year = str(int(data['動產擔保交易資料']['契約終止日期'].split('/')[0]) + 1911) if data['動產擔保交易資料']['契約終止日期'] else None
                        contract_end = contract_end_year + '-' + '-'.join(data['動產擔保交易資料']['契約終止日期'].split('/')[1:]) if contract_end_year else None
                        try:
                            property_detail = int(data['動產擔保交易資料']['動產明細項數']) if data['動產擔保交易資料']['動產明細項數'] else 0
                        except:
                            property_detail = None
                        is_maximum = False if data['動產擔保交易資料']['是否最高限額'] == '否' else True
                        is_floating = False if data['動產擔保交易資料']['是否為浮動擔保'] == '否' else True
                        kwargs = {
                                'damson': i,
                                'registration_authority': data['登記機關'],
                                'case_category': case_category,
                                'case_status': case_status,
                                'registration_number': data['登記編號'],
                                'mortgagee_name': data['抵押權人名稱'],
                                'mortgagee_agent_name': data['抵押權人資料']['代理人名稱'],
                                'property_type': property_type,
                                'guarantee_amount': guarantee_amount,
                                'contract_start': contract_start,
                                'contract_end': contract_end,
                                'property_detail': property_detail,
                                'is_maximum': is_maximum,
                                'is_floating': is_floating,
                                'target_type': target_type
                                }
                        create = DamsonQuery(**kwargs)
                        create_list.append(create)
                    if ((s+1) % 5000) == 0 or (s+1) == len(datas):
                        with transaction.atomic():
                            if create_list:
                                DamsonQuery.objects.bulk_create(create_list, ignore_conflicts=True)
                            create_list = []
                save_info.last_time = now_time
                save_info.save()
                end1 = time.perf_counter()
                logger.info(f'單身資料更新完成，總執行時間：{end1 - start1}秒')
            except Exception as e:
                end1 = time.perf_counter()
                logger.info(f'單身資料失敗，總執行時間：{end1 - start1}，{str(e)} exception in line {sys.exc_info()[2].tb_lineno}')

        if options['task_type'] == 'FP':
            start1 = time.perf_counter()
            try:
                update_count = 0
                datas = 'strat'
                count = 0
                while datas:
                    update_count += 1
                    #! 已跑過略過
                    if update_count < 100:
                        continue
                    if update_count == 1:
                        datas = Babaco.objects.filter(b7=1)[:batch_size]
                    else:
                        datas = Babaco.objects.filter(b7=1)[batch_size * (update_count - 1):batch_size * update_count]
                    # logger.info(f'總資料長度{len(datas)}')
                    count += len(datas)
                    update_list = []
                    create_list = []
                    time_now = timezone.now()
                    for i in datas:
                        check_update = False
                        #! 更新pdata
                        pdata = aes_decrypt(i.b5)
                        if pdata[:2] != '09' or len(pdata) != 10:
                            # logger.info(f'正規化前：{pdata}')
                            i.b7 = 0
                            i.b9 = time_now
                            check_update = True
                            pdata_list = pdata_handle(pdata)
                            if pdata_list:
                                # logger.info(f'正規化後：{pdata_list}')
                                for data_1 in pdata_list:
                                    b1 = i.b1
                                    b2 = data_1[:4] + '******'
                                    b4 = i.b4
                                    b5 = aes_encrypt(data_1)
                                    kwargs = {
                                            'b1': b1,
                                            'b2': b2,
                                            'b4': b4,
                                            'b5': b5
                                            }
                                    create = Babaco(**kwargs)
                                    create_list.append(create)
                        #! 更新udata
                        try:
                            if i.b1[0] in list(string.ascii_lowercase):
                                b4 = aes_encrypt(aes_decrypt(i.b4).upper())
                                i.b9 = time_now
                                try:
                                    Babaco.objects.get(b4=b4, b5=i.b5)
                                    i.b7 = 0
                                except:
                                    i.b1 = i.b1.upper()
                                    i.b4 = b4
                                check_update = True
                        except:
                            pass
                        if check_update:
                            update_list.append(i)
                    with transaction.atomic():
                        if create_list:
                            logger.info(f'新增筆數：{len(create_list)}')
                            Babaco.objects.bulk_create(create_list, ignore_conflicts=True)
                        if update_list:
                            logger.info(f'更新筆數：{len(update_list)}')
                            Babaco.objects.bulk_update(update_list, fields=['b1', 'b4', 'b7', 'b9'])
                    logger.info(f'已跑資料數：{count}')
                end1 = time.perf_counter()
                logger.info(f'資料更新完成，總執行時間：{end1 - start1}秒')
            except Exception as e:
                print(i.id, aes_decrypt(i.b4))
                end1 = time.perf_counter()
                logger.info(f'資料更新失敗，總執行時間：{end1 - start1}，{str(e)} exception in line {sys.exc_info()[2].tb_lineno}')

        if options['task_type'] == 'SE':
            start1 = time.perf_counter()
            try:
                control_dict = {-1: '無', 0: '不詳', 1: '政府機構', 2: '自然人', 3: '公司', 4: '租賃業者', 5: '金融機構'}
                control = options['control']
                control = int(control)
                sql = f'''SELECT a.id, a.registration_number, b.d4, c.b5, d.a10
                        FROM telem.i_search_damsonquery a
                        left join telem.i_search_damson b on a.damson_id=b.id
                        left join telem.i_search_babaco c on b.d2=c.b4
                        left join telem.i_search_abiu d on b.d2=d.a8
                        where a.property_type={control}'''
                datas = DamsonQuery.objects.raw(sql)
                if datas:
                    data = {}
                    filename = f'動保_{control_dict[control]}_{datetime.strftime((datetime.now()), "%Y-%m-%d")}'
                    data_list = []
                    data_dict = {}
                    for i in datas:
                        name = ''
                        uid = ''
                        address = ''
                        mortgagee_name = ''
                        car_no = ''
                        guarantee_amount = ''
                        phone = ''
                        bday = ''
                        registration_number = i.registration_number
                        damson_data = json.loads(aes_decrypt(i.d4))
                        for d_data in damson_data:
                            if d_data['certificateAppNoWord'] == registration_number:
                                name = d_data['債務人資料']['名稱']
                                uid = d_data['債務人資料']['統編']
                                address = d_data['動產擔保交易資料']['標的物所在地'].split('-')[1].replace(' ', '') if '-' in d_data['動產擔保交易資料']['標的物所在地'] else  d_data['動產擔保交易資料']['標的物所在地'].replace(' ', '')
                                mortgagee_name = d_data['抵押權人資料']['名稱']
                                car_no = d_data['車牌']
                                try:
                                    guarantee_amount = int(d_data['動產擔保交易資料']['擔保債權金額'].replace(',', '').replace(' ', '').replace('(新台幣)', ''))
                                except:
                                    pass
                                break
                        phone = aes_decrypt(i.b5) if i.b5 else ''
                        bdata = aes_decrypt(i.a10) if i.a10 else ''
                        bday = '/'.join([str(int(bdata[:3])), bdata[3:5], bdata[5:]]) if bdata else ''
                        if uid in data_dict:
                            data_dict[uid]['行動電話'] += f'，{phone}'
                        else:
                            data_dict[uid] = {
                                            '姓名': name,
                                            '身份證、生日、戶籍地': f'{uid}、{bday}、{address}',
                                            '行動電話': phone,
                                            '車牌': car_no,
                                            '抵押權人': mortgagee_name,
                                            '擔保債權金額': guarantee_amount,
                                            }
                    if data_dict:
                        for k, v in data_dict.items():
                            data_list.append(v)
                        data[filename] = {
                            'headers': [['姓名', '身份證、生日、戶籍地', '行動電話', '車牌', '抵押權人', '擔保債權金額']],
                            'rows': data_list,
                            }
                        msg = excel_file_write_sheets(filename + '.xlsx', data)
                end1 = time.perf_counter()
                logger.info(f'資料匯出完成，總執行時間：{end1 - start1}秒')
            except Exception as e:
                end1 = time.perf_counter()
                logger.info(f'資料匯出失敗，總執行時間：{end1 - start1}，{str(e)} exception in line {sys.exc_info()[2].tb_lineno}')