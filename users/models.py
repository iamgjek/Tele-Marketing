import json
import os
from datetime import datetime
from uuid import uuid4

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
# from django_mysql.models import EnumField
from storages.backends.s3boto3 import S3Boto3Storage

from users.enums import (Case_Type_Class, Right_Type_Class, Time_Range_Class,
                         age_Class, event_Class, uid_Class)


class CustomJSONField(models.JSONField):
    ''' json 的 Field'''
    def get_prep_value(self, value):
        if value is None:
            return value
        return json.dumps(value, ensure_ascii=False)

class MediaStorage(S3Boto3Storage):
    location = settings.AWS_MEDIA_LOCATION
    default_acl = 'private'
    file_overwrite = False
    custom_domain = False

def path_and_rename(instance, filename):
    upload_to = '{}/{:02d}/{:02d}/'.format(datetime.now().year,datetime.now().month,datetime.now().day)
    ext = filename.split('.')[-1]
    filename = '{}.{}'.format(uuid4().hex, ext)
    return os.path.join(upload_to, filename)

def get_storage():
    file_storage = MediaStorage()
    return file_storage

class User(AbstractUser):
    sip_ext = models.CharField(max_length=100, null=True, blank=True, verbose_name='使用分機')
    sip_id = models.CharField(max_length=100, null=True, blank=True, verbose_name='呼叫中心系统 id')
    sip_pwd = models.CharField(max_length=100, null=True, blank=True, verbose_name='呼叫中心系统 pwd')
    phone = models.CharField(max_length=30, null=True, blank=True, verbose_name='電話')
    user_token = models.UUIDField(default=uuid4, unique=True, verbose_name='使用者公鑰')

    class Meta:
        verbose_name = "使用者資訊"
        verbose_name_plural = "使用者資訊"

    def __str__(self):
        return '{}'.format(self.username)

class Company(models.Model):
    company_name = models.CharField(max_length=100, null=True, blank=True, verbose_name='公司名稱')
    company_id = models.CharField(max_length=10, null=True, blank=True, verbose_name='統編')
    sub_domain = models.CharField(max_length=100, null=True, blank=True, verbose_name='子域')
    ccsi = models.CharField(max_length=100, null=True, blank=True, verbose_name='呼叫中心系统 IP')
    open_data = CustomJSONField(default=list, blank=True, null=True, verbose_name='開放資料')
    contact_person = models.CharField(max_length=100, null=True, blank=True, verbose_name='聯絡人')
    phone = models.CharField(max_length=30, null=True, blank=True, verbose_name='電話')
    logo = models.ImageField(null=True, blank=True, upload_to=path_and_rename, storage=get_storage(), verbose_name='上傳logo')
    is_valid = models.BooleanField(default=True, verbose_name='是否有效')
    create_time = models.DateTimeField(auto_now_add=True, null=False, blank=False, verbose_name='建立時間')
    update_time = models.DateTimeField(null=True, blank=True, verbose_name='最後更新時間')

    class Meta:
        verbose_name = "公司資訊"
        verbose_name_plural = "公司資訊"
        indexes = [
            models.Index(fields=['is_valid']),
        ]

    def __str__(self):
        return '{}'.format(self.company_name)

class CompanyUserMapping(models.Model):
    company = models.ForeignKey(Company, blank=True, null=True, on_delete=models.CASCADE, verbose_name='公司')
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE, verbose_name='使用者')
    is_admin = models.BooleanField(default=False, verbose_name='是否為老闆')
    is_manager = models.BooleanField(default=False, verbose_name='是否為主管')
    is_operator = models.BooleanField(default=False, verbose_name='是否為專員')
    is_valid = models.BooleanField(default=True, verbose_name='是否有效')
    create_time = models.DateTimeField(auto_now_add=True, null=False, blank=False, verbose_name='建立時間')
    update_time = models.DateTimeField(null=True, blank=True, verbose_name='最後更新時間')

    class Meta:
        verbose_name = "公司和使用者對照表"
        verbose_name_plural = "公司和使用者對照表"
        indexes = [
            models.Index(fields=['company']),
            models.Index(fields=['user']),
            models.Index(fields=['is_admin']),
            models.Index(fields=['is_manager']),
            models.Index(fields=['is_operator']),
            models.Index(fields=['is_valid']),
        ]

