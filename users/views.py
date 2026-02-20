import json
import logging
import sys
import time
from datetime import date, datetime
from decimal import Decimal

import requests
from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.db import transaction
from django.db.models.fields.files import ImageFieldFile
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.http import HttpResponse
from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework import authentication, permissions
from rest_framework.authentication import SessionAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView

from users.models import Company, CompanyUserMapping, User
from users.serializers import (AddCompanySerializer, GetCompanyInfoSerializer,
                               ModifyCompanySerializer, GetUserListSerializer, AddUserSerializer, ModifyUserSerializer)

logger = logging.getLogger(__name__)
#* 開放資料清單
open_data_dict = {0: '土地', 1: '建物', 2: '動產'}
re_open_data_dict = {v: k for k, v in open_data_dict.items()}
is_test = False
#! 上code請遮
# is_test = True
#! 測試用
test_sub_domain = 'www-test'
# test_sub_domain = 'zsa'

def check_role(request):
    #! 檢查sub_domain
    user_id = User.objects.get(username=request.user.get_username()).id
    urls = request.build_absolute_uri('/')[:-1].strip("/")
    if '.telem.com.tw' in urls or '.vvips.com.tw' in urls:
        url_t = '.telem.com.tw' if '.telem.com.tw' in urls else '.vvips.com.tw' if '.vvips.com.tw' in urls else ''
        sub_domain = urls.split(url_t)[0].split('//')[1]
    else:
        sub_domain = test_sub_domain
    companys = Company.objects.filter(sub_domain=sub_domain, is_valid=1)
    if companys:
        company_id = companys[0].id
    else:
        company_id = None
    # else:
    #     company_id = 1
    #! 檢查角色
    #* role_dict = {0: 'Administrator(元宏本身)', 1: Admin(老闆), 2: Manager(店東或廠商主管), 3: Operator(廠商旗下的業務), 4: other(非此sub_domain下的帳號)}
    check_user = CompanyUserMapping.objects.filter(user_id=user_id, is_valid=1)
    if check_user:
        role = 4 if company_id and check_user[0].company_id != company_id else 1 if check_user[0].is_admin == 1 else 2 if check_user[0].is_manager == 1 else 3
    else:
        role = 0
    return role

def get_sub_domain(request):
    urls = request.build_absolute_uri('/')[:-1].strip("/")
    if '.telem.com.tw' in urls or '.vvips.com.tw' in urls:
        url_t = '.telem.com.tw' if '.telem.com.tw' in urls else '.vvips.com.tw' if '.vvips.com.tw' in urls else ''
        sub_domain = urls.split(url_t)[0].split('//')[1]
    else:
        sub_domain = 'www-test'
    return sub_domain

def remove_sub_domain_name(name):
    name = '.'.join(name.split('.')[1:])
    return name

class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return None

class CustomJsonEncoder(json.JSONEncoder):
    def default(self, obj): # pylint: disable=E0202
        if isinstance(obj, Decimal):
            return float(obj)
        elif isinstance(obj, datetime):
            return obj.isoformat()
        elif isinstance(obj, date):
            return obj.strftime("%Y-%m-%d")
        elif isinstance(obj, ImageFieldFile):
            if obj:
                return obj.path
            return None
        return json.JSONEncoder.default(self, obj)

class GetCompanyList(APIView):
    TAG = "[GetCompanyList]"

    authentication_classes = (CsrfExemptSessionAuthentication, )

    def process(self, request):
        result = {'status': 'NG'}
        try:
            role = check_role(request)
            if role == 0:
                sql = '''SELECT a.id, a.company_name, c.username, a.sub_domain, a.open_data, a.phone, a.is_valid FROM telem.users_company a
                        left join telem.users_companyusermapping b on b.company_id=a.id and b.is_admin=1
                        left join telem.users_user c on c.id = b.user_id
                        '''
                companys = Company.objects.raw(sql)
                data_list = []
                for i in companys:
                    open_data = '、'.join(i.open_data) if i.open_data else ''
                    data_list.append({
                        'name': i.company_name,
                        'account': i.username,
                        'sub_domain': i.sub_domain,
                        'open_data': open_data,
                        'phone': i.phone,
                        'state': True if i.is_valid else False,
                        })

                result['status'] = 'OK'
                result['msg'] = '成功傳送資料'
                result['data'] = data_list
            else:
                result['msg'] = '無權限'
        except Exception as e:
            print(e, 'exception in line', sys.exc_info()[2].tb_lineno)
            result['msg'] = '發生不可預期的錯誤，請聯繫官方客服'
        return result

    @extend_schema(
        summary='取帳號列表(公司)',
        description='取帳號列表(公司)',
        request=None,
        responses={
            200: OpenApiResponse(description='ok'),
            401: OpenApiResponse(description='身分認證失敗'),
        },
    )

    def get(self, request):
        logger.info('取帳號列表(公司)')
        time_start = time.perf_counter()
        result = self.process(request)
        time_end = time.perf_counter()
        logger.info(f'花費時間：{time_end - time_start}秒')
        return HttpResponse(json.dumps(result, ensure_ascii=False, cls=CustomJsonEncoder), content_type="application/json; charset=utf-8")

