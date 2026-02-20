import base64
import json
import logging
import operator
import re
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
from common.util import aes_decrypt, get_all_code
from diablo.models import BkeyRegnoList, LkeyRegnoList
from i_search.models import Abiu, Citron, info_config

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
        #* 國籍判斷
        if c_uid[0] in city_list:
            #*性別判斷
            gender = 1 if c_uid[1] in gender_man else 2 if c_uid[1] in gender_woman else 0
            if c_uid[1] in city_list:
                uid_tag = 2
            elif c_uid[1] in ['8', '9']:
                uid_tag = 2 if c_uid[2] in uid_tag_89 else uid_tag_dict[c_uid[2]] if c_uid[2] in uid_tag_dict else 0
            elif c_uid[1] in ['1', '2']:
                uid_tag = 1 if c_uid[2] in uid_tag_12 else uid_tag_dict[c_uid[2]] if c_uid[2] in uid_tag_dict else 0
        #* 第一碼為數字 -> 外國人
        elif c_uid[0] in ['0','1','2','3','4','5','6','7','8','9']:
            uid_tag = 2
        return uid_tag, gender

    def handle(self, *args, **options):
        if options['task_type'] == 'OH':
            start1 = time.perf_counter()
            try:
                lbtype = options['lbtype']
                all_code = get_all_code(0)
                date_now = datetime.strftime((datetime.now()), "%Y-%m-%d")
                owner_datas = 'start'
                while owner_datas:
                    start2 = time.perf_counter()
                    lbkey_dict = {}
                    django_query = []
                    owner_datas = Citron.objects.filter(c13__isnull=True, c3=lbtype)[:batch_size]
                    #* 拉資料前置
                    for i in owner_datas:
                        lbkey = i.c4
                        regno = i.c5
                        django_query.append(reduce(operator.and_,[Q(lbkey=lbkey), Q(regno=regno)]))
                    #* 拉資料
                    if django_query:
                        if lbtype == 'L':
                            datas = LkeyRegnoList.objects.filter(reduce(operator.or_, django_query))
                        elif lbtype == 'B':
                            datas = BkeyRegnoList.objects.filter(reduce(operator.or_, django_query))
                        for i in datas:
                            lbkey = i.lbkey
                            regno = i.regno
                            city_code = lbkey[0]
                            area_code = lbkey[2:4]
                            lbkey_regno = ';'.join([lbkey, regno])
                            lbkey_dict[lbkey_regno] = {
                                                    'c9': i.right_type,
                                                    'c10': i.case_type,
                                                    'c11': all_code[city_code]['city_name'],
                                                    'c12': all_code[city_code][area_code]['area_name'],
                                                    'c14': timezone.localtime(i.creditors_last_setting_time).strftime("%Y-%m-%d") if i.creditors_last_setting_time else None
                                                    }
                    #* 處理更新
                    update_list = []
                    if lbkey_dict:
                        for i in owner_datas:
                            lbkey = i.c4
                            regno = i.c5
                            lbkey_regno = ';'.join([lbkey, regno])
                            data = lbkey_dict[lbkey_regno] if lbkey_regno in lbkey_dict else {}
                            if data:
                                i.c9 = data['c9']
                                i.c10 = data['c10']
                                i.c11 = data['c11']
                                i.c12 = data['c12']
                                if data['c14']:
                                    i.c14 = data['c14']
                            i.c13 = date_now
                            update_list.append(i)

                    with transaction.atomic():
                        if update_list:
                            logger.info(f'更新筆數：{len(update_list)}')
                            Citron.objects.bulk_update(update_list, fields=['c9', 'c10', 'c11', 'c12', 'c13', 'c14'])
                        end2 = time.perf_counter()
                        logger.info(f'此批次時間：{end2 - start2}秒')
                        logger.info('')
                    # break

                end1 = time.perf_counter()
                logger.info(f'登序資料更新完成，總執行時間：{end1 - start1}秒')
            except Exception as e:
                end1 = time.perf_counter()
                logger.info(f'登序資料失敗，總執行時間：{end1 - start1}，{str(e)} exception in line {sys.exc_info()[2].tb_lineno}')

        if options['task_type'] == 'UP':
            start1 = time.perf_counter()
            try:
                #! 金鑰
                key = settings.THUNDERBOLT_KEY
                key = key.encode('utf8')
                date_now = datetime.strftime((datetime.now()), "%Y-%m-%d")
                # carName_re = re.compile(r'^[\d+-]*(\D*?[縣市])*(\D*[鄉鎮市區])*\S+[　+|\s+]*$')
                carName_re = re.compile(r'^[\d+-]*(\D{2}?[縣市])(\D{1,3}[鄉鎮市區])*\S+[　+|\s+]*$')
                old_city_dict = {
                    '臺北縣': '新北市', '桃園縣': '桃園市', 
                    '臺中縣': '臺中市', '臺南縣': '臺南市', 
                    '高雄縣': '高雄市', '臺北鯀': '新北市'
                    }
                old_area_dict = {
                    '板橋市': '板橋區', '中和市': '中和區', '永和市': '永和區', 
                    '土城市': '土城區', '三峽鎮': '三峽區', '鶯歌鎮': '鶯歌區', 
                    '樹林市': '樹林區', '三重市': '三重區', '蘆洲市': '蘆洲區', 
                    '新莊市': '新莊區', '五股鄉': '五股區', '泰山鄉': '泰山區', 
                    '林口鄉': '林口區', '八里鄉': '八里區', '淡水鎮': '淡水區', 
                    '三芝鄉': '三芝區', '石門鄉': '石門區', '金山鄉': '金山區', 
                    '萬里鄉': '萬里區', '汐止市': '汐止區', '瑞芳鎮': '瑞芳區', 
                    '貢寮鄉': '貢寮區', '平溪鄉': '平溪區', '雙溪鄉': '雙溪區', 
                    '新店市': '新店區', '深坑鄉': '深坑區', '石碇鄉': '石碇區', 
                    '坪林鄉': '坪林區', '烏來鄉': '烏來區', '桃園市': '桃園區', 
                    '中壢市': '中壢區', '八德市': '八德區', '平鎮市': '平鎮區', 
                    '楊梅市': '楊梅區', '蘆竹市': '蘆竹區', '大溪鎮': '大溪區', 
                    '龍潭鄉': '龍潭區', '龜山鄉': '龜山區', '大園鄉': '大園區', 
                    '觀音鄉': '觀音區', '新屋鄉': '新屋區', '復興鄉': '復興區', 
                    '太平市': '太平區', '大里市': '大里區', '霧峰鄉': '霧峰區', 
                    '烏日鄉': '烏日區', '豐原市': '豐原區', '后里鄉': '后里區', 
                    '石岡鄉': '石岡區', '東勢鎮': '東勢區', '和平鄉': '和平區', 
                    '新社鄉': '新社區', '潭子鄉': '潭子區', '大雅鄉': '大雅區', 
                    '神岡鄉': '神岡區', '大肚鄉': '大肚區', '沙鹿鎮': '沙鹿區', 
                    '龍井鄉': '龍井區', '梧棲鎮': '梧棲區', '清水鎮': '清水區', 
                    '大甲鎮': '大甲區', '外埔鄉': '外埔區', '大安鄉': '大安區', 
                    '永康市': '永康區', '歸仁鄉': '歸仁區', '新化鎮': '新化區', 
                    '左鎮鄉': '左鎮區', '玉井鄉': '玉井區', '楠西鄉': '楠西區', 
                    '南化鄉': '南化區', '仁德鄉': '仁德區', '關廟鄉': '關廟區', 
                    '龍崎鄉': '龍崎區', '官田鄉': '官田區', '麻豆鎮': '麻豆區', 
                    '佳里鎮': '佳里區', '西港鄉': '西港區', '七股鄉': '七股區', 
                    '將軍鄉': '將軍區', '學甲鎮': '學甲區', '北門鄉': '北門區', 
                    '新營市': '新營區', '後壁鄉': '後壁區', '白河鎮': '白河區', 
                    '東山鄉': '東山區', '六甲鄉': '六甲區', '下營鄉': '下營區', 
                    '柳營鄉': '柳營區', '鹽水鎮': '鹽水區', '善化鎮': '善化區', 
                    '大內鄉': '大內區', '山上鄉': '山上區', '新市鄉': '新市區', 
                    '安定鄉': '安定區', '鳳山市': '鳳山區', '岡山鎮': '岡山區', 
                    '旗山鎮': '旗山區', '美濃鎮': '美濃區', '大寮鄉': '大寮區', 
                    '林園鄉': '林園區', '仁武鄉': '仁武區', '路竹鄉': '路竹區', 
                    '大樹鄉': '大樹區', '鳥松鄉': '鳥松區', '梓官鄉': '梓官區', 
                    '燕巢鄉': '燕巢區', '阿蓮鄉': '阿蓮區', '湖內鄉': '湖內區', 
                    '彌陀鄉': '彌陀區', '內門鄉': '內門區', '六龜鄉': '六龜區', 
                    '杉林鄉': '杉林區', '田寮鄉': '田寮區', '甲仙鄉': '甲仙區', 
                    '橋頭鄉': '橋頭區', '茄萣鄉': '茄萣區', '永安鄉': '永安區', 
                    '大社鄉': '大社區', '桃源鄉': '桃源區', '茂林鄉': '茂林區', 
                    '那瑪夏鄉': '那瑪夏區'
                    }
                user_datas = 'start'
                while user_datas:
                    start2 = time.perf_counter()
                    lbkey_dict = {}
                    django_query = []
                    user_datas = Abiu.objects.filter(a17__isnull=True)[:batch_size]
                    #* 拉資料前置
                    update_list = []
                    for i in user_datas:
                        bday = aes_decrypt(i.a5) if i.a5 else 0
                        try:
                            a14 = int(bday.replace('*', '')) + 1911 if bday else None
                        except Exception as e:
                            a14 = None
                            logger.info(f'bday格式錯誤：{str(e)}，a8：{i.a8}，{str(e)} exception in line {sys.exc_info()[2].tb_lineno}')
                            exit()
                        # print(a14)
                        try:
                            if i.a3 and '＊＊＊' in i.a3:
                                i.a17 = date_now
                                update_list.append(i)
                                continue
                            address_match = carName_re.match(i.a3.replace(' ', '').replace('　', '').replace('巿', '市')) if i.a3 else ''
                            city_name = address_match[1].replace('台', '臺') if address_match[1] else None
                            area_name = address_match[2] if address_match[2] else None
                            if city_name in ['新竹市', '嘉義市']:
                                a15 = city_name
                                a16 = city_name
                            else:
                                a15 = old_city_dict[city_name] if city_name in old_city_dict else city_name
                                a16 = old_area_dict[area_name] if area_name in old_area_dict else area_name
                        except Exception as e:
                            a15 = None
                            a16 = None
                            # print(address_match)
                            # print(address_match[1])
                            logger.info(f'地址錯誤：{str(e)}，a3：{i.a3}，{str(e)} exception in line {sys.exc_info()[2].tb_lineno}')
                        # print(a15)
                        # print(a16)
                        if a15 and len(a15) > 3:
                            print(f'"{a15}"')
                            a15 = None
                            a16 = None
                            logger.info(f'外國地址：{i.a3}')
                        if a14:
                            i.a14 = a14
                        if a15:
                            i.a15 = a15
                        if a16:
                            i.a16 = a16
                        i.a17 = date_now
                        update_list.append(i)

                    with transaction.atomic():
                        if update_list:
                            logger.info(f'更新筆數：{len(update_list)}')
                            Abiu.objects.bulk_update(update_list, fields=['a14', 'a15', 'a16', 'a17'])
                        end2 = time.perf_counter()
                        logger.info(f'此批次時間：{end2 - start2}秒')
                        logger.info('')
                    # break

                end1 = time.perf_counter()
                logger.info(f'基本資料更新完成，總執行時間：{end1 - start1}秒')
            except Exception as e:
                end1 = time.perf_counter()
                logger.info(f'基本資料失敗，總執行時間：{end1 - start1}，{str(e)} exception in line {sys.exc_info()[2].tb_lineno}')

        #! 更新他項最後設定時間
        if options['task_type'] == 'LT':
            start1 = time.perf_counter()
            try:
                lbtype = options['lbtype']
                date_now = datetime.strftime((datetime.now()), "%Y-%m-%d")
                owner_datas = 'start'
                while owner_datas:
                    start2 = time.perf_counter()
                    lbkey_dict = {}
                    django_query = []
                    owner_datas = Citron.objects.filter(c13__isnull=True, c3=lbtype)[:batch_size]
                    #* 拉資料前置
                    for i in owner_datas:
                        lbkey = i.c4
                        regno = i.c5
                        django_query.append(reduce(operator.and_,[Q(lbkey=lbkey), Q(regno=regno)]))
                    #* 拉資料
                    if django_query:
                        if lbtype == 'L':
                            datas = LkeyRegnoList.objects.filter(reduce(operator.or_, django_query))
                        elif lbtype == 'B':
                            datas = BkeyRegnoList.objects.filter(reduce(operator.or_, django_query))
                        for i in datas:
                            lbkey = i.lbkey
                            regno = i.regno
                            lbkey_regno = ';'.join([lbkey, regno])
                            lbkey_dict[lbkey_regno] = {
                                                    'c14': timezone.localtime(i.creditors_last_setting_time).strftime("%Y-%m-%d") if i.creditors_last_setting_time else None
                                                    }
                    #* 處理更新
                    update_list = []
                    if lbkey_dict:
                        for i in owner_datas:
                            lbkey = i.c4
                            regno = i.c5
                            lbkey_regno = ';'.join([lbkey, regno])
                            data = lbkey_dict[lbkey_regno] if lbkey_regno in lbkey_dict else {}
                            if data:
                                i.c14 = data['c14']
                            i.c13 = date_now
                            update_list.append(i)

                    with transaction.atomic():
                        if update_list:
                            logger.info(f'更新筆數：{len(update_list)}')
                            Citron.objects.bulk_update(update_list, fields=['c13', 'c14'])
                        end2 = time.perf_counter()
                        logger.info(f'此批次時間：{end2 - start2}秒')
                        logger.info('')
                    # break

                end1 = time.perf_counter()
                logger.info(f'登序資料更新完成，總執行時間：{end1 - start1}秒')
            except Exception as e:
                end1 = time.perf_counter()
                logger.info(f'登序資料失敗，總執行時間：{end1 - start1}，{str(e)} exception in line {sys.exc_info()[2].tb_lineno}')