class DownloadHistory(models.Model):
    company = models.ForeignKey(Company, blank=True, null=True, on_delete=models.CASCADE, verbose_name='公司')
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE, verbose_name='使用者')
    filename = models.CharField(max_length=100, null=False, blank=False, unique=True, verbose_name='檔案名稱')
    #* 搜尋條件紀錄
    event = models.IntegerField(choices=event_Class.choices(), default=event_Class.UNSETTING, verbose_name='清單類型')
    lbtype = models.CharField(max_length=1, null=True, blank=True, verbose_name='土建型態')
    age_range = CustomJSONField(default=list, blank=True, null=True, verbose_name='年齡區間')
    uid_tag = CustomJSONField(default=list, blank=True, null=True, verbose_name='性別')
    case_type = CustomJSONField(default=list, blank=True, null=True, verbose_name='情資類別')
    right_type = CustomJSONField(default=list, blank=True, null=True, verbose_name='權利範圍型態')
    addr = CustomJSONField(null=True, blank=True, verbose_name='戶籍所在地')
    lb_addr = CustomJSONField(null=True, blank=True, verbose_name='土建所在地')
    setting_time = models.CharField(max_length=10, null=True, blank=True, verbose_name='他項設定時間')
    right_holder = models.CharField(max_length=50, null=True, blank=True, verbose_name='權利人搜索')
    set_amount_lo = models.IntegerField(null=True, blank=True, verbose_name='設定金額(下限)')
    set_amount_up = models.IntegerField(null=True, blank=True, verbose_name='設定金額(上限)')
    set_start_time = CustomJSONField(default=dict, blank=True, null=True, verbose_name='設定契約起始時間')
    set_end_time = CustomJSONField(default=dict, blank=True, null=True, verbose_name='設定契約終止時間')
    del_call_phone = models.BooleanField(default=False, verbose_name='是否排除接聽')

    count = models.IntegerField(default=0, null=True, blank=True, verbose_name='電話筆數')
    downloads = models.IntegerField(default=1, verbose_name='下載次數')
    create_time = models.DateTimeField(auto_now_add=True, null=False, blank=False, verbose_name='建立時間')
    last_download_time = models.DateTimeField(null=True, blank=True, verbose_name='最後下載時間')

    class Meta:
        verbose_name = "下載歷史紀錄"
        verbose_name_plural = "下載歷史紀錄"
        indexes = [
            models.Index(fields=['company']),
            models.Index(fields=['user']),
            models.Index(fields=['event']),
            models.Index(fields=['lbtype']),
            models.Index(fields=['set_amount_lo', 'set_amount_up']),
        ]

#* 測試用可刪除
# class DownloadHistory_v2(models.Model):
#     company = models.ForeignKey(Company, blank=True, null=True, on_delete=models.CASCADE, verbose_name='公司')
#     user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE, verbose_name='使用者')
#     filename = models.CharField(max_length=100, null=False, blank=False, unique=True, verbose_name='檔案名稱')
#     #* 搜尋條件紀錄
#     event = models.IntegerField(default=0, blank=False, null=False, verbose_name='清單類型')
#     lbtype = models.CharField(max_length=1, null=True, blank=True, verbose_name='土建型態')
#     age_range = CustomJSONField(default=list, blank=True, null=True, verbose_name='年齡區間')
#     uid_tag = CustomJSONField(default=list, blank=True, null=True, verbose_name='性別')
#     case_type = CustomJSONField(default=list, blank=True, null=True, verbose_name='情資類別')
#     right_type = CustomJSONField(default=list, blank=True, null=True, verbose_name='權利範圍型態')
#     addr = CustomJSONField(null=True, blank=True, verbose_name='戶籍所在地')
#     lb_addr = CustomJSONField(null=True, blank=True, verbose_name='土建所在地')
#     right_holder = CustomJSONField(null=True, blank=True, verbose_name='權利人搜索')
#     set_amount_lo = models.IntegerField(null=True, blank=True, verbose_name='設定金額(下限)')
#     set_amount_up = models.IntegerField(null=True, blank=True, verbose_name='設定金額(上限)')
#     set_time_range = CustomJSONField(default=list, blank=True, null=True, verbose_name='設定時間')

#     downloads = models.IntegerField(default=1, verbose_name='下載次數')
#     create_time = models.DateTimeField(auto_now_add=True, null=False, blank=False, verbose_name='建立時間')
#     last_download_time = models.DateTimeField(null=True, blank=True, verbose_name='最後下載時間')

#     class Meta:
#         verbose_name = "下載歷史紀錄"
#         verbose_name_plural = "下載歷史紀錄"
#         indexes = [
#             models.Index(fields=['company']),
#             models.Index(fields=['user']),
#             models.Index(fields=['event', 'lbtype']),
#             models.Index(fields=['event', 'set_amount_lo', 'set_amount_up']),
#             models.Index(fields=['lbtype']),
#             models.Index(fields=['set_amount_lo', 'set_amount_up']),
#         ]

