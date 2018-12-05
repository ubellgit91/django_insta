"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('photo/', include('photo.urls', namespace='photo')),
    path('member/', include('member.urls', namespace='member'))
    # namespace에 이름을 붙이면, 각각의 urls모듈을 템플릿이나 뷰에서 사용할 때 같은 URL이름도 모듈별로 분리된 이름을 가질 수 있도록 해준다.

]

# django.conf.urls.static.static()함수는 첫 번째 인자로 주어진 경로(MEDIA_URL)로 요청이 올 경우, document_root에 지정된 경로에서 파일을 찾아 응답으로 보내준다.

urlpatterns += static('/upload_files/', document_root=settings.MEDIA_ROOT)
