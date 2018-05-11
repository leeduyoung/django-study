from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^areas/(?P<area>.+)/$', views.areas), # .+는 모든 문자 허용
    url(r'^polls/(?P<poll_id>\d+)/$', views.polls), # \d+ 는 숫자만 허용
]
