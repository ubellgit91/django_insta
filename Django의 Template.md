# Django의 Template

## Django 템플릿 (Template)

Django에서의 View가 다른 MVC Framework에서의 Controller와 유사한 역활을 한다면, 

Django에서의 템플릿 (Template)은 MVC Framework에서의 View와 비슷한 역활을 한다. 템플릿 (Template)은 View로부터 전달된 데이타를 템플릿에 적용하여 Dynamic 한 웹페이지를 만드는데 사용된다.

Template은 HTML 파일로서 Django App 폴더 밑에 "templates" 라는 서브폴더를 만들고 그 안에 템플릿 파일(*.html)을 생성한다. 이는 단일 App이거나 동일 템플릿명이 없는 경우 사용할 수 있다.

하지만, Django 개발 가이드라인은 **"App폴더/templates/App명/템플릿파일" 처럼, 각 App 폴더 밑에 templates 서브폴더를 만들고 다시 그 안에 App명을 사용하여 서브폴더를 만든 후 템플릿 파일을 그 안에 넣기를 권장**한다 (예: /home/templates/home/index.html ).

이는 만약 복수의 App들이 동일한 이름의 템플릿을 가진 경우, View에서 잘못된 템플릿을 가져올 수 있기 때문인데, 예를 들어, App1에 create.html이 있고, App2에 동일한 create.html 템플릿이 있는 경우, App2의 View에서 create.html를 지정하면, 처음 App1의 create.html을 사용하게 된다. 이는 템플릿을 찾을 때 자신의 App 내의 템플릿을 먼저 찾는 것이 아니라, 전체 App들의 템플릿 폴더들을 처음부터 순서대로 찾기 때문이다. View에서 "App2/create.html" 과 같이 템플릿명을 지정하면 이런 혼동은 없어진다.

## 템플릿 사용하기

템플릿은 물론 순수하게 HTML로만 쓰여진 Static HTML 파일일 수는 있지만, 거의 대부분의 경우 View로부터 어떤 데이타를 전달받아 HTML 템플릿 안에 그 데이타를 동적으로 치환해서 사용한다. 예를 들어, 위의 index 뷰에서 message 라는 데이타를 index.html 이라는 템블릿에 전달하고 그 템플릿 안에서 이를 사용하기 위해서 다음과 같이 할 수 있다.

(1) 먼저 View (home/views.py)에서 다음과 같이 index()를 정의한다. 여기서 render는 django.shortcuts 패키지에 있는 함수로서 첫번째 파라미터로 request를, 그리고 두번째 파라미터로 템플릿을 받아들인다. 여기서 템플릿은 index.html으로 지정되어 있는데, 이는 home/templates/index.html을 가리키게 된다. 세번째 파라미터는 Optional 인데, View에서 템플릿에 **전달한 데이타를 Dictionary로 전달**한다. Dictionary의 Key는 템플릿에서 사용할 키(or 변수명)이고, Value는 전달하는 데이타의 내용을 담는다. 여기서는 message 라는 키로 "My Message"라는 문자열을 전달하고 있다.

Views.py

```python
from django.shortcuts import render

def index(request):
    msg = 'My Message'
    return render(request, 'index.html', {'message': msg})
# templates로 보낼 context는 딕셔너리 형태로 보낸다.
```


다음으로 Template (home/templates/index.html)에 HTML 문서를 작성한다.

여기서 body 태그 안에 message를 보면 {{ }} 으로 둘러싸인 것을 볼 수 있는데, Django의 템플릿에서 {{ 변수명 }} 은 해당 변수의 값을 그 자리에 치환하라는 의미를 갖는다. 

즉 {{}} 템플릿태그는 단순 **출력문** 이라고 볼 수 있다.

 Django Template은 또한 View로 부터 전달된 다양한 데이타들을 템플릿에 편리하게 넣을 수 있도록 여러 템플릿 태크( {% 탬플릿태그 %} 와 같은 형태, 아래 참조)들을 제공하고 있다.

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
    <h1>{{message}}</h1> # Views에서 템플릿으로 넘겨받은 message를 출력한다.