#* 新增帳號時自動建立token
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    # 建立帳號時 自動觸發
    if created:
        Token.objects.create(user=instance)

class AddCompany(APIView):
    TAG = "[AddCompany]"

    authentication_classes = (CsrfExemptSessionAuthentication, )

    def process(self, request):
        result = {'status': 'NG'}
        try:
            role = check_role(request)
            if role == 0:
                params = request.POST
                sub_domain = params.get('sub_domain', None)
                ccsi = params.get('ccsi', None)
                open_data = params.get('open_data', None)
                upload_file = request.FILES.get('upload_file', None)
                account = params.get('account', None)
                password = params.get('password', None)
                password2 = params.get('password2', None)
                company_name = params.get('company_name', None)
                company_id = params.get('company_id', None)
                contact_person = params.get('contact_person', None)
                phone = params.get('phone', None)

                if not company_name:
                    result['msg'] = '公司名稱不能為空'
                    return result

                if not account:
                    result['msg'] = '帳號不能為空'
                    return result

                #* 檢查密碼
                check_password = True if (not password2) or (password2 and password == password2) else False
                if not check_password:
                    result['msg'] = '確認密碼錯誤'
                    return result

                #* 檢查公司有無重複
                company = Company.objects.filter(company_name=company_name, is_valid=1)
                if company:
                    result['msg'] = '該公司已存在'
                    return result

                #* 開放資料處理
                open_data_list = []
                if open_data:
                    for k, v in json.loads(open_data).items():
                        if v:
                            open_data_list.append(open_data_dict[int(k)])

                with transaction.atomic():
                    try:
                        user = User.objects.create(username=account, password=make_password(password), first_name=contact_person, phone=phone)
                    except:
                        result['msg'] = '已存在此公司帳號'
                        return result
                    company = Company.objects.create(company_name=company_name, company_id=company_id, sub_domain=sub_domain, phone=phone, open_data=open_data_list,
                                                    contact_person=contact_person, logo=upload_file, ccsi=ccsi)
                    CompanyUserMapping.objects.create(user=user, company=company, is_admin=True)

                result['status'] = 'OK'
                result['msg'] = '新增公司帳號成功'
            else:
                result['msg'] = '無權限'
        except Exception as e:
            print(e, 'exception in line', sys.exc_info()[2].tb_lineno)
            result['msg'] = '發生不可預期的錯誤，請聯繫官方客服'
        return result

    @extend_schema(
        summary='新增帳號(公司)',
        description='新增帳號(公司)',
        request=AddCompanySerializer,
        responses={
            200: OpenApiResponse(description='ok'),
            401: OpenApiResponse(description='身分認證失敗'),
        },
    )

    def post(self, request):
        logger.info('新增帳號(公司)')
        time_start = time.perf_counter()
        result = self.process(request)
        time_end = time.perf_counter()
        logger.info(f'花費時間：{time_end - time_start}秒')
        return HttpResponse(json.dumps(result, ensure_ascii=False, cls=CustomJsonEncoder), content_type="application/json; charset=utf-8")

