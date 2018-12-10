# static파일

## 종류

Django은 정적 파일을 크게 두 종류로 구분합니다.

**Static file은** Javascript, CSS, Image 파일처럼 웹 서비스에서 사용하려고 미리 준비해 놓은 정적 파일입니다. 파일 자체가 고정되어 있고, 서비스 중에도 수시로 추가되거나 변경되지 않고 고정되어 있습니다.

**Media file은** 이용자가 웹에서 올리는(upload) 파일입니다. 파일 자체는 고정되어 이지만, 언제 어떤 파일이 정적 파일로 제공되고 준비되는지 예측할 수 없습니다.

Static file은 서비스에 필요한 정적 파일을 미리 준비해놓기 때문에 manage.py 도구에 findstatic과 collectstatic이라는 기능으로 정적 파일을 모으고 찾는 관리 기능을 제공

그에 반해 Media file은 이용자가 웹에서 올리는 파일이므로 미리 예측해서 준비할 수 없습니다. 그래서 Static file 관련된 관리 기능인 findstatic과 collectstatic 기능을 사용하지 못합니다.

## Static 파일

웹사이트는 일반적으로 자바스크립트, CSS, 이미지 등의 파일들을 사용하는데, 이러한 파일들을 Django 에서는 **Static 파일**이라 부른다. 이러한 Static 파일들을 체계적으로 관리하기 위하여 일반적으로 Django 프로젝트 홈 디렉토리 (settings.py에서의 BASE_DIR) 밑에 "static" 이라는 서브 폴더를 만들어 그곳에 static 파일들을 넣는다. 아래 그림은 /static 폴더 안에 리소스 별 서브폴더를 만들어 static 파일들을 관리하는 예를 보여주는 것이다.

static 폴더에 파일들을 넣고 사용하기 위해서는 **settings.py 에 하나의 셋팅을 추가해 주어야 한다.** 즉, settings.py 파일에서 아래와 같이 static 파일들을 찾는 경로를 나타내는 STATICFILES_DIRS 라는 변수를 설정해야 한다. 경로가 여러 개일 수 있지만, 여기서는 BASE_DIR/static 폴더 하나를 지정하였다.

settings.py

```python
STATIC_URL = '/static/' # URL은 웹상에서 static폴더에 접근할 때 쓴다.
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'), # 실제적으로 static파일이 저장될 디렉토리경로
]
혹은
STATIC_URL = '/static/'
STATICFILES_DIRS = ( os.path.join('static'), )
```

STATIC_URL 은 url을 통해서 static파일에 접근할 때 쓰이는 url주소이다.

**실제 static파일이 적재되는 디렉토리를 지칭하는 것이 아니다.** 

STATICFILES_DIRS 에 static 파일들이 저장되어있는 경로를 지정할 수 있다.



## Django App의 Static 폴더

필요에 따라 각각의 Django App마다 **App별 정적 파일을 담는 별도의 "static" 폴더를 둘 수도 있다**. 이를 위해서는 settings.py 파일 안에 STATICFILES_FINDERS을 설정하고 그 값으로 AppDirectoriesFinder을 추가해 주어야 한다. 각 App의 static 폴더는 그 폴더명을 "static" 으로 지정해 주어야 하며, 일반적으로 App명/static/App명 과 같이 각 App의 static 폴더 안에 다시 "App명"" 서브폴더를 둘 것을 권장한다. 이는 Deployment 시 collectstatic 을 실행할 때, 각 static 폴더 밑의 내용을 그대로 복사하므로 동명 파일들이 충돌하지 않게 하기 위함이다.

settings.py

```python
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)
```

참고로 위의 FileSystemFinder는 STATICFILES_DIRS 에 있는 경로들로부터 정적 파일을 찾을 수 있게 한다.

해당 finder 모듈을 settings에 지정해줘야 static 경로 지정한 곳에서 static 파일들을 찾아낼 수 있는 모양이다. 

## Static 파일 사용

