import json

from django.db import models

from i_search.enums import (PropertyType_Class, a6_Class, a7_Class, c9_Class,
                            c10_Class, case_category_Class, case_status_Class,
                            handle_Class, target_type_Class,
                            transfer_out_Class)
from users.models import User


class CustomJSONField(models.JSONField):
    ''' json 的 Field'''
    def get_prep_value(self, value):
        if value is None:
            return value
        return json.dumps(value, ensure_ascii=False)

class Abiu(models.Model):
    a1 = models.CharField(max_length=100, null=True, blank=True)
    a2 = models.CharField(max_length=100, null=True, blank=True)
    a3 = models.CharField(max_length=500, null=True, blank=True)
    a4 = models.CharField(max_length=500, null=True, blank=True)
    a5 = models.CharField(max_length=100, null=True, blank=True)
    a6 = models.IntegerField(choices=a6_Class.choices(), default=a6_Class.UNKNOWN)
    a7 = models.IntegerField(choices=a7_Class.choices(), default=a7_Class.UNKNOWN)
    a8 = models.CharField(max_length=100, unique=True, null=False, blank=False)
    a9 = models.CharField(max_length=300, null=True, blank=True)
    a10 = models.CharField(max_length=100, null=True, blank=True)
    a11 = models.DateField(null=False, blank=False)
    a12 = models.DateTimeField(auto_now_add=True, null=False, blank=False)
    a13 = models.DateTimeField(null=True, blank=True)
    a14 = models.IntegerField(null=True, blank=True)
    a15 = models.CharField(max_length=10, null=True, blank=True)
    a16 = models.CharField(max_length=10, null=True, blank=True)
    a17 = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = "黃晶果"
        verbose_name_plural = "黃晶果"
        indexes = [
            models.Index(fields=['a6']),
            models.Index(fields=['a7']),
            models.Index(fields=['a9']),
            models.Index(fields=['a10']),
            models.Index(fields=['a11']),
            models.Index(fields=['a14']),
            models.Index(fields=['a15', 'a16']),
            models.Index(fields=['a15']),
            models.Index(fields=['a16']),
            models.Index(fields=['a17']),
        ]

class Babaco(models.Model):
    b1 = models.CharField(max_length=20, null=True, blank=True)
    b2 = models.CharField(max_length=20, null=True, blank=True)
    b3 = models.CharField(max_length=20, null=True, blank=True)
    b4 = models.CharField(max_length=100, null=True, blank=True)
    b5 = models.CharField(max_length=100, null=True, blank=True)
    b6 = models.CharField(max_length=100, null=True, blank=True)
    b7 = models.BooleanField(default=True)
    b8 = models.DateTimeField(auto_now_add=True, null=False, blank=False)
    b9 = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = "香檳果"
        verbose_name_plural = "香檳果"
        unique_together = ('b4', 'b5')
        indexes = [
            models.Index(fields=['b4']),
            models.Index(fields=['b5']),
            models.Index(fields=['b6']),
            models.Index(fields=['b7']),
        ]

class Citron(models.Model):
    c1 = models.CharField(max_length=20, null=True, blank=True)
    c2 = models.CharField(max_length=100, null=True, blank=True)
    c3 = models.CharField(max_length=1, null=True, blank=True)
    c4 = models.CharField(max_length=20, null=True, blank=True)
    c5 = models.CharField(max_length=10, null=True, blank=True)
    c6 = models.BooleanField(default=True)
    c7 = models.DateTimeField(auto_now_add=True, null=False, blank=False)
    c8 = models.DateTimeField(null=True, blank=True)
    c9 = models.IntegerField(choices=c9_Class.choices(), default=c9_Class.NONE)
    c10 = models.IntegerField(choices=c10_Class.choices(), default=c10_Class.NONE)
    c11 = models.CharField(max_length=10, null=True, blank=True)
    c12 = models.CharField(max_length=10, null=True, blank=True)
    c13 = models.DateTimeField(null=True, blank=True)
    c14 = models.DateField(null=True, blank=True)

    class Meta:
        verbose_name = "枸櫞"
        verbose_name_plural = "枸櫞"
        unique_together = ('c4', 'c5')
        indexes = [
            models.Index(fields=['c2']),
            models.Index(fields=['c3']),
            models.Index(fields=['c4', 'c5']),
            models.Index(fields=['c6']),
            models.Index(fields=['c9']),
            models.Index(fields=['c10']),
            models.Index(fields=['c11', 'c12']),
            models.Index(fields=['c11']),
            models.Index(fields=['c12']),
            models.Index(fields=['c13']),
            models.Index(fields=['c14'])
        ]

class Damson(models.Model):
    d1 = models.CharField(max_length=20, null=True, blank=True)
    d2 = models.CharField(max_length=100, null=True, blank=True, unique=True)
    d3 = CustomJSONField(default=list, null=True, blank=True)
    d4 = models.TextField(blank=True, null=True)
    d5 = models.BooleanField(default=True)
    d6 = models.DateTimeField(auto_now_add=True, null=False, blank=False)
    d7 = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = "烏荊子李"
        verbose_name_plural = "烏荊子李"
        indexes = [
            models.Index(fields=['d2']),
            models.Index(fields=['d5']),
        ]