class ModifyCompany(APIView):
    TAG = "[ModifyCompany]"

    authentication_classes = (CsrfExemptSessionAuthentication, )

    def process(self, request):
        result = {'status': 'NG'}
        try:
            role = check_role(request)
            if role == 0:
                params = request.POST
                sub_domain = params.get('sub_domain', None)
                ccsi = params.get('ccsi', None)
                open_data = params.get('open_data', None)
                upload_file = request.FILES.get('upload_file', None)
                account = params.get('account', None)
                state = params.get('state', 'true')
                company_name = params.get('company_name', None)
                company_id = params.get('company_id', None)
                contact_person = params.get('contact_person', None)
                phone = params.get('phone', None)
                state = json.loads(state)

                #* 帳號
                try:
                    user = User.objects.get(username=account)
                    if contact_person:
                        user.first_name = contact_person
                    if phone:
                        user.phone = phone
                except:
                    result['msg'] = '不存在的帳號'
                    return result

                #* 公司
                cu_mapping = CompanyUserMapping.objects.get(user=user, is_admin=1)
                cu_mapping.is_valid = state
                cid = cu_mapping.company_id
                company = Company.objects.get(id=cid)
                if company_name:
                    company.company_name = company_name
                if company_id:
                    company.company_id = company_id
                if sub_domain:
                    company.sub_domain = sub_domain
                if contact_person:
                    company.contact_person = contact_person
                if phone:
                    company.phone = phone
                if ccsi:
                    company.ccsi = ccsi
                if upload_file:
                    company.logo = upload_file
                company.is_valid = state

                #* 開放地區處理
                open_data_list = []
                if open_data:
                    for k, v in json.loads(open_data).items():
                        if v:
                            open_data_list.append(open_data_dict[int(k)])

                company.open_data = open_data_list

                with transaction.atomic():
                    user.save()
                    company.save()
                    cu_mapping.save()

                result['status'] = 'OK'
                result['msg'] = '修改帳號資料成功'
            else:
                result['msg'] = '無權限'
        except Exception as e:
            print(e, 'exception in line', sys.exc_info()[2].tb_lineno)
            result['msg'] = '發生不可預期的錯誤，請聯繫官方客服'
        return result

    @extend_schema(
        summary='修改帳號(公司)',
        description='修改帳號(公司)',
        request=ModifyCompanySerializer,
        responses={
            200: OpenApiResponse(description='ok'),
            401: OpenApiResponse(description='身分認證失敗'),
        },
    )

    def post(self, request):
        logger.info('修改帳號(公司)')
        time_start = time.perf_counter()
        result = self.process(request)
        time_end = time.perf_counter()
        logger.info(f'花費時間：{time_end - time_start}秒')
        return HttpResponse(json.dumps(result, ensure_ascii=False, cls=CustomJsonEncoder), content_type="application/json; charset=utf-8")

class GetCompanyInfo(APIView):
    TAG = "[GetCompanyInfo]"

    authentication_classes = (CsrfExemptSessionAuthentication, )

    def process(self, request):
        result = {'status': 'NG'}
        try:
            role = check_role(request)
            if role == 0:
                params = request.POST
                account = params.get('account', None)

                sql = f'''SELECT c.id, c.sub_domain, c.ccsi, c.open_data, c.logo, a.username, c.is_valid, c.company_name, c.company_id, c.contact_person, c.phone
                        FROM telem.users_user a
                        left join telem.users_companyusermapping b on b.user_id=a.id
                        left join telem.users_company c on c.id=b.company_id
                        where a.username="{account}"'''
                datas = User.objects.raw(sql)
                for data in datas:
                    c_id = data.id
                    logo = Company.objects.get(id=c_id).logo
                    open_data = json.loads(data.open_data) if data.open_data else []
                    city_dict = {re_open_data_dict[i]: True for i in open_data} if open_data else {}
                    data_dict = {
                                'sub_domain': data.sub_domain,
                                'ccsi': data.ccsi,
                                'open_area': city_dict,
                                'logo': logo.url if logo else '',
                                'account': data.username,
                                'state': True if data.is_valid else False,
                                'company_name': data.company_name,
                                'company_id': data.company_id,
                                'contact_person': data.contact_person,
                                'phone': data.phone
                                }

                result['status'] = 'OK'
                result['msg'] = '取得公司帳號資訊成功'
                result['data'] = data_dict
            else:
                result['msg'] = '無權限'
        except Exception as e:
            print(e, 'exception in line', sys.exc_info()[2].tb_lineno)
            result['msg'] = '發生不可預期的錯誤，請聯繫官方客服'
        return result

    @extend_schema(
        summary='取得帳號資訊(公司)',
        description='取得帳號資訊(公司)',
        request=GetCompanyInfoSerializer,
        responses={
            200: OpenApiResponse(description='ok'),
            401: OpenApiResponse(description='身分認證失敗'),
        },
    )

    def post(self, request):
        logger.info('取得帳號資訊(公司)')
        time_start = time.perf_counter()
        result = self.process(request)
        time_end = time.perf_counter()
        logger.info(f'花費時間：{time_end - time_start}秒')
        return HttpResponse(json.dumps(result, ensure_ascii=False, cls=CustomJsonEncoder), content_type="application/json; charset=utf-8")

