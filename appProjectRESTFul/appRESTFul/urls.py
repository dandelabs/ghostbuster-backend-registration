from django.conf.urls import url 
from appRESTFul import views

urlpatterns = [
    url(r'^api/v1/item$', views.item_list),
    url(r'^api/v1/item/(?P<pk>[0-9]+)$', views.item_detail),
    url(r'^api/v1/login$', views.login),
    url(r'^api/v1/user$', views.user_init),
]