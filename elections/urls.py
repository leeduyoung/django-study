from django.conf.urls import url
from . import views

app_name = 'elections'
urlpatterns = [
    # url(r'^$', views.index),
    url(r'^$', views.index, name = 'home'),
    url(r'^areas/(?P<area>[가-힣]+)/$', views.areas), # .+는 모든 문자 허용, [가-힣]는 한글만 허용
    url(r'^areas/(?P<area>[가-힣]+)/results$', views.results), # .+는 모든 문자 허용
    url(r'^polls/(?P<poll_id>\d+)/$', views.polls), # \d+ 는 숫자만 허용
    url(r'^candidates/(?P<name>[가-힣]+)/$', views.candidates),
]
