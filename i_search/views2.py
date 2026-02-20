import copy
import csv
import hashlib
import json
import logging
import mimetypes
import operator
import os
import sys
import time
import traceback
from datetime import date, datetime, timedelta
from decimal import Decimal
from io import BytesIO, StringIO

import numpy as np
import openpyxl
import pandas as pd
import requests
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.db import transaction
from django.db.models.fields.files import ImageFieldFile
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.http import (Http404, HttpResponse, HttpResponseBadRequest,
                         JsonResponse)
from django.shortcuts import HttpResponseRedirect, redirect, render
from django.utils import timezone
from django.views.generic.base import TemplateView, View
from drf_spectacular.utils import (OpenApiCallback, OpenApiExample,
                                   OpenApiParameter, OpenApiResponse,
                                   Serializer, extend_schema,
                                   inline_serializer)
from openpyxl import Workbook, load_workbook
from openpyxl.utils import get_column_letter
from rest_framework import authentication, generics, permissions, serializers
from rest_framework.authentication import SessionAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import ParseError
from rest_framework.response import Response
from rest_framework.views import APIView

from arsenal.views import aes_decrypt, aes_encrypt
from common.util import check_role, excel_file_write_sheets, get_sub_domain
from diablo.models import BkeyRegnoList, LkeyRegnoList
from i_search.forms import UploadFileForm
from i_search.models import Abiu, Babaco, Citron, Damson, History, TIRecord
from i_search.serializers import (AddRemarkSerializer,
                                  DownloadPhoneNumberSerializer,
                                  SaveRecordSerializer, TirecordSerializer)
from users.models import Company, CompanyUserMapping, DownloadHistory, User

logger = logging.getLogger(__name__)

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

class GetDownloadList(APIView):
    TAG = "[GetDownloadList]"

    authentication_classes = (CsrfExemptSessionAuthentication, )

    def 組電話清單(self, data_list, download_datas):
        for i in download_datas:
            filename = i.filename
            if filename and os.path.exists('output_file/' + filename):
                company_name = i.company.company_name if i.company else '元宏創新股份有限公司'
                username = i.user.first_name if i.user else 'yeshome'
                sub_domain = i.company.sub_domain if i.company else 'www'
                search_condition = {
                                    'event': '謄本' if i.event == 1 else '動保' if i.event == 2 else None,
                                    'age_interval': i.age_range if i.age_range else [],
                                    'gender': i.uid_tag if i.uid_tag else [],
                                    'credits': i.case_type if i.case_type else [],
                                    'rights': i.right_type if i.right_type else [],
                                    'location': i.lb_addr if i.lb_addr else [],
                                    'setting_time': i.setting_time if i.setting_time else None,
                                    'right_holder': i.right_holder if i.right_holder else None,
                                    'set_amount_lo': i.set_amount_lo if i.set_amount_lo else None,
                                    'set_amount_up': i.set_amount_up if i.set_amount_up else None,
                                    'set_start_time_lo': (i.set_start_time)['set_start_time_lo'] if i.set_start_time and 'set_start_time_lo' in i.set_start_time and (i.set_start_time)['set_start_time_lo'] else None,
                                    'set_start_time_up': (i.set_start_time)['set_start_time_up'] if i.set_start_time and 'set_start_time_up' in i.set_start_time and (i.set_start_time)['set_start_time_up'] else None,
                                    'set_end_time_lo': (i.set_end_time)['set_end_time_lo'] if i.set_end_time and 'set_end_time_lo' in i.set_end_time and (i.set_end_time)['set_end_time_lo'] else None,
                                    'set_end_time_up': (i.set_end_time)['set_end_time_up'] if i.set_end_time and 'set_end_time_up' in i.set_end_time and (i.set_end_time)['set_end_time_up'] else None,
                                    'del_call_phone': True if i.del_call_phone else False
                                    # 'set_start_time': i.set_start_time if i.set_start_time else {'set_start_time_lo': None, 'set_start_time_up': None},
                                    # 'set_end_time': i.set_end_time if i.set_end_time else {'set_end_time_lo': None, 'set_end_time_up': None}
                                    }
                # search_list = []
                # if i.event == 1:
                #     search_condition += '謄本 '
                #     if i.age_range:
                #         search_list.extend(i.age_range)
                #     if i.uid_tag:
                #         search_list.extend(i.uid_tag)
                #     if i.case_type:
                #         search_list.extend(i.case_type)
                #     if i.right_type:
                #         search_list.extend(i.right_type)
                #     if i.addr:
                #         search_list.extend([str(addr) for addr in i.addr])
                #     if i.lb_addr:
                #         search_list.extend([str(lb_addr) for lb_addr in i.lb_addr])
                #     if search_list:
                #         search_condition += ', '.join(search_list)
                # elif i.event == 2:
                #     search_condition += '動保'
                data_list.append({
                    'filename': filename,
                    'sub_domain': sub_domain,
                    'company_name': company_name,
                    'user_name': username,
                    'search_condition': search_condition,
                    'count': i.count,
                    'downloads': i.downloads,
                    'datetime': timezone.localtime(i.last_download_time).strftime("%Y/%m/%d %H:%M:%S")
                    })

    def process(self, request):
        result = {'status': 'NG'}
        try:
            role = check_role(request)
            data_list = []
            download_datas = None
            if role == 0:
                download_datas = DownloadHistory.objects.all().order_by('-last_download_time')
            elif role in [1, 2]:
                user_id = User.objects.get(username=request.user.get_username()).id
                company_id = CompanyUserMapping.objects.filter(user_id=user_id, is_valid=1)[0].company_id
                download_datas = DownloadHistory.objects.filter(company_id=company_id).order_by('-last_download_time')
            else:
                result['msg'] = '無權限'
                return result

            if download_datas:
                self.組電話清單(data_list, download_datas)

            result['status'] = 'OK'
            result['msg'] = '成功傳送資料'
            result['data'] = data_list
        except Exception as e:
            print(e, 'exception in line', sys.exc_info()[2].tb_lineno)
            result['msg'] = '發生不可預期的錯誤，請聯繫官方客服'
        return result

    @extend_schema(
        summary='取電話檔案清單',
        description='取電話檔案清單',
        request=None,
        responses={
            200: OpenApiResponse(description='ok'),
            401: OpenApiResponse(description='身分認證失敗'),
        },
    )

    def get(self, request):
        logger.info('取電話檔案清單')
        time_start = time.perf_counter()
        result = self.process(request)
        time_end = time.perf_counter()
        logger.info(f'花費時間：{time_end - time_start}秒')
        if result['status'] == 'NG':
            return HttpResponseBadRequest(json.dumps(result, ensure_ascii=False, cls=CustomJsonEncoder), content_type="application/json; charset=utf-8")
        return HttpResponse(json.dumps(result, ensure_ascii=False, cls=CustomJsonEncoder), content_type="application/json; charset=utf-8")

