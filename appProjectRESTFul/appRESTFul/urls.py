from django.conf.urls import url 
from appRESTFul.views import item as itemView, login as loginView, machine as machineView, user as userView, downtime as downtimeView, downtimeTypes as downtimeTypeView, orderStatus as orderStatusView

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
    
    #Downtime urls
    url(r'^api/v1/downtime$', downtimeView.downtime_list),
    url(r'^api/v1/downtime/(?P<pk>[0-9]+)$', downtimeView.downtime_detail),
    url(r'^api/v1/downtime/filter$', downtimeView.downtime_filter),
    
    #DowntimeType urls
    url(r'^api/v1/downtimetype$', downtimeTypeView.downtimeType_list),
    url(r'^api/v1/downtimetype/(?P<pk>[0-9]+)$', downtimeTypeView.downtimeType_detail),
    
    #Orderstatus urls
    url(r'^api/v1/orderstatus$', orderStatusView.orderStatus_list),
    url(r'^api/v1/orderstatus/(?P<pk>[0-9]+)$', orderStatusView.orderStatus_detail),
]