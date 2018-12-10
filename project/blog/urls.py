from django.urls import path, include

from . import views

app_name = 'blog'

urlpatterns = [

    path('', views.PostList.as_view(), name="list"),
    path('<int:pk>/', views.PostDetail.as_view(), name="detail"),
    path('post/', views.PostInsert.as_view(), name="insert"),
    path('<int:pk>/update', views.PostUpdate.as_view(), name="update"),
    path('<int:pk>/delete', views.PostDelete.as_view(), name="update"),

]