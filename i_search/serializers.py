from rest_framework import serializers

class TirecordSerializer(serializers.Serializer):
    user_account = serializers.CharField(default='dennis1', help_text='帳號')

class SaveRecordSerializer(serializers.Serializer):
    ptoken = serializers.CharField(default='99UnIsbt03WngWJ8JemJNw==', help_text='識別')
    is_call = serializers.CharField(default='0', help_text='是否撥打電話')
    call_end = serializers.CharField(default='0', help_text='是否結束電話')
    thunderbolt = serializers.BooleanField(default=False, help_text='是否顯示')


class AddRemarkSerializer(serializers.Serializer):
    ptoken = serializers.CharField(default='99UnIsbt03WngWJ8JemJNw==', help_text='識別')
    tag_list = serializers.JSONField(default=['二胎', '轉貸'], help_text='標籤清單')
    utoken = serializers.CharField(default='UPEm55ho3zWitAD+y0CmOQ==', help_text='識別')
    transfer_out = serializers.CharField(default='0', help_text='轉出')
    handle_type = serializers.CharField(default='0', help_text='處理類型')
    memo = serializers.CharField(default='測試', help_text='內文')

class DownloadPhoneNumberSerializer(serializers.Serializer): 
    event = serializers.CharField(default='謄本', help_text='1：謄本，2：動保')
    age_interval = serializers.JSONField(default=['20-29','30-39'], help_text='年齡區間')
    gender = serializers.JSONField(default=['男','女'], help_text='姓別')
    rights= serializers.JSONField(default=['全部','持分'], help_text='持分狀態')
    credits= serializers.JSONField(default=['私設', '租賃'], help_text='他項標記')
    location = serializers.JSONField(default=[['新北市','新莊區'], ['新北市','新店區']], help_text='土地/建物所在地')
    setting_time = serializers.CharField(default='近2年', help_text='他項設定時間(近3個月，近6個月，近1年，近2年，2年以上)')
    right_holder = serializers.CharField(default='資融', help_text='找權利人關鍵字')
    right_type = serializers.JSONField(default=['政府機構','自然人', '公司', '租賃業者', '金融機構'], help_text='權利人類別')
    set_amount_lo = serializers.IntegerField(default=0, help_text='設定金額(下限)')
    set_amount_up = serializers.IntegerField(default=0, help_text='設定金額(上限)')
    set_start_time_lo = serializers.CharField(default='2020-10-10', help_text='契約起始(下限)')
    set_start_time_up = serializers.CharField(default='2023-10-10', help_text='契約起始(上限)')
    set_end_time_lo = serializers.CharField(default='2024-10-10', help_text='契約終止(下限)')
    set_end_time_up = serializers.CharField(default='2034-10-10', help_text='契約終止(上限)')
