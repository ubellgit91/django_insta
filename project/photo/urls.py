from django.conf.urls import url
from django.urls import path

from . import views

urlpatterns = [
    path('', views.hello), # 함수를 호출한게 아니라 함수 자체를 가져옴. 파이썬은 함수나 클래스 조차도 그 자체가 객체기 때문에 가능함.
    path('photos/<int:pk>', views.DetailView.as_view(), name='detail'),
]