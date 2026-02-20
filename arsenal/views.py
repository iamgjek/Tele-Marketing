import base64
import json
import logging
import sys
import time
from datetime import date, datetime
from decimal import Decimal

import requests
from Crypto.Cipher import AES
from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.core.management import call_command
from django.db import transaction
from django.db.models.fields.files import ImageFieldFile
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.http import HttpResponse
from django.utils import timezone
from django.views import View
from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework import authentication, permissions
from rest_framework.authentication import SessionAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView

from arsenal.management.commands import arsenal_owner_inside
from arsenal.models import BuildingOwner, LandOwner
from arsenal.serializers import GetInfomationSerializer
from common.util import aes_decrypt, aes_encrypt
from i_search.management.commands import owner_handle
from i_search.models import Abiu

logger = logging.getLogger(__name__)

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

class GetInfomation(APIView):
    TAG = "[GetInfomation]"

    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.AllowAny]

    def process(self, request):
        result = {'status': 'NG'}
        try:
            params = request.POST
            udata = params.get('udata', None)

            nationality_type = {0: '未知', 1: '本國人', 2: '外國人或無國籍人', 3: '取得國籍之外國人', 4: '原無戶籍國民', 5: '原港澳人民', 6: '原大陸人民'}
            gender_type = {0: '未知', 1: '男', 2: '女'}

            p_data = Abiu.objects.get(a8=udata)
            data = {
                    'uid': p_data.a1,
                    'name': p_data.a2,
                    'addr': p_data.a3,
                    'bday': aes_decrypt(p_data.a5),
                    'nationality': nationality_type[p_data.a6],
                    'gender': gender_type[p_data.a7],
                    'reg_date': p_data.a11,
                    'query_time': timezone.localtime(p_data.a13).strftime("%Y-%m-%d %H:%M:%S")
                    }
            result['status'] = 'OK'
            result['data'] = data
        except:
            result['msg'] = '無資料'
        return result

    @extend_schema(
        summary='取資料',
        description='取資料',
        request=GetInfomationSerializer,
        responses={
            200: OpenApiResponse(description='ok'),
            401: OpenApiResponse(description='身分認證失敗'),
        },
    )

    def post(self, request):
        logger.info('取資料')
        time_start = time.perf_counter()
        result = self.process(request)
        time_end = time.perf_counter()
        logger.info(f'花費時間：{time_end - time_start}秒')
        return HttpResponse(json.dumps(result, ensure_ascii=False, cls=CustomJsonEncoder), content_type="application/json; charset=utf-8")

class ArsenalLandOwnerInput(View):
    TAG = "[ArsenalLandOwnerInput]"

    def process(self, request):
        result = {'status': 'NG'}
        try:
            #! 匯入
            call_command(arsenal_owner_inside.Command(), lbtype='L')
            #! 更新
            call_command(owner_handle.Command(), task_type='UP')
            call_command(owner_handle.Command(), task_type='OH', lbtype='L')
            result['status'] = '土地登序匯入完成'
        except:
            result['msg'] = '無資料'
        return result

    def get(self, request):
        logger.info('土地登序匯入開始')
        time_start = time.perf_counter()
        result = self.process(request)
        time_end = time.perf_counter()
        logger.info(f'花費時間：{time_end - time_start}秒')
        return HttpResponse(json.dumps(result, ensure_ascii=False, cls=CustomJsonEncoder), content_type="application/json; charset=utf-8")

class ArsenalBuildOwnerInput(View):
    TAG = "[ArsenalBuildOwnerInput]"

    def process(self, request):
        result = {'status': 'NG'}
        try:
            #! 匯入
            call_command(arsenal_owner_inside.Command(), lbtype='B')
            #! 更新
            call_command(owner_handle.Command(), task_type='UP')
            call_command(owner_handle.Command(), task_type='OH', lbtype='B')
            result['status'] = '建物登序匯入完成'
        except:
            result['msg'] = '無資料'
        return result

    def get(self, request):
        logger.info('建物登序匯入開始')
        time_start = time.perf_counter()
        result = self.process(request)
        time_end = time.perf_counter()
        logger.info(f'花費時間：{time_end - time_start}秒')
        return HttpResponse(json.dumps(result, ensure_ascii=False, cls=CustomJsonEncoder), content_type="application/json; charset=utf-8")
