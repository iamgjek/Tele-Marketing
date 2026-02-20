from rest_framework import serializers

class AddCompanySerializer(serializers.Serializer):
    sub_domain = serializers.CharField(default='kent', help_text='')
    ccsi = serializers.CharField(default='127.0.0.1', help_text='呼叫中心系统 IP')
    open_data = serializers.JSONField(default={0:True, 1:False}, help_text='開放資料')
    # upload_file = serializers.CharField(default='', help_text='圖片檔')
    account = serializers.CharField(default='tim', help_text='帳號')
    password = serializers.CharField(default='1234', help_text='密碼')
    password2 = serializers.CharField(default='1234', help_text='確認密碼')
    company_name = serializers.CharField(default='元宏創新服務股份有限公司', help_text='公司名稱')
    company_id = serializers.CharField(default='54167553', help_text='統編')
    contact_person = serializers.CharField(default='dennis', help_text='聯絡人')
    phone = serializers.CharField(default='0987654321', help_text='電話')

class ModifyCompanySerializer(serializers.Serializer):
    sub_domain = serializers.CharField(default='kent', help_text='')
    ccsi = serializers.CharField(default='127.0.0.1', help_text='呼叫中心系统 IP')
    open_data = serializers.JSONField(default={0:True, 1:False}, help_text='開放資料')
    # upload_file = serializers.CharField(default='', help_text='圖片檔')
    account = serializers.CharField(default='dennis', help_text='帳號')
    password = serializers.CharField(default='1234', help_text='密碼')
    password2 = serializers.CharField(default='1234', help_text='確認密碼')
    state = serializers.BooleanField(default=True, help_text='是否啟用')
    company_name = serializers.CharField(default='元宏創新服務股份有限公司', help_text='公司名稱')
    company_id = serializers.CharField(default='54167553', help_text='統編')
    contact_person = serializers.CharField(default='dennis', help_text='聯絡人')
    phone = serializers.CharField(default='0987654321', help_text='電話')

class GetCompanyInfoSerializer(serializers.Serializer):
    account = serializers.CharField(default='dennis', help_text='公司帳號')

class GetUserListSerializer(serializers.Serializer):
    company_account = serializers.CharField(default='dennis1', help_text='帳號')

class AddUserSerializer(serializers.Serializer):
    account = serializers.CharField(default='dennis99', help_text='帳號')
    password = serializers.CharField(default='1234', help_text='密碼')
    password2 = serializers.CharField(default='1234', help_text='確認密碼')
    sip_ext = serializers.CharField(default='08', help_text='使用分機')
    sip_id = serializers.CharField(default='5678', help_text='呼叫中心系统 id')
    sip_pwd = serializers.CharField(default='1234', help_text='呼叫中心系统 pwd')
    name = serializers.CharField(default='一陣風', help_text='名稱')
    phone = serializers.CharField(default='0987654321', help_text='電話')

class ModifyUserSerializer(serializers.Serializer):
    account = serializers.CharField(default='dennis99', help_text='帳號')
    password = serializers.CharField(default='1234', help_text='密碼')
    password2 = serializers.CharField(default='1234', help_text='確認密碼')
    sip_ext = serializers.CharField(default='08', help_text='使用分機')
    sip_id = serializers.CharField(default='5678', help_text='呼叫中心系统 id')
    sip_pwd = serializers.CharField(default='1234', help_text='呼叫中心系统 pwd')
    name = serializers.CharField(default='一陣風', help_text='名稱')
    phone = serializers.CharField(default='0987654321', help_text='電話')
    delete = serializers.BooleanField(default=False, help_text='是否刪除')
