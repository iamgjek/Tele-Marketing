from enum import Enum, IntEnum

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

class a6_Class(IntChoiceEnum):
    # 未知
    UNKNOWN = 0
    # 本國人
    NATIVES = 1
    # 外國人或無國籍人
    FOREIGNERS = 2
    # 取得國籍之外國人
    FOREIGNERS_N = 3
    # 原無戶籍國民
    NATIVES_N = 4
    # 原港澳人民
    HKMC = 5
    # 原大陸人民
    CH = 6

    @classmethod
    def choices(cls):
        CHOICES = (
            (cls.UNKNOWN.value, '未知'),
            (cls.NATIVES.value, '本國人'),
            (cls.FOREIGNERS.value, '外國人或無國籍人'),
            (cls.FOREIGNERS_N.value, '取得國籍之外國人'),
            (cls.NATIVES_N.value, '原無戶籍國民'),
            (cls.HKMC.value, '原港澳人民'),
            (cls.CH.value, '原大陸人民'),
        )
        return CHOICES

class a7_Class(IntChoiceEnum):
    # 未知
    UNKNOWN = 0
    # 男
    MAN = 1
    # 女
    WOMAN = 2

    @classmethod
    def choices(cls):
        CHOICES = (
            (cls.UNKNOWN.value, '未知'),
            (cls.MAN.value, '男'),
            (cls.WOMAN.value, '女'),
        )
        return CHOICES

class handle_Class(IntChoiceEnum):
    # 未設定
    UNKNOWN = 0
    # 聯繫
    CONNECT = 1
    # 更新進度
    UPDATE_PROGRESS = 2
    # 結案
    CLOSE_CASE = 3

    @classmethod
    def choices(cls):
        CHOICES = (
            (cls.UNKNOWN.value, '未知'),
            (cls.CONNECT.value, '聯繫'),
            (cls.UPDATE_PROGRESS.value, '更新進度'),
            (cls.CLOSE_CASE.value, '結案'),
        )
        return CHOICES

class transfer_out_Class(IntChoiceEnum):
    # 未設定
    UNKNOWN = 0
    # 有意願購買,轉主管
    WTBTTS = 1
    # 加入待追蹤名單
    JTWI = 2
    # 放棄,電訪三次找不到人
    GUCTTACFA = 3
    # 放棄,無意願購買
    GUUTB = 4


    @classmethod
    def choices(cls):
        CHOICES = (
            (cls.UNKNOWN.value, '未知'),
            (cls.WTBTTS.value, '有意願購買,轉主管'),
            (cls.JTWI.value, '加入待追蹤名單'),
            (cls.GUCTTACFA.value, '放棄,電訪三次找不到人'),
            (cls.GUUTB.value, '放棄,無意願購買'),
        )
        return CHOICES

class c9_Class(IntChoiceEnum):
    # 未分類
    NONE = 0
    # 全部
    WHOLE = 1
    # 持分
    SHARED = 2
    # 公同共有
    COMMON_SHARED = 3

    @classmethod
    def choices(cls):
        CHOICES = (
            (cls.NONE.value, '未分類'),
            (cls.WHOLE.value, '全部'),
            (cls.SHARED.value, '持分'),
            (cls.COMMON_SHARED.value, '公同共有'),
        )
        return CHOICES

class c10_Class(IntChoiceEnum):
    # 無設定
    NONE = 0
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
            (cls.NONE.value, '無設定'),
            (cls.PRIVATE.value, '私設'),
            (cls.BANKS.value, '銀行二胎'),
            (cls.BANK.value, '銀行'),
            (cls.RENTAL.value, '租賃'),
            (cls.COMPANY.value, '公司'),
            (cls.GOVERMENT.value, '政府機構'),
        )
        return CHOICES    

#! 動保權利人類別
class PropertyType_Class(IntEnum):
    # 無
    NoneType = -1
    # 不詳
    Unknown = 0
    # 政府機構
    Goverment = 1
    # 自然人
    Private = 2
    # 公司
    Company = 3
    # 租賃業者
    Rental = 4
    # 金融機構
    Finance = 5

    @classmethod
    def choices(cls):
        CHOICES = (
            (cls.NoneType.value, '無'),
            (cls.Unknown.value, '不詳'),
            (cls.Goverment.value, '政府機構'),
            (cls.Private.value, '自然人'),
            (cls.Company.value, '公司'),
            (cls.Rental.value, '租賃業者'),
            (cls.Finance.value, '金融機構'),
        )
        return CHOICES

class case_category_Class(IntEnum):
    # 不詳
    Unknown = 0
    # 動產抵押
    ChattelMortgage = 1
    # 附條件買賣
    ConditionalSale = 2
    # 信託占有
    TrustPossession = 3

    @classmethod
    def choices(cls):
        CHOICES = (
            (cls.Unknown.value, '不詳'),
            (cls.ChattelMortgage.value, '動產抵押'),
            (cls.ConditionalSale.value, '附條件買賣'),
            (cls.TrustPossession.value, '信託占有'),
        )
        return CHOICES

class case_status_Class(IntEnum):
    # 不詳
    Unknown = 0
    # 效期內
    ValidityPeriod = 1
    # 已過效期未註銷
    Expired = 2

    @classmethod
    def choices(cls):
        CHOICES = (
            (cls.Unknown.value, '不詳'),
            (cls.ValidityPeriod.value, '政府機構'),
            (cls.Expired.value, '自然人'),
        )
        return CHOICES

class target_type_Class(IntEnum):
    # 無資料
    NoneType = -1
    # 不詳
    Unknown = 0
    # 汽車、大型重型機器腳踏車及拖車
    Automobiles = 1
    # 總噸位未滿二十噸之動力漁船或未滿五十噸之非動力漁船
    FishingVessels = 2
    # 漁船以外之小船
    SmallBoats = 3
    # 機器設備或工具
    Machine = 4

    @classmethod
    def choices(cls):
        CHOICES = (
            (cls.NoneType.value, '無資料'),
            (cls.Unknown.value, '不詳'),
            (cls.Automobiles.value, '汽車、大型重型機器腳踏車及拖車'),
            (cls.FishingVessels.value, '總噸位未滿二十噸之動力漁船或未滿五十噸之非動力漁船'),
            (cls.SmallBoats.value, '漁船以外之小船'),
            (cls.Machine.value, '機器設備或工具'),
        )
        return CHOICES

# 廢棄
class d8_Class(IntEnum):
    # 無
    NoneType = -1
    # 不詳
    Unknown = 0
    # 政府機構
    Goverment = 1
    # 自然人
    Private = 2
    # 公司
    Company = 3
    # 租賃業者
    Rental = 4
    # 金融機構
    Finance = 5

    @classmethod
    def choices(cls):
        CHOICES = (
            (cls.NoneType.value, '無'),
            (cls.Unknown.value, '不詳'),
            (cls.Goverment.value, '政府機構'),
            (cls.Private.value, '自然人'),
            (cls.Company.value, '公司'),
            (cls.Rental.value, '租賃業者'),
            (cls.Finance.value, '金融機構'),
        )
        return CHOICES