class GetUserList(APIView):
    TAG = "[GetCompanyList]"

    authentication_classes = (CsrfExemptSessionAuthentication, )

    def process(self, request):
        result = {'status': 'NG'}
        try:
            role = check_role(request)
            if role in [0, 1, 2]:
                company_account = self.username
                data_list = []
                sql = f'''SELECT c.id
                        FROM telem.users_user a
                        left join telem.users_companyusermapping b on b.user_id=a.id
                        left join telem.users_company c on c.id=b.company_id
                        where a.username="{company_account}"'''
                company_id = User.objects.raw(sql)[0].id
                if not company_id:
                    sql = f'''SELECT a.id, a.is_manager, a.is_operator, b.first_name, b.username, b.phone, b.sip_ext, b.sip_id, b.sip_pwd FROM telem.users_companyusermapping a
                            left join telem.users_user b on b.id=a.user_id
                            left join telem.users_company c on c.id=a.company_id
                            where a.is_admin=0 and a.is_valid=1;
                            '''
                else:
                    role_str = '' if role in [0, 1] else ' and a.is_manager=0'
                    sql = f'''SELECT a.id, a.is_manager, a.is_operator, b.first_name, b.username, b.phone, b.sip_ext, b.sip_id, b.sip_pwd FROM telem.users_companyusermapping a
                            left join telem.users_user b on b.id=a.user_id
                            left join telem.users_company c on c.id=a.company_id
                            where a.company_id={company_id} and a.is_admin=0 and a.is_valid=1{role_str};
                            '''
                try:
                    users = User.objects.raw(sql)
                    for i in users:
                        data_list.append({
                            'name': i.first_name,
                            'account': remove_sub_domain_name(i.username),
                            'phone': i.phone,
                            'sip_ext': i.sip_ext,
                            'sip_id': i.sip_id,
                            'role': '主管' if i.is_manager else '專員'
                            })
                except:
                    pass
                result['status'] = 'OK'
                result['msg'] = '成功傳送資料'
                result['data'] = data_list
            else:
                result['msg'] = '無權限'
        except Exception as e:
            print(e, 'exception in line', sys.exc_info()[2].tb_lineno)
            result['msg'] = '發生不可預期的錯誤，請聯繫官方客服'
        return result

    @extend_schema(
        summary='取帳號列表(使用者)',
        description='取帳號列表(使用者)',
        request=GetUserListSerializer,
        responses={
            200: OpenApiResponse(description='ok'),
            401: OpenApiResponse(description='身分認證失敗'),
        },
    )

    def get(self, request):
        self.username = User.objects.get(username=request.user.get_username()).username
        logger.info('取帳號列表(使用者)')
        time_start = time.perf_counter()
        result = self.process(request)
        time_end = time.perf_counter()
        logger.info(f'花費時間：{time_end - time_start}秒')
        return HttpResponse(json.dumps(result, ensure_ascii=False, cls=CustomJsonEncoder), content_type="application/json; charset=utf-8")