Static 파일들은 주로 템플릿에서 사용되는데, settings.py 설정을 마친 후 static 파일들을 사용하기 위해서는, 템플릿 상단에 {% load staticfiles %} 태그를 먼저 명시해 주어야 한다. 그리고, 실제 static 파일을 가리키기 위해서는 아래 link 태그에서 보이듯이 "{% static '리소스명' %}" 와 같이 static 템플릿 태그를 사용하여 해당 리소스를 지정한다. 이때 리소스명에는 "static/" 폴더명 다음의 경로만 지정한다.

```html
{% load staticfiles %}

<html lang="en">

<head>
    <link rel="stylesheet" href="{% static 'bootstrap/css/bootstrap.min.css' %}">
</head>

<body>
</body>
</html>
```

## collectstatic

Django 프로젝트를 Deploy할 때, 흩어져 있는 Static 파일들을 모아 특정 디렉토리로 옮기는 작업을 할 수 있는데, 이 작업은 위해 "./manage.py collectstatic" 명령을 사용한다. 즉, collectstatic 명령은 Django 프로젝트와 각 Django App 안에 있는 Static 파일들을 settings.py 파일 안에 정의되어 있는 STATIC_ROOT 디렉토리로 옮기는 작업을 수행한다.

예를 들어, settings.py 에 다음과 같이 STATIC_ROOT 가 설정되어 있을 때,

STATIC_ROOT = '/var/www/myweb_static'
아래 collectstatic 명령은 모든 정적 파일들을 /var/www/myweb_static 디렉토리에 복사해 준다.

(venv1) /var/www/myweb $ ./manage.py collectstatic

## static setting에 대한 것들

python manage.py findstatic static파일경로/static파일명

이렇게 하면 STATICFILES_DIRS에 설정한 경로에서 지정한 정적 파일을 찾습니다.

STATICFILES_DIRS는 settings.py에 지정함.

우선순위는 STATICFILES_DIRS에 명기된 디렉터리가 더 상위인데, 
STATICFILES_FINDERS라는 settings.py 설정 항목에서 
기본 파일 시스템 파인더(finder)가 Django App 디렉터리보다 상위순위로 지정되어 있기 때문입니다. 
즉 Root 디렉토리에서 static폴더를 찾고, 다음으로 App단위에서 static폴더를 찾는다


STATIC_URL
STATIC_URL은 웹 페이지에서 사용할 정적 파일의 최상위 URL 경로입니다. 
이 최상위 경로 자체는 실제 파일이나 디렉터리가 아니며, URL로만 존재하는 단위입니다. 
그래서 이용자 마음대로 정해도 무방

STATIC_URL = '/assets/'
문자열은 반드시 /로 끝나야 합니다. findstatic 명령어로 탐색되는 정적 파일 경로에 STATIC_URL 경로를 합치면 실제 웹에서 접근 가능한 URL이 됩니다.

findstatic js/jquery-2.1.3.min.js :
http://pystagram.com/assets/js/jquery-2.1.3.min.js


STATIC_URL은 정적 파일이 실제 위치한 경로를 참조하며, 이 실제 경로는 STATICFILES_DIRS 설정 항목에 지정된 경로가 아닌
STATIC_ROOT 설정 항목에 지정된 경로를 참조한다.

STATIC_ROOT
STATIC_ROOT는 Django 프로젝트에서 사용하는 모든 정적 파일을 한 곳에 모아넣는 경로.
한 곳에 모으는 기능은 manage.py 파일의 collectstatic 명령어로 수행
각 Django 앱 디렉터리에 있는 static 디렉터리와 STATICFILES_DIRS에 지정된 경로에 있는 모든 파일을 모읍니다.
개발 과정에선, 정확히는 settings.py의 DEBUG가 True로 설정되어 있으면 STATIC_ROOT 설정은 작용하지 않으며, STATIC_ROOT는 실 서비스 환경을 위한 설정 항목입니다. 그래서 개발 과정에선 STATIC_ROOT에 지정한 경로가 실제로 존재하지 않거나 아예 STATIC_ROOT 설정 항목 자체가 없어도 문제없이 동작함.

실 서비스 환경에서 STATIC_ROOT는 왜 필요할까요? 이 경로에 있는 모든 파일을 웹 서버가 직접 제공(serving)하기 위함입니다.
즉 서버(아파치 등 C/C+로 작성된 서버.) 서버와 웹 어플리케이션은 중간 인터페이스를 매개(wsgi 등)로 연결되어있음. 

