from django.conf.urls import url 
from appRESTFul.views import item as itemView, login as loginView, machine as machineView, user as userView

urlpatterns = [
    #Item urls
    url(r'^api/v1/item$', itemView.item_list),
    url(r'^api/v1/item/(?P<pk>[0-9]+)$', itemView.item_detail),
    url(r'^api/v1/item/filter$', itemView.item_filter),
    
    #Login url
    url(r'^api/v1/login$', loginView.do_login),
    
    #Create user url
    url(r'^api/v1/user/create$', userView.user_init),
    
    #User urls
    url(r'^api/v1/user$', userView.user_list),
    url(r'^api/v1/user/(?P<pk>[0-9]+)$', userView.user_detail),
    url(r'^api/v1/user/filter$', userView.user_filter),
    
    #Machine urls
    url(r'^api/v1/machine$', machineView.machine_list),
    url(r'^api/v1/machine/(?P<pk>[0-9]+)$', machineView.machine_detail),
    url(r'^api/v1/machine/filter$', machineView.machine_filter),
]