class AddUser(APIView):
    TAG = "[AddCompany]"

    authentication_classes = (CsrfExemptSessionAuthentication, )

    def process(self, request):
        result = {'status': 'NG'}
        try:
            role = check_role(request)
            sub_domain = get_sub_domain(request)
            if role in [0, 1, 2]:
                params = request.POST
                company_account = self.username
                account = params.get('account', None)
                password = params.get('password', None)
                password2 = params.get('password2', None)
                sip_ext = params.get('sip_ext', None)
                sip_id = params.get('sip_id', None)
                sip_pwd = params.get('sip_pwd', None)
                name = params.get('name', None)
                phone = params.get('phone', None)
                u_role = params.get('role', 3)
                u_role = int(u_role)

                if not account:
                    result['msg'] = '帳號不能為空'
                    return result
                else:
                    account = ''.join([sub_domain, '.', account])

                #* 檢查密碼
                check_password = True if (not password2) or (password2 and password == password2) else False
                if not check_password:
                    result['msg'] = '確認密碼錯誤'
                    return result

                #* 檢查同級不能新增
                if u_role == role:
                    result['msg'] = '無法新增同階級的帳號'
                    return result

                #* 取得公司id
                if company_account:
                    sql = f'''SELECT c.id
                            FROM telem.users_user a
                            left join telem.users_companyusermapping b on b.user_id=a.id
                            left join telem.users_company c on c.id=b.company_id
                            where a.username="{company_account}"'''
                    company_id = User.objects.raw(sql)[0].id
                else:
                    company_id = 1
                try:
                    company = Company.objects.get(id=company_id, is_valid=1)
                except:
                    result['msg'] = '非公司帳號，無此操作權限'
                    return result

                with transaction.atomic():
                    try:
                        user = User.objects.create(username=account, password=make_password(password), first_name=name, phone=phone, sip_ext=sip_ext, sip_id=sip_id,
                                                sip_pwd=sip_pwd)
                    except:
                        result['msg'] = '已存在此帳號'
                        return result
                    if u_role == 2:
                        CompanyUserMapping.objects.create(user=user, company=company, is_manager=True)
                    else:
                        CompanyUserMapping.objects.create(user=user, company=company, is_operator=True)

                result['status'] = 'OK'
                result['msg'] = '新增帳號成功'
            else:
                result['msg'] = '無權限'
        except Exception as e:
            print(e, 'exception in line', sys.exc_info()[2].tb_lineno)
            result['msg'] = '發生不可預期的錯誤，請聯繫官方客服'
        return result

    @extend_schema(
        summary='新增帳號(使用者)',
        description='新增帳號(使用者)',
        request=AddUserSerializer,
        responses={
            200: OpenApiResponse(description='ok'),
            401: OpenApiResponse(description='身分認證失敗'),
        },
    )

    def post(self, request):
        self.username = User.objects.get(username=request.user.get_username()).username
        logger.info('新增帳號(使用者)')
        time_start = time.perf_counter()
        result = self.process(request)
        time_end = time.perf_counter()
        logger.info(f'花費時間：{time_end - time_start}秒')
        return HttpResponse(json.dumps(result, ensure_ascii=False, cls=CustomJsonEncoder), content_type="application/json; charset=utf-8")

class ModifyUser(APIView):
    TAG = "[ModifyCompany]"

    authentication_classes = (CsrfExemptSessionAuthentication, )

    def process(self, request):
        result = {'status': 'NG'}
        try:
            role = check_role(request)
            sub_domain = get_sub_domain(request)
            if role in [0, 1, 2, 3]:
                params = request.POST
                account = params.get('account', None)
                name = params.get('name', None)
                password = params.get('password', None)
                password2 = params.get('password2', None)
                sip_ext = params.get('sip_ext', None)
                sip_id = params.get('sip_id', None)
                sip_pwd = params.get('sip_pwd', None)
                phone = params.get('phone', None)
                delete = params.get('delete', 'false')
                delete = json.loads(delete)

                #* 檢查密碼
                check_password = True if (not password2) or (password2 and password == password2) else False
                if not check_password:
                    result['msg'] = '確認密碼錯誤'
                    return result

                #* 帳號
                try:
                    account = ''.join([sub_domain, '.', account]) if account else None
                    print(account)
                    return result
                    user = User.objects.get(username=account)
                    if name:
                        user.first_name = name
                    if phone:
                        user.phone = phone
                    if sip_ext:
                        user.sip_ext = sip_ext
                    if sip_id:
                        user.sip_id = sip_id
                    if sip_pwd:
                        user.sip_pwd = sip_pwd
                    if password:
                        user.password = make_password(password)
                    if delete:
                        user.is_active = 0
                except:
                    result['msg'] = '不存在的帳號'
                    return result

                with transaction.atomic():
                    user.save()
                    #* 公司
                    if delete:
                        cu_mapping = CompanyUserMapping.objects.filter(user=user, is_admin=0, is_valid=1)
                        for i in cu_mapping:
                            i.is_valid = 0
                            i.save()

                result['status'] = 'OK'
                result['msg'] = '修改帳號資料成功'
            else:
                result['msg'] = '無權限'
        except Exception as e:
            print(e, 'exception in line', sys.exc_info()[2].tb_lineno)
            result['msg'] = '發生不可預期的錯誤，請聯繫官方客服'
        return result

    @extend_schema(
        summary='修改帳號(使用者)',
        description='修改帳號(使用者)',
        request=ModifyUserSerializer,
        responses={
            200: OpenApiResponse(description='ok'),
            401: OpenApiResponse(description='身分認證失敗'),
        },
    )

    def post(self, request):
        logger.info('修改帳號(使用者)')
        time_start = time.perf_counter()
        result = self.process(request)
        time_end = time.perf_counter()
        logger.info(f'花費時間：{time_end - time_start}秒')
        return HttpResponse(json.dumps(result, ensure_ascii=False, cls=CustomJsonEncoder), content_type="application/json; charset=utf-8")

