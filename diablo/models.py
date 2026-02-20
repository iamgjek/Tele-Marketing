from django.db import models

class LmLandList(models.Model):
    lkey = models.CharField(max_length=19, primary_key=True, verbose_name='地號')
    lno = models.CharField(max_length=9, verbose_name='土地子母號')
    city_name = models.CharField(max_length=50, null=True, blank=True, verbose_name='縣市名')   #!
    area_name = models.CharField(max_length=50, null=True, blank=True, verbose_name='行政區')   #!
    region_name = models.CharField(max_length=50, null=True, blank=True, verbose_name='段小段') #!
    plan_name = models.CharField(max_length=100, null=True, blank=True, verbose_name='計劃案名')
    owners_num = models.IntegerField(blank=True, null=True, verbose_name='所有權人數')
    owner_type = models.IntegerField(verbose_name='權屬樣態')
    land_area = models.DecimalField(default=0, max_digits=10, decimal_places=2, verbose_name='土地總面積')
    urban_type = models.IntegerField(verbose_name='都市型態')
    urban_name = models.CharField(max_length=500, blank=True, null=True, verbose_name='都市計畫案名或使用地類別(非都市土地)')
    urban_name_v523 = models.CharField(max_length=500, blank=True, null=True, verbose_name='都市計畫案名或使用地類別_v523(非都市土地)')
    land_zone = models.CharField(max_length=500, null=True, blank=True, verbose_name='使用分區')
    land_zone_code = models.CharField(max_length=3, null=True, blank=True, verbose_name='使用分區編號')
    land_zone_v523 = models.CharField(max_length=500, null=True, blank=True, verbose_name='使用分區_v523')
    national_land_zone = models.CharField(max_length=500, null=True, blank=True, verbose_name='國土分區')
    land_category = models.CharField(max_length=500, null=True, blank=True, verbose_name='地目')
    land_notice_value_date = models.CharField(max_length=100, null=True, blank=True, verbose_name='公告期別')
    land_notice_value = models.CharField(max_length=11, null=True, blank=True, verbose_name='公告土地現值')   #!
    build_num = models.IntegerField(blank=True, null=True, verbose_name='建物數量')
    build_finish_day = models.CharField(max_length=100, null=True, blank=True, verbose_name='建物完成日期(民國)')
    build_finish_time = models.DateTimeField(null=True, blank=True, verbose_name='建物完成日期(datetime)')
    build_type = models.IntegerField(verbose_name='建物型態')
    other_remark = models.IntegerField(verbose_name='標示備註')
    create_time = models.DateTimeField(null=True, blank=True, verbose_name='建立時間')
    update_time = models.DateTimeField(null=True, blank=True, verbose_name='異動時間')
    valid_time = models.DateTimeField(null=True, blank=True, verbose_name='有效日期')
    invalid_time = models.DateTimeField(null=True, blank=True, verbose_name='失效日期')
    is_valid = models.BooleanField(default=True, verbose_name='有效性')

    class Meta:
        managed = False
        db_table = 't_search_lmlandlist'

