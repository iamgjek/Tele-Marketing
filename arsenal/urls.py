
from django.urls import re_path

from arsenal import views



urlpatterns = [
    re_path(r'^get_infomation/$', views.GetInfomation.as_view(), name='get_infomation'),
    re_path(r'^arsenal_land_owner_input/$', views.ArsenalLandOwnerInput.as_view(), name='arsenal_land_owner_input'),
    re_path(r'^arsenal_build_owner_input/$', views.ArsenalBuildOwnerInput.as_view(), name='arsenal_build_owner_input'),
]