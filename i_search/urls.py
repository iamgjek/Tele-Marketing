from django.contrib import admin
from django.urls import include, path, re_path
from drf_spectacular.views import (SpectacularAPIView, SpectacularRedocView,
                                   SpectacularSwaggerView)
from rest_framework import routers

from i_search import views, views2

urlpatterns = [
    re_path(r'^login/$', views.LoginView.as_view(), name='login'),
    re_path(r'^logout/$', views.LogoutView.as_view(), name='logout'),
    re_path(r'^telem/$', views.TelemView.as_view(), name='telem'),
    re_path(r'^get_area/$', views.GetAreaListView.as_view(), name='get_area'),
    re_path(r'^account_add/$', views.AccountAddView.as_view(), name='account_add'),
    re_path(r'^account_manage/$', views.AccountManageView.as_view(), name='account_manage'),
    re_path(r'^account_edit/$', views.AccountEditView.as_view(), name='account_edit'),
    re_path(r'^member_aclist/$', views.MemberAclistView.as_view(), name='member_aclist'),
    re_path(r'^list_download/$', views.ListDownloadView.as_view(), name='list_download'),
    re_path(r'^account_download/$', views.AccountDownloadView.as_view(), name='account_download'),
    re_path(r'^member_newac/$', views.MemberNewacView.as_view(), name='member_newac'),
    re_path(r'^member_editac/$', views.MemberEditacView.as_view(), name='member_editac'),
    re_path(r'^upload_file/$', views.UploadFileView.as_view(), name='upload_file'),
    #* API專區
    re_path(r'^get_record_info/$', views.GetRecordInfo.as_view(), name='get_record_info'),
    re_path(r'^get_tirecord/$', views.GetTirecordView.as_view(), name='get_tirecord'),
    re_path(r'^add_remark/$', views.AddRemark.as_view(), name='add_remark'),
    re_path(r'^get_logo/$', views.GetLogoView.as_view(), name='get_logo'),
    #* 製作 excel 清單
    re_path(r'^download_phone/$', views.DownloadPhoneNumberView.as_view(), name='download_phone'),
    #* 下載檔案
    re_path(r'^download/(?P<filename>.*)', views.download, name='download'),
    #* 拉電話清單
    re_path(r'^get_download_list/$', views2.GetDownloadList.as_view(), name='get_download_list'),
]