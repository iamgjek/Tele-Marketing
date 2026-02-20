from enum import Enum, IntEnum
from django.db import models

class IntChoiceEnum(IntEnum):

    @classmethod
    def nameList(cls):
        return list(map(lambda x: x.name, cls))

    @classmethod
    def valueList(cls):
        return list(map(lambda x: x.value, cls))

    @classmethod
    def choices(cls):
        return tuple(lambda x: (x.name, x.value), cls)

    @classmethod
    def dictionary(cls):
        return dict(map(lambda x: x, cls.choices()))

class age_Class(IntChoiceEnum):
    # 未設定
    UNSETTING = 0
    # 20-30
    AGE1 = 1
    # 30-40
    AGE2 = 2
    # 40-50
    AGE3 = 3
    # 50-60
    AGE4 = 4

    @classmethod
    def choices(cls):
        CHOICES = (
            (cls.UNSETTING.value, '未設定'),
            (cls.AGE1.value, '20-30'),
            (cls.AGE2.value, '30-40'),
            (cls.AGE3.value, '40-50'),
            (cls.AGE4.value, '50-60'),
        )
        return CHOICES

class uid_Class(IntChoiceEnum):
    # 未設定
    UNSETTING = 0
    # 男
    MAN = 1
    # 女
    WOMAN = 2

    @classmethod
    def choices(cls):
        CHOICES = (
            (cls.UNSETTING.value, '未設定'),
            (cls.MAN.value, '男'),
            (cls.WOMAN.value, '女'),
        )
        return CHOICES

class Right_Type_Class(IntChoiceEnum):
    # 未設定
    UNSETTING = 0
    # 全部
    WHOLE = 1
    # 持分
    SHARED = 2

    @classmethod
    def choices(cls):
        CHOICES = (
            (cls.UNSETTING.value, '未設定'),
            (cls.WHOLE.value, '全部'),
            (cls.SHARED.value, '持分'),
        )
        return CHOICES

class Case_Type_Class(IntChoiceEnum):
    # 未設定
    UNSETTING = 0
    # 私設
    PRIVATE = 1
    # 銀行二胎
    BANKS = 2
    # 銀行
    BANK = 3
    # 租賃
    RENTAL = 4
    # 公司
    COMPANY = 5
    # 政府機構
    GOVERMENT = 6

    @classmethod
    def choices(cls):
        CHOICES = (
            (cls.UNSETTING.value, '未設定'),
            (cls.PRIVATE.value, '私設'),
            (cls.BANKS.value, '銀行二胎'),
            (cls.BANK.value, '銀行'),
            (cls.RENTAL.value, '租賃'),
            (cls.COMPANY.value, '公司'),
            (cls.GOVERMENT.value, '政府機構'),
        )
        return CHOICES    

class Time_Range_Class(IntChoiceEnum):
    # 未設定
    UNSETTING = 0
    # 兩年內
    TIME1 = 1
    # 五年內
    TIME2 = 2
    # 十年內
    TIME3 = 3

    @classmethod
    def choices(cls):
        CHOICES = (
            (cls.UNSETTING.value, '未設定'),
            (cls.TIME1.value, '兩年內'),
            (cls.TIME2.value, '五年內'),
            (cls.TIME3.value, '十年內'),
        )
        return CHOICES   

class event_Class(IntChoiceEnum):
    # 未設定
    UNSETTING = 0
    # 謄本
    TRANSCRIPT = 1
    # 動保
    PROPERTY = 2

    @classmethod
    def choices(cls):
        CHOICES = (
            (cls.UNSETTING.value, '未設定'),
            (cls.TRANSCRIPT.value, '謄本'),
            (cls.PROPERTY.value, '動保'),
        )
        return CHOICES    

# class event_Class(models.TextChoices):
#     # 未設定
#     UNSETTING = '未設定'
#     # 謄本
#     TRANSCRIPT = '謄本'
#     # 動保
#     PROPERTY = '動保'

#     # @classmethod
#     # def choices(cls):
#     #     CHOICES = (
#     #         (cls.UNSETTING.value, '未設定'),
#     #         (cls.TRANSCRIPT.value, '謄本'),
#     #         (cls.PROPERTY.value, '動保'),
#     #     )
#     #     return CHOICES    