class LkeyRegnoList(models.Model):
    lbkey =  models.CharField(max_length=19, verbose_name='地建號')
    regno = models.CharField(max_length=4, null=True, blank=True, verbose_name='登序編號')
    add_time = models.DateTimeField(null=True, blank=True, verbose_name='新增時間')
    remove_time = models.DateTimeField(null=True, blank=True, verbose_name='移除時間')
    last_check_time = models.DateTimeField(blank=True, null=True, verbose_name='最後查詢時間')
    property_type = models.IntegerField(verbose_name='登序類型')
    is_valid = models.BooleanField(default=True, verbose_name='有效性')
    reg_date = models.DateField(blank=True, null=True, verbose_name='登記日期')
    reg_date_str = models.CharField(max_length=255, blank=True, null=True, verbose_name='登記日期(字串)')   #!
    reg_reason_str = models.CharField(max_length=255, blank=True, null=True, verbose_name='登記原因(字串)')  #!
    reg_reason = models.IntegerField(verbose_name='登記原因')
    reason_date = models.DateField(blank=True, null=True, verbose_name='原因發生日期')
    reason_date_str = models.CharField(max_length=255, blank=True, null=True, verbose_name='原因發生日期(字串)')
    name = models.CharField(max_length=255, blank=True, null=True, verbose_name='所有權人姓名')
    uid = models.CharField(max_length=10, blank=True, null=True, verbose_name='統一編號／身份證字號')
    address = models.CharField(max_length=255, blank=True, null=True, verbose_name='正規化前住址')
    address_re = models.CharField(max_length=255, blank=True, null=True, verbose_name='正規化後住址')
    query_time = models.DateTimeField(null=True, blank=True, verbose_name='謄本查詢時間')
    query_time_str = models.CharField(max_length=255, blank=True, null=True, verbose_name='謄本查詢日期(字串)')
    right_numerator = models.BigIntegerField(blank=True, null=True, verbose_name='權利範圍分子')
    right_denominator = models.BigIntegerField(blank=True, null=True, verbose_name='權利範圍分母')
    right_str = models.CharField(max_length=255, blank=True, null=True, verbose_name='權利範圍(字串)')   #!
    right_num = models.BigIntegerField(blank=True, null=True, verbose_name='權利範圍(公同共有人數)')
    right_type = models.IntegerField(verbose_name='權利範圍型態')
    shared_size = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name='持分面積')   #!
    restricted_type = models.IntegerField(verbose_name='限制登記型態')
    restricted_reason = models.TextField(blank=True, null=True, verbose_name='限制登記原因')
    case_type = models.IntegerField(verbose_name='情資類別')
    creditors_unknown_num = models.IntegerField(blank=True, null=True, verbose_name='不詳借貸')
    creditors_goverment_num = models.IntegerField(blank=True, null=True, verbose_name='政府機構借貸')
    creditors_private_num = models.IntegerField(blank=True, null=True, verbose_name='自然人借貸')
    creditors_company_num = models.IntegerField(blank=True, null=True, verbose_name='公司借貸')
    creditors_rental_num = models.IntegerField(blank=True, null=True, verbose_name='租賃業者借貸')
    creditors_finance_num = models.IntegerField(blank=True, null=True, verbose_name='金融機構借貸')
    last_creditor_property_type = models.IntegerField(verbose_name='最末借貸人型態')
    creditors_rights = models.TextField(blank=True, null=True, verbose_name='他項權利列示')  #!
    #   1)[銀]107-08-17
    #   上海商業儲蓄(36000000元)
    #   銀:36,000,000私:0總:36,000,000
    creditors_last_setting_time = models.DateTimeField(blank=True, null=True, verbose_name='他項最後設定時間')
    guarantee_amount = models.BigIntegerField(blank=True, null=True, verbose_name='擔保債權總金額')
    collateral_lkey = models.TextField(blank=True, null=True, verbose_name='共同擔保地號(列表)')
    collateral_bkey = models.TextField(blank=True, null=True, verbose_name='共同擔保建號(列表)')
    public_amount = models.BigIntegerField(blank=True, null=True, verbose_name='政府機構借貸總金額')
    private_amount = models.BigIntegerField(blank=True, null=True, verbose_name='自然人借貸總金額')
    company_amount = models.BigIntegerField(blank=True, null=True, verbose_name='公司借貸總金額')
    rental_amount = models.BigIntegerField(blank=True, null=True, verbose_name='租賃業者總金額')
    finance_amount = models.BigIntegerField(blank=True, null=True, verbose_name='金融機構借貸總金額')

    name_all = models.CharField(max_length=255, blank=True, null=True, verbose_name='所有權人姓名(全碼)')
    uid_all = models.CharField(max_length=10, blank=True, null=True, verbose_name='統一編號／身份證字號(全碼)')
    bday = models.DateField(blank=True, null=True, verbose_name='出生日期')
    phone = models.CharField(max_length=30, null=True, blank=True, verbose_name='聯絡電話')
    uid_tag = models.IntegerField(verbose_name='身份標籤(國籍)')
    uid_type_tag = models.IntegerField(verbose_name='身份標籤(型態)')
    owner_remark = models.TextField(blank=True, null=True, verbose_name='所有權註記')

    class Meta:
        managed = False
        db_table = 't_search_lkeyregnolist'

