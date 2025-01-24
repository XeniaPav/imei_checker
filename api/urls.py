from django.urls import path
from api.apps import ApiConfig
from .views import check_imei

app_name = ApiConfig.name

urlpatterns = [path("api/check-imei/", check_imei, name="check_imei")]
