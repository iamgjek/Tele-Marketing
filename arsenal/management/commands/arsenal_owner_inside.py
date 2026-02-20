import base64
import logging
import operator
import sys
import time
import json
from functools import reduce

from Crypto.Cipher import AES
from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import transaction
from django.db.models import Q

from arsenal.models import BuildingOwner, LandOwner
from i_search.models import Abiu, info_config, Citron
from diablo.models import LkeyRegnoList, BkeyRegnoList
from datetime import datetime

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
            '-LB',
            '--lbtype',
            action='store',
            dest='lbtype',
            default='L',
            help=''' input lbtype'''
        )

    def profile_handle(self, c_uid):
        city_list = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L' ,'M', 'N', 'O', 'P', 'Q','R','S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
        uid_tag_89 = ['0', '1', '2', '3', '4', '5', '6']
        uid_tag_12 = uid_tag_89[:-1]
        uid_tag_dict = {'6': 3, '7': 4, '8': 5, '9': 6}
        gender_man = ['A', 'C', '1', '8']
        gender_woman = ['B', 'D', '2', '9']
        uid_tag = 0
        gender = 0
        error = False
        #* 國籍判斷
        if c_uid and c_uid[0] in city_list:
            #*性別判斷
            gender = 1 if c_uid[1] in gender_man else 2 if c_uid[1] in gender_woman else 0
            if c_uid[1] in city_list:
                uid_tag = 2
            elif c_uid[1] in ['8', '9']:
                uid_tag = 2 if c_uid[2] in uid_tag_89 else uid_tag_dict[c_uid[2]] if c_uid[2] in uid_tag_dict else 0
            elif c_uid[1] in ['1', '2']:
                uid_tag = 1 if c_uid[2] in uid_tag_12 else uid_tag_dict[c_uid[2]] if c_uid[2] in uid_tag_dict else 0
        #* 第一碼為數字 -> 外國人
        elif c_uid and c_uid[0] in ['0','1','2','3','4','5','6','7','8','9']:
            uid_tag = 2
        else:
            error = True
        return uid_tag, gender, error

    def aes_encrypt(self, text):
        try:
            length = 16
            count = len(text)
            add = length - (count % length) if (count % length != 0) else 0
            text += '\0'.encode() * add
            cipher_text = self.cryptor.encrypt(text)
            encodestrs = base64.b64encode(cipher_text)
            enctext = encodestrs.decode('utf8')
        except:
            enctext = None
        return enctext

    def aes_decrypt(self, text):
        try:
            text = base64.b64decode(text)
            plain_text = self.cryptor.decrypt(text).decode()
        except:
            plain_text = None
        return plain_text

    def handle(self, *args, **options):
        start1 = time.perf_counter()
        try:
            #! 金鑰
            key = settings.THUNDERBOLT_KEY
            key = key.encode('utf8')
            self.cryptor = AES.new(key, AES.MODE_ECB)
            lbtype = options['lbtype']
            if lbtype == 'L':
                lb_id = info_config.objects.get(mode_str='104_landowner')
                Owner = LandOwner
                tr_model = 'transcript_landtranscript'
                index_model = 'transcript_landtranscriptindex'
            elif lbtype == 'B':
                lb_id = info_config.objects.get(mode_str='104_buildingowner')
                Owner = BuildingOwner
                tr_model = 'transcript_buildingtranscript'
                index_model = 'transcript_buildingtranscriptindex'
            lb_last_id = lb_id.last_id
            owner_datas = 'start'
            while owner_datas:
                start2 = time.perf_counter()
                owner_datas = Owner.objects.filter(id__gt=lb_last_id, o_uid__isnull=False).exclude(o_uid='').order_by('id')[:batch_size]
                if lbtype == 'L':
                    logger.info(f'土地總筆數：{len(owner_datas)}')
                elif lbtype == 'B':
                    logger.info(f'建物總筆數：{len(owner_datas)}')

                #! 判斷登序有無效
                lbkey_list = []
                for i in owner_datas:
                    #! 過濾
                    if not i.o_name or not i.bday:
                        continue
                    lbkey = i.lbkey
                    if not lbkey in lbkey_list:
                        lbkey_list.append(lbkey)
                lkey_str = "'" + "','".join(lbkey_list) + "'"
                sql = f'''SELECT a.id, a.lbkey, b.owners
                        FROM arsenal.{index_model} a
                        left join arsenal.{tr_model} b on b.id=a.transcript_id
                        where a.lbkey in ({lkey_str}) '''
                lbkey_trs = Owner.objects.raw(sql)
                lbkey_owner_dict = {}
                for i in lbkey_trs:
                    owner_data = json.loads(i.owners) if i.owners else None
                    if owner_data:
                        lbkey = i.lbkey
                        owner_data = [t for t in owner_data['regno_list']] if 'regno_list' in owner_data else None
                        if owner_data:
                            lbkey_owner_dict[lbkey] = owner_data

                #! 前置資料處理
                check_udata_list = []
                check_lbkey = []
                check_reg_date = {}
                check_query_time = {}
                check_lbkey_query_time = {}
                udata_dict = {}
                lbkey_regno_dict = {}
                q_list = []
                for i in owner_datas:
                    #! 過濾
                    if not i.o_name or not i.bday:
                        continue
                    lbkey = i.lbkey
                    regno = i.regno
                    is_valid = i.is_valid if not lbkey in lbkey_owner_dict else 1 if regno in lbkey_owner_dict[lbkey] else 0
                    id = i.id
                    uid = i.uid
                    c_uid = i.o_uid.replace('\u3000', '').encode()
                    error = False
                    uid_tag, gender, error = self.profile_handle(uid)
                    if error:
                        logger.info(f'uid無法解析：{uid}，lbkey：{lbkey}，regno：{regno}')
                        continue
                    name = i.name
                    c_name = i.o_name.replace('\u3000', '').encode()
                    c_bday = i.bday_str[1:].replace('\u3000', '').encode()
                    bday = i.bday_str[1:4] + '****'
                    udata = self.aes_encrypt(c_uid)
                    reg_date = i.reg_date if i.reg_date else datetime.strptime('1912-01-01', '%Y-%m-%d').date()
                    query_time = i.query_time

                    #* Profile
                    kwargs = {
                            'a1': uid,
                            'a2': name,
                            'a3': i.address,
                            'a5': self.aes_encrypt(bday.replace('\u3000', '').encode()),
                            'a6': uid_tag,
                            'a7': gender,
                            'a8': udata,
                            'a9': self.aes_encrypt(c_name),
                            'a10': self.aes_encrypt(c_bday),
                            'a11': reg_date,
                            'a13': query_time,
                            }

                    #* LBkeyData
                    kwargs_regno = {
                                    'c1': uid,
                                    'c2': udata,
                                    'c3': lbtype,
                                    'c4': lbkey,
                                    'c5': regno,
                                    'c6': is_valid,
                                    'c8': query_time
                                    }

                    #* Profile
                    if not udata in check_udata_list:
                        check_udata_list.append(udata)
                        check_reg_date[udata] = reg_date
                        check_query_time[udata] = query_time
                        udata_dict[udata] = kwargs
                    else:
                        if reg_date > udata_dict[udata]['a11']:
                            udata_dict[udata]['a11'] = reg_date
                        elif query_time > udata_dict[udata]['a13']:
                            udata_dict[udata]['a13'] = query_time

                    #* LBkeyData
                    lbkey_regno = lbkey + ':' + regno
                    if not lbkey_regno in check_lbkey:
                        check_lbkey.append(lbkey_regno)
                        q_list.append(reduce(operator.and_, [Q(c4=lbkey), Q(c5=regno)]))
                        check_lbkey_query_time[lbkey_regno] = query_time
                        lbkey_regno_dict[lbkey_regno] = kwargs_regno
                    elif query_time > lbkey_regno_dict[lbkey_regno]['c8']:
                        lbkey_regno_dict[lbkey_regno]['c1'] = uid
                        lbkey_regno_dict[lbkey_regno]['c2'] = udata
                        lbkey_regno_dict[lbkey_regno]['c6'] = is_valid
                        lbkey_regno_dict[lbkey_regno]['c8'] = query_time

                #! 紀錄已跑完的id
                lb_id.last_id = id
                lb_last_id = id

                #! 已存在資料更新
                #* Profile
                have_udata_list = []
                update_list = []
                update_datas = Abiu.objects.filter(a8__in=check_udata_list)
                for update in update_datas:
                    udata = update.a8
                    have_udata_list.append(udata)
                    if udata_dict[udata]['a11'] > update.a11 or not update.a13 or udata_dict[udata]['a13'] > update.a13:
                        update.a2 = udata_dict[udata]['a2']
                        update.a3 = udata_dict[udata]['a3']
                        update.a6 = udata_dict[udata]['a6']
                        update.a7 = udata_dict[udata]['a7']
                        update.a9 = udata_dict[udata]['a9']
                        update.a10 = udata_dict[udata]['a10']
                        update.a11 = udata_dict[udata]['a11']
                        update.a13 = udata_dict[udata]['a13']
                        update_list.append(update)

                #* LBkeyData
                have_lbkey_list = []
                lbkey_update_list = []
                if not q_list:
                    continue
                update_datas = Citron.objects.filter(reduce(operator.or_, q_list))
                for update in update_datas:
                    lbkey = update.c4
                    regno = update.c5
                    lbkey_regno = lbkey + ':' + regno
                    have_lbkey_list.append(lbkey)
                    if lbkey_regno_dict[lbkey_regno]['c8'] > update.c8:
                        update.c1 = lbkey_regno_dict[lbkey_regno]['c1']
                        update.c2 = lbkey_regno_dict[lbkey_regno]['c2']
                        update.c6 = lbkey_regno_dict[lbkey_regno]['c6']
                        update.c8 = lbkey_regno_dict[lbkey_regno]['c8']
                        lbkey_update_list.append(update)

                #! 建立新資料
                #* Profile
                last_udata_list = list(set(check_udata_list) - set(have_udata_list))
                create_list = []
                for udata in last_udata_list:
                    kwargs = udata_dict[udata]
                    land_create = Abiu(**kwargs)
                    create_list.append(land_create)

                #* LBkeyData
                last_lbkey_udata = list(set(check_lbkey) - set(have_lbkey_list))
                lbkey_create_list = []
                for lbkey_regno in last_lbkey_udata:
                    kwargs = lbkey_regno_dict[lbkey_regno]
                    land_create = Citron(**kwargs)
                    lbkey_create_list.append(land_create)

                with transaction.atomic():
                    lb_id.save()
                    if create_list:
                        logger.info(f'Profile新建筆數：{len(create_list)}')
                        Abiu.objects.bulk_create(create_list, ignore_conflicts=True)
                    if update_list:
                        logger.info(f'Profile更新筆數：{len(update_list)}')
                        Abiu.objects.bulk_update(update_list, fields=['a2', 'a3', 'a6', 'a7', 'a9', 'a10', 'a11', 'a13'])
                    if lbkey_create_list:
                        logger.info(f'LBkeyData新建筆數：{len(lbkey_create_list)}')
                        Citron.objects.bulk_create(lbkey_create_list, ignore_conflicts=True)
                    if lbkey_update_list:
                        logger.info(f'LBkeyData更新筆數：{len(lbkey_update_list)}')
                        Citron.objects.bulk_update(lbkey_update_list, fields=['c1', 'c2', 'c6', 'c8'])
                    end2 = time.perf_counter()
                    logger.info(f'此批次時間：{end2 - start2}秒')
                    logger.info('')

            end1 = time.perf_counter()
            logger.info(f'所有權資料匯入完成，總執行時間：{end1 - start1}秒')
            # print('所有權資料匯入完成，總執行時間：', end1 - start1)
            # logger.info('案源更新匯入完成，總執行時間：{}'.format(end1 - start1))
        except Exception as e:
            # print(lbkey)
            # print(regno)
            # print(e, 'exception in line', sys.exc_info()[2].tb_lineno)
            end1 = time.perf_counter()
            # print('所有權資料匯入失敗，總執行時間：', end1 - start1)
            logger.info(f'案源匯入失敗，總執行時間：{end1 - start1}，{str(e)} exception in line {sys.exc_info()[2].tb_lineno}，lbkey：{lbkey}，regno：{regno}')