class BmBuildList(models.Model):
    bkey =  models.CharField(max_length=19, primary_key=True, verbose_name='建號')
    city_name = models.CharField(max_length=50, null=True, blank=True, verbose_name='縣市名')  #!
    area_name = models.CharField(max_length=50, null=True, blank=True, verbose_name='行政區')  #!
    region_name = models.CharField(max_length=50, null=True, blank=True, verbose_name='段小段')  #!
    community_name = models.CharField(max_length=500, blank=True, null=True, verbose_name='社區(建物名稱)')  #!
    road_name = models.CharField(max_length=100, null=True, blank=True, verbose_name='路名')
    road_name_re = models.CharField(max_length=100, null=True, blank=True, verbose_name='路名(正規化)')
    door = models.CharField(max_length=500, blank=True, null=True, verbose_name='門牌')   #!
    door_re = models.CharField(max_length=500, blank=True, null=True, verbose_name='正規化門牌')
    door_part = models.CharField(max_length=500, blank=True, null=True, verbose_name='部份門牌')
    owners_num = models.IntegerField(blank=True, null=True, verbose_name='所有權人數')
    owner_type = models.IntegerField(verbose_name='權屬樣態')
    build_size = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True, verbose_name='建物總面積')  #!
    main_size = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True, verbose_name='主建面積')    #!
    attach_size = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True, verbose_name='附屬面積')  #!
    public_size = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True, verbose_name='公設面積')  #!
    parking_size = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True, verbose_name='停車位面積') #!
    parking_no = models.IntegerField(blank=True, null=True, verbose_name='停車位總數')
    level = models.TextField(blank=True, null=True, verbose_name='層次')
    floor_first = models.IntegerField(blank=True, null=True, verbose_name='建物所在第一個樓層')
    floor_last = models.IntegerField(blank=True, null=True, verbose_name='建物所在最後一個樓層')
    total_level = models.IntegerField(blank=True, null=True, verbose_name='總樓層數')   #!
    finish_day = models.CharField(max_length=100, null=True, blank=True, verbose_name='建物完成日期(民國)')
    finish_time = models.DateTimeField(null=True, blank=True, verbose_name='建物完成日期(datetime)')
    use_license_no = models.TextField(blank=True, null=True, verbose_name='使照編號')
    main_purpose = models.IntegerField(verbose_name='主要用途')
    main_material = models.TextField(blank=True, null=True, verbose_name='主要建材')
    car_type = models.IntegerField(verbose_name='車位型態')
    build_type = models.IntegerField(verbose_name='建物型態')
    other_remark = models.IntegerField(verbose_name='標示備註')
    longitude = models.FloatField(blank=True, null=True, verbose_name='經度')
    latitude = models.FloatField(blank=True, null=True, verbose_name='緯度')
    create_time = models.DateTimeField(null=True, blank=True, verbose_name='建立時間')
    update_time = models.DateTimeField(null=True, blank=True, verbose_name='異動時間')
    valid_time = models.DateTimeField(null=True, blank=True, verbose_name='有效日期')
    invalid_time = models.DateTimeField(null=True, blank=True, verbose_name='失效日期')
    build_share = models.BooleanField(default=False, verbose_name='是否為共有(公設)建物')
    public_check = models.IntegerField(verbose_name='檢查補登公設')
    public_replenish = models.BooleanField(default=False, verbose_name='是否要補登公設(非公設建物)')
    balcony_check = models.IntegerField(verbose_name='檢查補登陽台(非公設建物)')
    balcony_replenish = models.BooleanField(default=False, verbose_name='是否要補登陽台(非公設建物)')
    is_valid = models.BooleanField(default=True, verbose_name='有效性')
    data_complete = models.BooleanField(default=True, verbose_name='資料完整')

    class Meta:
        managed = False
        db_table = 't_search_bmbuildlist'