class GetUserInfo(APIView):
    TAG = "[GetCompanyInfo]"

    authentication_classes = (CsrfExemptSessionAuthentication, )

    def process(self, request):
        result = {'status': 'NG'}
        try:
            role = check_role(request)
            sub_domain = get_sub_domain(request)
            if role in [0, 1, 2, 3]:
                params = request.POST
                account = params.get('account', None)
                try:
                    account = ''.join([sub_domain, '.', account]) if account else None
                    data = User.objects.get(username=account)
                    u_role = CompanyUserMapping.objects.get(user_id=data.id, is_valid=1)
                    role = 1 if u_role.is_admin == 1 else 2 if u_role.is_manager == 1 else 3
                except:
                    result['msg'] = '不存在的帳號'
                    return result
                data_dict = {
                            'account': data.username.replace(sub_domain + '.', ''),
                            'name': data.first_name,
                            'phone': data.phone,
                            'sip_ext': data.sip_ext,
                            'sip_id': data.sip_id,
                            'role': role
                            }

                result['status'] = 'OK'
                result['msg'] = '取得帳號資訊成功'
                result['data'] = data_dict
            else:
                result['msg'] = '無權限'
        except Exception as e:
            print(e, 'exception in line', sys.exc_info()[2].tb_lineno)
            result['msg'] = '發生不可預期的錯誤，請聯繫官方客服'
        return result

    @extend_schema(
        summary='取得帳號資訊(使用者)',
        description='取得帳號資訊(使用者)',
        request=GetCompanyInfoSerializer,
        responses={
            200: OpenApiResponse(description='ok'),
            401: OpenApiResponse(description='身分認證失敗'),
        },
    )

    def post(self, request):
        logger.info('取得帳號資訊(使用者)')
        time_start = time.perf_counter()
        result = self.process(request)
        time_end = time.perf_counter()
        logger.info(f'花費時間：{time_end - time_start}秒')
        return HttpResponse(json.dumps(result, ensure_ascii=False, cls=CustomJsonEncoder), content_type="application/json; charset=utf-8")

class GetUserIp(APIView):
    TAG = "[GetUserIp]"

    authentication_classes = (CsrfExemptSessionAuthentication, )

    def process(self, request):
        result = {'status': 'NG'}
        try:
            role = check_role(request)
            sub_domain = get_sub_domain(request)
            if role in [0, 1, 2, 3]:
                params = request.POST
                account = params.get('account', None)
                try:
                    account = ''.join([sub_domain, '.', account]) if account else None
                    data = User.objects.get(username=account)
                except:
                    result['msg'] = '不存在的帳號'
                    return result
                try:
                    company = CompanyUserMapping.objects.filter(user=data, is_valid=1).order_by('-create_time')[0]
                except:
                    result['msg'] = '帳號無綁定公司'
                    return result
                data_dict = {
                            'ccsi': company.company.ccsi,
                            'sip_ext': data.sip_ext,
                            'sip_id': data.sip_id
                            }

                result['status'] = 'OK'
                result['msg'] = '取得資料成功'
                result['data'] = data_dict
            else:
                result['msg'] = '無權限'
        except Exception as e:
            print(e, 'exception in line', sys.exc_info()[2].tb_lineno)
            result['msg'] = '發生不可預期的錯誤，請聯繫官方客服'
        return result

    @extend_schema(
        summary='取得帳號ip(使用者)',
        description='取得帳號ip(使用者)',
        request=GetCompanyInfoSerializer,
        responses={
            200: OpenApiResponse(description='ok'),
            401: OpenApiResponse(description='身分認證失敗'),
        },
    )

    def post(self, request):
        logger.info('取得帳號ip(使用者)')
        time_start = time.perf_counter()
        result = self.process(request)
        time_end = time.perf_counter()
        logger.info(f'花費時間：{time_end - time_start}秒')
        return HttpResponse(json.dumps(result, ensure_ascii=False, cls=CustomJsonEncoder), content_type="application/json; charset=utf-8")