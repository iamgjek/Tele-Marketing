# coding:utf-8
from i_search.property_type_list import *
from i_search.enums import PropertyType_Class
import logging

logger = logging.getLogger('analyser.parser')

TAG = '[Parser]'
land_list = []
build_list = []

# 計算公法人、私法人、自然人數量、所有權型態
def get_target_amount_one_str(target_str, report=False):
    try:
        if is_public(target_str) == True:
            res_p = PropertyType_Class.Goverment
            res_s = '公'
        elif is_finance(target_str) == True:
            res_p = PropertyType_Class.Finance
            res_s = '銀'
        elif is_rental(target_str) == True:
            res_p = PropertyType_Class.Rental
            res_s = '租'
        elif is_private(target_str) == True:
            res_p = PropertyType_Class.Private
            res_s = '私'
        elif is_company(target_str) == True:
            res_p = PropertyType_Class.Company
            res_s = '法'
        else:
            res_p = PropertyType_Class.Unknown
            res_s = '未'
    except:
        res_p = PropertyType_Class.NoneType
        res_s = None
    return res_p, res_s

def is_public(owner):
    if owner in public_list:
        return True
    elif owner.replace('台', '臺') in public_list:
        return True
    elif owner.find('中華民國') >= 0:
        return True
    elif owner.endswith('農田水利會'):
        return True
    else:
        return False

def is_finance(owner):
    if owner in finance_list:
        return True
    elif owner.find('銀行') >= 0:
        return True
    elif owner.find('漁會') >= 0:
        return True
    elif owner.find('農會') >= 0:
        return True
    elif owner.find('合作社') >= 0:
        return True
    elif owner.find('人壽') >= 0:
        return True
    elif owner.find('保險') >= 0:
        return True
    elif owner.find('郵政') >= 0:
        return True
    else:
        return False

def is_rental(owner):
    if owner in rental_list:
        return True
    elif owner.find('車租賃') >= 0:
        return False
    elif owner.find('租賃') >= 0:
        return True
    elif owner.find('中租') >= 0:
        return True
    else:
        return False

def is_private(owner):
    if owner.find('＊') >= 0:
        return True
    elif owner.find('*') >= 0:
        return True
    elif len(owner) == 3:
        return True
    else:
        return False

def is_company(owner):
    if owner.endswith('公司'):
        return True
    elif owner.endswith('工會'):
        return True
    elif owner.endswith('公會'):
        return True
    elif owner.endswith('總會'):
        return True
    elif owner.endswith('宮'):
        return True
    elif owner.endswith('廟'):
        return True
    elif owner.endswith('寺'):
        return True
    elif owner.endswith('庵'):
        return True
    elif owner.endswith('堂'):
        return True
    elif owner.endswith('殿'):
        return True
    elif owner.endswith('祀'):
        return True
    elif owner.endswith('壇'):
        return True
    elif owner.find('財團法人') >= 0:
        return True
    elif owner.find('社團法人') >= 0:
        return True
    elif owner.endswith('教會'):
        return True
    elif owner.endswith('商會'):
        return True
    elif owner.endswith('祠'):
        return True
    elif owner.endswith('中心'):
        return True
    elif owner.endswith('社'):
        return True
    elif owner.startswith('祭祀公業'):
        return True
    elif owner.startswith('祭祀公會'):
        return True
    elif owner.startswith('公業'):
        return True
    elif owner.startswith('公號'):
        return True
    elif owner.endswith('公業'):
        return True
    elif owner.endswith('宗親會'):
        return True
    elif owner.endswith('農場'):
        return True
    elif owner.endswith('精舍'):
        return True
    elif owner.endswith('協會'):
        return True
    elif owner.endswith('慈善會'):
        return True
    elif owner.endswith('獅子會'):
        return True
    elif owner.endswith('同鄉會'):
        return True
    elif owner.endswith('聯合會'):
        return True
    elif owner.endswith('學會'):
        return True
    elif owner.endswith('委員會'):
        return True
    elif owner.endswith('同濟會'):
        return True
    elif owner.endswith('協進會'):
        return True
    elif owner.endswith('校友會'):
        return True
    elif owner.endswith('研究會'):
        return True
    elif owner.endswith('神明會'):
        return True
    elif owner.endswith('道院'):
        return True
    elif owner.endswith('商業會'):
        return True
    elif owner.endswith('健行會'):
        return True
    elif owner.endswith('工業會'):
        return True
    elif owner.endswith('佛院'):
        return True
    elif owner.endswith('工廠'):
        return True
    elif owner.endswith('苑'):
        return True
    elif owner.endswith('高級中學'):
        return True
    elif owner.find('同業公會') >= 0:
        return True
    elif owner.find('公業法人') >= 0:
        return True
    elif owner.find('慈祐宮') >= 0:
        return True
    elif owner in company_list:
        return True
    else:
        return False