class BkeyRegnoList(models.Model):
    lbkey =  models.CharField(max_length=19, verbose_name='地建號')
    regno = models.CharField(max_length=4, null=True, blank=True, verbose_name='登序編號')
    add_time = models.DateTimeField(null=True, blank=True, verbose_name='新增時間')
    remove_time = models.DateTimeField(null=True, blank=True, verbose_name='移除時間')
    last_check_time = models.DateTimeField(blank=True, null=True, verbose_name='最後查詢時間')
    property_type = models.IntegerField(verbose_name='登序類型')
    is_valid = models.BooleanField(default=True, verbose_name='有效性')
    reg_date = models.DateField(blank=True, null=True, verbose_name='登記日期')
    reg_date_str = models.CharField(max_length=255, blank=True, null=True, verbose_name='登記日期(字串)')    #!
    reg_reason_str = models.CharField(max_length=255, blank=True, null=True, verbose_name='登記原因(字串)')  #!
    reg_reason = models.IntegerField(verbose_name='登記原因')
    reason_date = models.DateField(blank=True, null=True, verbose_name='原因發生日期')
    reason_date_str = models.CharField(max_length=255, blank=True, null=True, verbose_name='原因發生日期(字串)')
    name = models.CharField(max_length=255, blank=True, null=True, verbose_name='所有權人姓名')
    uid = models.CharField(max_length=10, blank=True, null=True, verbose_name='統一編號／身份證字號')
    address = models.CharField(max_length=255, blank=True, null=True, verbose_name='正規化前住址')
    address_re = models.CharField(max_length=255, blank=True, null=True, verbose_name='正規化後住址')
    query_time = models.DateTimeField(null=True, blank=True, verbose_name='謄本查詢時間')
    query_time_str = models.CharField(max_length=255, blank=True, null=True, verbose_name='謄本查詢日期(字串)')
    right_numerator = models.BigIntegerField(blank=True, null=True, verbose_name='權利範圍分子')
    right_denominator = models.BigIntegerField(blank=True, null=True, verbose_name='權利範圍分母')
    right_str = models.CharField(max_length=255, blank=True, null=True, verbose_name='權利範圍(字串)')
    right_num = models.BigIntegerField(blank=True, null=True, verbose_name='權利範圍(公同共有人數)')
    right_type = models.IntegerField(verbose_name='權利範圍型態')
    shared_size = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name='持分面積')
    restricted_type = models.IntegerField(verbose_name='限制登記型態')
    restricted_reason = models.TextField(blank=True, null=True, verbose_name='限制登記原因')   #!
    case_type = models.IntegerField(verbose_name='情資類別')
    creditors_unknown_num = models.IntegerField(blank=True, null=True, verbose_name='不詳借貸')
    creditors_goverment_num = models.IntegerField(blank=True, null=True, verbose_name='政府機構借貸')
    creditors_private_num = models.IntegerField(blank=True, null=True, verbose_name='自然人借貸')
    creditors_company_num = models.IntegerField(blank=True, null=True, verbose_name='公司借貸')
    creditors_rental_num = models.IntegerField(blank=True, null=True, verbose_name='租賃業者借貸')
    creditors_finance_num = models.IntegerField(blank=True, null=True, verbose_name='金融機構借貸')
    last_creditor_property_type = models.IntegerField(verbose_name='最末借貸人型態')
    creditors_rights = models.TextField(blank=True, null=True, verbose_name='他項權利列示')  #!
    #   1)[銀]107-08-17
    #   上海商業儲蓄(36000000元)
    #   銀:36,000,000私:0總:36,000,000
    creditors_last_setting_time = models.DateTimeField(blank=True, null=True, verbose_name='他項最後設定時間')
    guarantee_amount = models.BigIntegerField(blank=True, null=True, verbose_name='擔保債權總金額')
    collateral_lkey = models.TextField(blank=True, null=True, verbose_name='共同擔保地號(列表)')
    collateral_bkey = models.TextField(blank=True, null=True, verbose_name='共同擔保建號(列表)')
    public_amount = models.BigIntegerField(blank=True, null=True, verbose_name='政府機構借貸總金額')
    private_amount = models.BigIntegerField(blank=True, null=True, verbose_name='自然人借貸總金額')
    company_amount = models.BigIntegerField(blank=True, null=True, verbose_name='公司借貸總金額')
    rental_amount = models.BigIntegerField(blank=True, null=True, verbose_name='租賃業者總金額')
    finance_amount = models.BigIntegerField(blank=True, null=True, verbose_name='金融機構借貸總金額')

    name_all = models.CharField(max_length=255, blank=True, null=True, verbose_name='所有權人姓名(全碼)')
    uid_all = models.CharField(max_length=10, blank=True, null=True, verbose_name='統一編號／身份證字號(全碼)')
    bday = models.DateField(blank=True, null=True, verbose_name='出生日期')
    phone = models.CharField(max_length=30, null=True, blank=True, verbose_name='聯絡電話')
    uid_tag = models.IntegerField(verbose_name='身份標籤(國籍)')
    uid_type_tag = models.IntegerField(verbose_name='身份標籤(型態)')
    owner_remark = models.TextField(blank=True, null=True, verbose_name='所有權註記')

    class Meta:
        managed = False
        db_table = 't_search_bkeyregnolist'