class DamsonQuery(models.Model):
    damson = models.ForeignKey(Damson, blank=True, null=True, on_delete=models.CASCADE, verbose_name='單身')
    registration_authority = models.CharField(max_length=50, null=True, blank=True, verbose_name='登記機關')
    case_category = models.IntegerField(choices=case_category_Class.choices(), default=case_category_Class.Unknown, verbose_name='案件類別')
    case_status = models.IntegerField(choices=case_status_Class.choices(), default=case_status_Class.Unknown, verbose_name='案件狀態')
    registration_number = models.CharField(max_length=50, null=True, blank=True, unique=True, verbose_name='登記編號')
    mortgagee_name = models.CharField(max_length=50, null=True, blank=True, verbose_name='抵押權人名稱')
    mortgagee_agent_name = models.CharField(max_length=50, null=True, blank=True, verbose_name='代理抵押權人名稱')
    property_type = models.IntegerField(choices=PropertyType_Class.choices(), default=PropertyType_Class.Unknown, verbose_name='權利人型態')
    guarantee_amount = models.IntegerField(null=True, blank=True, verbose_name='擔保債權金額')
    contract_start = models.DateField(null=True, blank=True, verbose_name='契約啟始日期')
    contract_end = models.DateField(null=True, blank=True, verbose_name='契約終止日期')
    property_detail = models.IntegerField(default=0, null=True, blank=True, verbose_name='動產明細項數')
    is_maximum = models.BooleanField(default=False, null=True, blank=True, verbose_name='是否最高限額')
    is_floating = models.BooleanField(default=False, null=True, blank=True, verbose_name='是否為浮動擔保')
    target_type = models.IntegerField(choices=target_type_Class.choices(), default=target_type_Class.Unknown, verbose_name='標的物種類')

    class Meta:
        verbose_name = "搜尋單身表"
        verbose_name_plural = "搜尋單身表"
        indexes = [
            models.Index(fields=['damson']),
            models.Index(fields=['case_category']),
            models.Index(fields=['case_status']),
            models.Index(fields=['mortgagee_name']),
            models.Index(fields=['property_type']),
            models.Index(fields=['contract_start', 'contract_end']),
            models.Index(fields=['contract_end']),
            models.Index(fields=['target_type'])
        ]

class info_config(models.Model):
    mode_str = models.CharField(max_length=100, null=True, blank=True, verbose_name='mode')
    last_id = models.IntegerField(null=True, blank=True, verbose_name='最後一筆id')
    remark = models.TextField(blank=True, null=True, verbose_name='備註')
    last_time = models.DateTimeField(null=True, blank=True, verbose_name='最後時間')

    class Meta:
        verbose_name = "紀錄表"
        verbose_name_plural = "紀錄表"

class TIRecord(models.Model):
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE, verbose_name='記錄人')
    utoken = models.CharField(max_length=20, null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True, verbose_name='電話')
    ptoken = models.CharField(max_length=100, null=True, blank=True)
    tag = CustomJSONField(default=list, null=True, blank=True, verbose_name='標籤清單')
    is_valid = models.BooleanField(default=True, verbose_name='有效性')
    is_read = models.BooleanField(default=False, verbose_name='是否已讀')
    create_time = models.DateTimeField(auto_now_add=True, null=False, blank=False, verbose_name='建立時間')
    update_time = models.DateTimeField(null=True, blank=True, verbose_name='更新時間')

    class Meta:
        verbose_name = "電訪紀錄"
        verbose_name_plural = "電訪紀錄"
        unique_together = ('user', 'phone', 'ptoken')
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['utoken']),
            models.Index(fields=['ptoken']),
            models.Index(fields=['tag']),
            models.Index(fields=['is_valid']),
        ]

class History(models.Model):
    ti_record = models.ForeignKey(TIRecord, blank=True, null=True, on_delete=models.CASCADE, verbose_name='電訪紀錄')
    transfer_out_type = models.IntegerField(choices=transfer_out_Class.choices(), default=transfer_out_Class.UNKNOWN, verbose_name='轉出類型')
    handle_type = models.IntegerField(choices=handle_Class.choices(), default=handle_Class.UNKNOWN, verbose_name='處理類型')
    memo = models.TextField(blank=True, null=True, verbose_name='内文')
    create_time = models.DateTimeField(auto_now_add=True, null=False, blank=False, verbose_name='建立時間')
    update_time = models.DateTimeField(null=True, blank=True, verbose_name='更新時間')

    class Meta:
        verbose_name = "歷史紀錄"
        verbose_name_plural = "歷史紀錄"
        indexes = [
            models.Index(fields=['ti_record']),
            models.Index(fields=['transfer_out_type']),
            models.Index(fields=['handle_type']),
        ]