setting.py에 
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles') 라고 지정해놓고
python manage.py collectstatic 명령어를 수행하면,
BASE_DIR 경로에 'staticfiles'라는 디렉토리가 새로 생기고 그 안에 Django앱에서 쓰이는 모든 static파일들이 모이게 됨.
이렇게 정적 파일을 모아놓은 STATIC_ROOT는 Django가 직접 접근하진 않습니다. 
Django가 접근하여 다루는 설정은 STATICFILES_DIRS이며, 
STATIC_ROOT는 정적 파일을 직접 제공(serving)할 웹 서버가 접근합니다. 즉, 서버(아파치 등)에서 쓸 정적파일들을 모으기 위한 작업임.
Django는 웹 어플리케이션 프레임워크일 뿐이고 서버가 아님. 서버에서 쓰는 static이랑 구분지어야 함.

collectstatic 명령어를 수행하면 STATICFILES_DIRS나 앱 디렉터리에 있는 static 디렉터리 안에 있는 파일을 STATIC_ROOT에 모으는데, STATICFILES_DIRS에 지정된 경로인 경우 따로 명시한 접두사으로 디렉터리를 만들어 그 안에 파일을 복사하고, 앱 디렉터리에 있는 static 디렉터리인 경우는 앱 이름으로 디렉터리를 만들어 그 안에 static 디렉터리 안에 있는 파일을 복사합니다. 즉, 개발 단계(DEBUG = True)에서는 정적 파일 URL 경로가 논리 개념이고, 서비스 환경(DEBUG = False)에서는 실제 물리 개념인 정적 파일 URL 경로가 되는 것입니다.

주의할 점. STATIC_ROOT 경로는 STATICFILES_DIRS 등록된 경로와 같은 경로가 있어서는 안 됩니다. 남들이 잘 안 쓸만한 이상한 이름(staticfiles?)을 쓰세요.



## 이용자(클라이언트)가 업로드한 static파일들.

Django는 이용자가 업로드한 파일은 MEDIA_URL과 MEDIA_ROOT라는 설정값을 참조하여 제공(serve)합니다. 

모델의 FileField 필드 클래스나 ImageField 필드 클래스로 지정하는 upload_to 인자는 MEDIA_URL과 MEDIA_ROOT 경로 아래에 위치합니다

자, 그럼 MEDIA_URL과 MEDIA_ROOT를 설정하겠습니다. pystagram 패키지(디렉터리) 안에 있는 settings.py 파일을 열고 맨 아래에 다음 두 줄을 추가합니다.

```python
# settings.py
MEDIA_URL = '/upload_files/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'uploads')
```


이번엔 models.py를 열고, image와 filtered_image 모델 필드에 지정된 upload_to를 변경합니다.

```python
class Photo(models.Model):
    image = models.ImageField(upload_to='%Y/%m/%d/orig')
    filtered_image = models.ImageField(upload_to='%Y/%m/%d/filtered')
    content = models.TextField(max_length=500, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
```

업로드된 파일은 upload_files 라는 URL을 따르므로 urls.py에도 이와 관련된 내용을 등록해야 합니다. 원리는 이렇습니다. upload_files 뒤에 나오는 경로를 받은 뒤 지정된 경로에 있는 이미지 파일을 읽어온 후 웹브라우저에 보내는 겁니다. 경로에 없으면 404 오류를 일으키고요. 아, 생각만 해도 귀찮습니다. 

다행히 Django엔 이런 걸 처리해주는 기능이 이미 있습니다. django.conf.urls.static 모듈에 있는 static 함수지요. urls.py 파일에서 기존 urlpatterns 변수 아래에, 간단히 말해 맨 아래에 다음 줄을 추가하세요.

```python

from django.conf import settings
from django.conf.urls.static import static

urlpatterns += static('upload_files', document_root=settings.MEDIA_ROOT)
```



자, 끝났습니다. 이제 다시 웹브라우저에서 개별 사진 URL로 접근해보세요. 404 오류 나던 것이 몇 가지 조치를 취하자 이미지가 잘 나오는데, 이는 정적 파일 처리와 관련된 내용이며 나중에 자세히 다루겠습니다. :)