</body>
</html>
```

템플릿 셋팅
Django에서는 여러 템플릿 엔진을 선택하여 사용할 수 있으며, 이 셋팅은 Django 프로젝트의 settings.py 에서 할 수 있다. 디폴트 Django 템플릿 엔진을 사용하기 위해서는 settings.py 파일의 TEMPLATES 섹션에서 BACKEND를 django.template.backends.django.DjangoTemplates 로 설정한다 (기본으로 설정되어 있다).

## Django 템플릿 언어

Django 템플릿에서 사용하는 특별한 태크 및 문법을 Django 템플릿 언어 (Django Template Language)라 부른다. 템플릿 언어는 크게 템플릿 변수, 템플릿 태크, 템플릿 필터, 코멘트 등으로 나눌 수 있다.

템플릿 변수 (출력용)
템플릿 변수는 {{ 와 }} 으로 둘러 싸여 있는 변수로서 그 변수의 값이 해당 위치에 치환된다. 변수에는 Primitive 데이타를 갖는 변수 혹은 객체의 속성 등을 넣을 수 있다.

```python
<h4>
  Name : {{ name }}
  Type : {{ vip.key }}
</h4>
```

템플릿 태그
템플릿 태크는 {% 와 %} 으로 둘러 싸여 있는데**, 이 태크 안에는 if, for 루프 같은 Flow Control 문장에서부터 웹 컨트롤 처럼 내부 처리 결과를 직접 덤프하는 등등 여러 용도로 쓰일 수 있다**. 다양한 태크에 대한 자세한 설명은 Built-in Template Tag 를 참조하면 된다. 아래 처음 부분은 if 와 for 태크를 사용한 예이고, 마지막은 CSRF 해킹 공격에 대응하여 토큰을 넣어주는 csrf_token 태그를 사용한 예이다.

```pyton
{% if count > 0 %}
    Data Count = {{ count }}
{% else %}
    No Data
{% endif %}

{% for item in dataList %}
  <li>{{ item.name }}</li>
{% endfor %}

{% csrf_token %}
```

템플릿 필터 ( | )
템플릿 필터는 변수의 값을 특정한 포맷으로 변형하는 기능을 한다. 예를 들어, 날짜를 특정 날짜 포맷으로 변경하거나 문자열을 대소문자로 변경하는 일등을 할 수 있다.

```html
날짜 포맷 지정
{{ createDate|date:"Y-m-d" }}

