from django.conf.urls import url
from django.urls import path

from . import views

# 해당 app의 url용 네임스페이스를 지정해준다..
app_name='photo'

urlpatterns = [
    path('', views.PostListView.as_view(), name='list'), # 함수를 호출한게 아니라 함수 자체를 가져옴. 파이썬은 함수나 클래스 조차도 그 자체가 객체기 때문에 가능함.
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('post/', views.post_create, name='post'),
    path('<int:pk>/delete', views.post_delete, name="delete"),
    path('<int:pk>/comment/create/', views.comment_create, name='comment_create'),
    path('<int:pk>/like-toggle/',views.post_like_toggle, name='post_like_toggle'),

]