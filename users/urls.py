from django.urls import re_path

from users import views

urlpatterns = [
    #* 公司
    re_path(r'^get_company_list/$', views.GetCompanyList.as_view(), name='get_company_list'),
    re_path(r'^add_company/$', views.AddCompany.as_view(), name='add_company'),
    re_path(r'^get_company_info/$', views.GetCompanyInfo.as_view(), name='get_company_info'),
    re_path(r'^modify_company/$', views.ModifyCompany.as_view(), name='modify_company'),
    #* 使用者
    re_path(r'^get_user_list/$', views.GetUserList.as_view(), name='get_user_list'),
    re_path(r'^add_user/$', views.AddUser.as_view(), name='add_user'),
    re_path(r'^get_user_info/$', views.GetUserInfo.as_view(), name='get_user_info'),
    re_path(r'^modify_user/$', views.ModifyUser.as_view(), name='modify_user'),
    re_path(r'^get_user_ip/$', views.GetUserIp.as_view(), name='get_user_ip'),
]