소문자로 변경
{{ lastName|lower }}
```

코멘트
템플릿에서 코멘트를 넣는 방법은 크게 2가지이다. 한 라인에 코멘트를 적용할 때는 코멘트를 {# 과 #} 으로 둘러싸면 된다. 또한, 복수 라인 문장을 코멘트할 경우는 문장들을 {% comment %} 태그와 {% endcomment %}로 둘러싸면 된다.

```html
{# 1 라인 코멘트 #}

{% comment %}  

  <div>
      <p>
          불필요한 블럭
      </p>
      <span></span>
  </div>

{% endcomment %}
```


HTML Escape
HTML 내용 중에 <, >, ', ", & 등과 같은 문자들이 있을 경우 이를 그 문자에 상응하는 HTML Entity로 변환해 주어야 하는데, Django 템플릿에서 이러한 작업을 자동으로 처리해 주기 위해 {% autoescape on %} 템플릿 태그나 escape 라는 필터를 사용한다.

예를 들어, 아래 예제에서 content 라는 변수에 인용부호가 들어 있다고 했을 때, 아래와 같이 autoescape 태그나 escape 필터를 사용해서 자동으로 변환하게 할 수 있다. 만약 이러한 변환을 하지 않으면 HTML이 중간에 깨지게 된다.

```html


{% autoescape on %}     # autoescape 태그
	{{ content }}
{% endautoescape %}

{{ content|escape }}    # escape 필터
```



만약 이러한 HTML escape 혹은 HTML 인코딩 기능을 사용하지 않고, <, >, ', ", & 이 들어간 문자열을 HTML에서 사용하고자 한다면, 각 문자를 HTML Entity로 미리 변환해 주어야 한다. 이러한 변환을 보다 편리하게 하는 한 방법으로 온라인 HTML 인코딩 변환 도구를 사용할 수 있다.

## 템플릿 확장

템플릿 확장
웹사이트를 개발하다 보면 모든 (혹은 많은) 웹 페이지마다 공통적으로 들어가는 HTML 코드가 있음을 알게 된다. 각 웹페이지마다 공통 코드를 중복해서 넣어 주는 것은 효율적이지 않다. Django 에서는 이러한 공통 부분을 기본 템플릿(Base Template)으로 만들고, 각 웹페이지 마다 변경이 필요한 부분만 코드를 작성하게 하는 템플릿 확장(Template Extension) 기능을 제공한다 (템플릿 확장은 또한 템플릿 상속(Template Inheritance)이라고도 불리운다).

Base 템플릿을 어디에 만드는가는 개발자가 템플릿을 어떻게 체계화하는가의 문제이다. 여기서는 모든 Django App에 공통적으로 적용되는 Base 템플릿을 (manage.py가 있는) Base Directory 밑의 templates 라는 서브 폴더에 만들어 보자. 즉 ./templates/base.html 이라는 Base 템플릿을 만들었는데, 이 파일 안에 각 웹페이지에서 변경 혹은 삽입할 영역을 {% block 블럭명 %} 으로 지정한다. 여기서는 블럭명을 content로 정하여 {% block content %} 으로 표시하였다.


Base 템플릿을 사용(확장)하는 각 Django App의 템플릿들은 각 App 폴더의 templates 폴더에 저장한다. 예를 들어, ./home/templates/index.html에서 base.html을 확장해서 사용한다고 가정해 보자. Base 템플릿을 사용(확장)하는 템플릿 (예: home/templates/index.html)은 아래와 같이 먼저 {% extends %} 확장 템플릿 태그를 사용하여 어떤 Base 템플릿을 사용하는지 지정해 주어야 한다. 이 extends 태그는 항상 템플릿의 처음에 와야 한다. 다음으로 {% block %} 블럭에 삽입하고자 하는 웹 페이지 내용을 작성한다. 아래 예에서는 간단히 h1 태그를 추가하였다. 만약 Base 템플릿에 여러 {% block %} 블럭이 있다면, 확장 템플릿에서 각 블럭의 이름별로 여러 블럭들을 추가할 수 있다.

```html
{% extends "base.html" %}

{% block content %}
   <h1>{{message}}</h1>
{% endblock content %}
```

위의 Base 템플릿이 제대로 동작하기 위해서는 아래에서 설명할 템플릿 위치와 관련된 셋팅을 추가해 주어야 한다.

템플릿 위치 셋팅
Django 템플릿 위치와 관련하여 두 가지 중요한 셋팅이 있는데, Django 프로젝트의 settings.py 안의 TEMPLATES 셋팅 중 DIRS 와 APP_DIRS 옵션이 그것이다.

```python
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [ os.path.join(BASE_DIR, 'templates') ],  # 추가
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
```


DIRS 옵션은 Django가 템플릿들을 찾는 디렉토리 경로를 지정하는 것으로, 원래는 비어 있었는데, 위의 같이 Base 디렉토리(BASE_DIR) 밑의 templates 폴더 경로를 추가하였다. 즉, BASE_DIR\templates 가 경로에 추가되어야만 base.html 템플릿을 찾을 수 있게 된다. 만약 DIRS에 여러 경로가 추가되면, Django는 경로 순서대로 검색하면서 템플릿을 찾게 된다.

APP_DIRS 옵션은 Django가 Django App 안의 templates 폴더에서 템플릿들을 찾을 것인지의 여부를 설정하는 것이다. 디폴트로 True가 설정되어 있어서 기본적으로 App안의 templates 폴더를 검색하여 템플릿을 찾게 된다.



## Template를 찾아 갈 수 있는 이유

photos 앱 디렉터리에 templates 디렉터리를 만들고 그곳에 템플릿 파일을 담으면 Django가 알아서 앱 디렉터리에 있는 템플릿 파일을 가져온다. 이 동작은 settings.py에 따로 설정되어 있어서 그렇다

TEMPLATES = [
​    {
​        'BACKEND': 'django.template.backends.django.DjangoTemplates',
​        'DIRS': [os.path.join(BASE_DIR, 'templates'), ],
​        'APP_DIRS': True,
​        'OPTIONS': {
​            'context_processors': [
​                'django.template.context_processors.debug',
​                'django.template.context_processors.request',
​                'django.contrib.auth.context_processors.auth',
​                'django.contrib.messages.context_processors.messages',
​            ],
​        },
​    },
]
settings.py의 TEMPLATES 항목을 보면 'APP_DIRS': True, 코드가 있는데, 
이 부분이 바로 Django 앱 별로 템플릿 파일을 다루도록 할 것인지 여부를 지정한 것이며 
앱 안에 위치하는 템플릿 디렉터리 이름은 templates로 고정되어 있습니다. False로 바꾸면 앱 디렉터리에 있는 템플릿 파일을 다루지 않는다.

