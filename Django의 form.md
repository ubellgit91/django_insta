# Django의 form

## form이란

Http의 Request로 사용자가 서버에게 처리를 요청해오는 데이터를 처리하는 양식이라고 보면 된다.

처리를 원하는 `<form>`이라는 태그 안에 담겨서 서버로 보내져 온다. 데이터는 form태그 안에 있는 것을 한번에 묶어서 보내지며, 보내는 전송 방식에는 GET, POST가 있다.

form 태그 안에 보내고자 하는 데이터를 받는 input태그를 작성하고, 

submit을 통해 서버로 전송하는 것이다.

### 폼 태그 속성

폼 태그 속성에는 name, action, method, target 등이 있습니다. 폼 속성을 이용하여 전송할 때 어디로 보내야 하는지 그리고 어떤 방법으로 보낼지 정합니다. 폼 태그 속성은 다음과 같습니다.

- action : 폼을 전송할 서버의 url주소를 지정한다.
- name : 폼을 식별하기 위한 이름을 지정한다. name속성의 값이 해당 input의 이름이 된다. 보통 name속성값이랑 맵핑하고자 하는 model의 필드명이랑 동일하게 한다. 
- accept-charset : 폼 전송에 사용할 문자 인코딩을 지정.
- target : action에서 지정한 스크립트 파일을 현재 창이 아닌 다른 위치에 열도록 지정
- method : 폼을 서버에 전송할 http 메소드를 정한다. (GET 또는 POST)

아래 소스와 같이 폼 태그 속성을 지정할 수 있다.

```html
<html>  
    <head>
    </head>

    <body>
        <form action = "http://localhost:8080/form.jsp" accept-charset="utf-8" 
              name = "person_info" method = "get"> 

        </form>
    </body>
<html>  
```

전송할 http 메소드 종류인 GET과 POST는 브라우저에서 폼 데이터를 가져와 서버로 보내는 똑같은 기능을 수행하지만, 방식은 다릅니다. 

> 참조 https://hongsii.github.io/2017/08/02/what-is-the-difference-get-and-post/

#### GET

GET은 URL의 끝에 `?`가 붙고 서버로 요청하고자 하는 파라미터가 이름과 값으로 쌍을 이루어 붙게 됩니다. 파라미터가 여러 개일 경우에는 `&`로 구분합니다. (쿼리스트링)
 GET을 사용할 경우 다음과 같이 URL이 나타나게 됩니다.

> [www.tseturl.com/get_test?name1=value1&name2=value2](http://www.tseturl.com/get_test?name1=value1&name2=value2)

GET의 특징은 다음과 같습니다.

- URL에 요청 파라미터를 붙여서 전송.
- URL로 파라미터를 전송하기 때문에 대용량 데이터를 전송하기 힘듦.
- 요청 파라미터를 사용자가 쉽게 눈으로 확인할 수 있음.

HTTP/1.1 스펙인 [RFC2616의 Section9.3](https://tools.ietf.org/html/rfc2616#section-9.3)의 GET메소드 설명에 따르면 

GET은 **정보를 조회하기 위한 메소드**라고 되어있습니다. 

정보 조회를 위한 메소드이기 때문에 GET을 사용하여 서버로 요청하여 응답을 받게 되면, 브라우저에서 해당 요청에 대한 응답을 캐시 하므로 사용자의 불필요한 네트워크 이용을 줄여서 빠르게 조회할 수 있게 해줍니다. 

#### POST

POST는 **서버로 데이터를 전송하기 위해 설계**되었기 때문에 GET과 달리 파라미터가 URL로 넘어가지 않고 **HTTP 패킷의 Body에 담아서 파라미터를 전송**합니다. 

Body에 담아서 서버에게 요청하므로 전송하는 길이에 제한 없이 대용량 데이터를 전송하는데 적합합니다. 

POST로 요청할 때, Request header의 Content-Type에 해당 데이터 타입이 표현되며, 전송하고자 하는 데이터 타입을 적어주어야 합니다. 타입을 적어주지 않는다면 서버에서 내용이나 URI의 이름의 확장명등으로 타입을 유추하거나 알 수 없는 경우에는 `application/octet-stream`로 처리합니다. 

데이터가 Body로 전송되기 때문에 GET보다 보안적인 면에서 안전하다고 할 수 있으나, 

POST도 Fiddler와 같은 툴로 **확인이 가능하기 때문에 반드시 암호화하여 전송하여야 합니다.** 

> 개발자도구에서도 손쉽게 form의 내용을 확인할 수 있으므로 보안상 사실상 차이는 없다고 봐야한다.

## Django에서의 form

Form은 이름에서 드러나듯이 입력 양식(form)을 다루는 기능입니다. “입력 양식”이란 Django가 웹 프레임워크이니 웹 입력 양식을 뜻합니다. 
Django Form은 HTML로 만든 웹 화면의 form 태그에서 서버로 전달된 항목이 유효한 지 검증(validation)할 뿐만 아니라
웹 입력 항목에 필요한 HTML 태그를 생성해 출력합니다. 
유효하지 않은 항목이 있으면 어떻게 유효하지 않은 지 안내말을 출력하기도 합니다. 

즉 form 으로 전송된 값들이 모델의 필드값에 맞는 값인지 유효성검사를 알아서 해준다.

물론 어디까지나 유효성을 검사하는 것이므로 제가 앞서 언급한 보안성에 대해 무결하지는 않습니다. 
예를 들어, Django Form의 ImageField 폼 필드는 클라이언트가 제출한 파일이 이미지 파일로 유효한지 확인하는 방법을 Image Library인 PIL이나 Pillow의 verify()에 의존합니다. verify() 메서드는 파일의 헤더 영역을 읽어 들여서 유효한 파일인지 검사할 뿐입니다. 그 마저도 일부 파일에 대해서만 제공하여, GIF 파일을 처리하는 모듈엔 verify()가 아예 없습니다. GIF, PNG, Jpeg과 같은 이미지 파일은 일반 문자열을 담는 Metadata 영역(chunk)을 지원하는데, 이 요소를 악용하여 보안을 위협하는 코드를 삽입하여 서버나 클라이언트(방문자)에게 해를 끼칠 가능성이 있습니다

입력 항목이 유효한 지에 대한 필수 검사 요소는 갖추고 있으므로 Django Form을 가장 기본으로 사용하고 보안에 필요한 조치를 추가하는 것이 나을 것입니다.

즉, Django의 form은 유효성검사는 해주지만, 보안성까지는 책임지지 않는다.

## form의 종류

Django에서는 사용자 입력을 받기 위해 사용되는 텍스트박스, 드롭다운박스와 같은

 폼(Form)을 html에 렌더링하기 위해 훌륭한 방법을 제공하고 있다. 

이 방법을 사용하면 사전 검사를 통해 사용자의 입력 중 유효한 값만을 사용할 수 있는 등(유효성 검사) 반복적으로 해야하는 귀찮은 일들을 크게 줄여 준다..

Django에서 폼(Form)을 사용하는 2가지 방법

1.forms.Form 클래스를 상속받는 일반 폼(Form)

2.forms.ModelForm 클래스를 상속받는 모델 폼(Form)

어떤 폼 구현 방식이 나에게 어울리나?

사용하려는 폼의 성격이 **모델(Model)**과**얼마나** **관련**이 있고, **스타일** **등의** **커스터마이징을** **원하나** 생각해보는 것이 폼 구현 방법 결정에 큰 도움을 준다..

 

### 일반 폼(Form)

forms.Form 클래스를 상속받아 사용한다. **일일이 모델에 정의한 필드를 다 맵핑해줘야** 해 번거롭고 힘든면이 있다. 모델(model)에 정의한 값을 html로 렌더링하는 경우라면 Django는 ‘모델 폼’ 이라는 더 좋은 방법을 제공한다.

그렇다고 ‘일반 폼’이 쓸모없는 건 아니다.. 모델(model)에서 정의한 필드 외 값을 다루어야 하는 경우 일반 폼을 사용해야 한다.

이렇게 폼을 정의하고,

```python
from django import forms 

class NameForm(forms.Form):
    your_name = forms.CharField(label='Your name', max_length=100)
```

> your_name이라는 name attr로 넘어온 form과 맵핑된다.



이렇게 뷰에서 불러다 쓴다.

```python
from django.shortcuts import render

from django.http import HttpResponseRedirect

 

from .forms import NameForm


def get_name(request):

    \# if this is a POST request we need to process the form data
    if request.method == 'POST':
        \# create a form instance and populate it with data from the request:
        form = NameForm(request.POST)
        \# check whether it's valid:
        if form.is_valid():
            \# process the data in form.cleaned_data as required
            \# ...
            \# redirect to a new URL:
            return HttpResponseRedirect('/thanks/')

     \# if a GET (or any other method) we'll create a blank form
    else:
        form = NameForm()
    return render(request, 'name.html', {'form': form})
   
```

forms.Form 클래스를 상속받아 작성된 Form클래스들은 내부에 is_valid()라는 메소드를 가지고 있는데, 이 메소드는 request로 부터 넘겨받은 form의 유효성을 검사해주는 메소드이다.

즉

`form = NameForm(request.POST)` 이렇게 Post로 받은 값을 Form의 생성자로 넘겨서 객체를 만들면, 내부에서 POST로 넘겨받은 정보를 Form클래스 내부에 정의한 필드와 맵핑시킨다. 

이후 ,

`is_vaili()`를 이용하면 넘겨받은 폼의 타입과 Form클래스에 정의된 필드에 타입이 일치하는지 유효성 검사를 한다. 틀리게되면 에러메세지를 반환한다.

### 모델 폼(ModelForm)

forms.ModelForm을 상속받아 사용한다. 

모델(model)에 정의한 필드만 html로 렌더링한다면 이 방법을 쓰는게 좋다. 

아래와 같이 폼 클래스를 정의할 때 메타(Meta) 클래스의 속성만 지정해주면 나머진 Django가 다 알아서 해준다. 

```python
from django.forms import ModelForm

 

class AuthorForm(ModelForm):

    class Meta:
        model = Author
        fields = '__all__'
```

ModelForm을 상속받은 form 클래스이다. 

내부클래스 Meta 클래스에 model 필드를 선언하고, request로 부터 넘겨받은 form의 필드와 맵핑시키고자 하는 model을 대입시켜준다. 

model만 선언하면 form에서 넘겨받은 모든 필드의 name 값을 기준으로 일치하는 model의 필드와 자동으로 맵핑되며, 

특정 필드만 맵핑시키고자 할 때에는 fields 속성을 선언하고 맵핑시키고자 하는 필드를 대입시켜 준다.

### 모델 폼을 더 쉽게 만들자. 팩토리 함수!

Django에서는 이런 모델 폼을 더 쉽게 생성할 수 있도록 팩토리(Factory)함수를 제공합니다. GoF(Gang of Four)의 디자인패턴(Design pattern)에서 등장하는 그것 맞습니다. : ) 아래와 같이 modelform_factory 함수 한줄만 호출하면 ‘모델 폼’이 만들어집니다.

```python
from django.forms import modelform_factory

from myapp.models import Book


BookForm = modelform_factory(Book, fields=("author", "title"))

이렇게 widgets 속성을 이용해 상세 설정을 해줄 수도 있습니다.

from django.forms import Textarea

Form = modelform_factory(Book, form=BookForm,
                         widgets={"title": Textarea()})
```

> 사용 해보질 않아서 잘 모르겠음.

### 폼(Form) 사용의 끝판왕, 제네릭 뷰(Generic view)

지금까지 폼을 사용할 때 모델과 연관이 있는지, 없는지에 따라 ‘일반 폼’과 ‘모델 폼’을 사용으로 나눠봤고, 팩토리 함수를 통해 더 쉽게 ‘모델 폼’을 만드는 것도 알아봤다. 

Django는 한 발 더 나아가 제네릭 뷰를 이용해 폼을 다룰 수 있게 해두었다. 

가만히 보니 사람들이 모델(Model)과 관련된 폼(Form)을 뷰(View)를 통해 html 렌더링하는 경우가 많더라는 것. 

아래 예제를 잘 보면 CreateView, UpdateView, DeleteView를 임포트하여 상속 후, 별도의 폼(Form) 클래스를 만들지 않고 뷰(View)에서 바로 필요한 속성만 딱 지정해준 것을 볼 수 있다.

```python
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from myapp.models import Author

 

class AuthorCreate(CreateView):
    model = Author
    fields = ['name']

 

class AuthorUpdate(UpdateView):
    model = Author
    fields = ['name']

 

class AuthorDelete(DeleteView):
    model = Author
    success_url = reverse_lazy('author-list')

 
```

view에서 form이 해주는 request받은 form과 model의 맵핑처리를 한번에 해주는 것이다.

CreateView는 Model객체(row)를 생성하기 위해, 요청받은 form을 model과 맵핑시켜주는 역할을 하고, 

updateView는 수정, deleteView는 삭제를 위한 Model과 form의 맵핑을 view에서 처리해준다고 보면 된다.



## ModelForm 생성, 활용 예제

Django 폼 (Form)
Django 프레임워크는 Model 클래스로부터 폼(Form)을 자동으로 생성하는 기능을 제공하고 있다. 
**즉, Model 클래스에 정의된 칼럼(필드)를 기반으로 해당 컬럼에 들어갈 값을 넣을 수 있는 폼을 자동으로 만들어준다.**
모델 클래스로부터 폼 클래스를 만들기 위해서는,
(1) django.forms.ModelForm 클래스으로부터 파생된 사용자 폼 클래스를 정의한다.
(2) 사용자 폼 클래스 안에 Meta 클래스 (Inner 클래스)를 정의하고 Meta 클래스 안 model 속성(attribute)에 해당 모델 클래스를 지정한다. 
**즉, 어떤 모델을 기반으로 폼을 작성할 것인지를 Meta.model 에 지정하는 것**이다.

앞에서 정의하였지만, 다시 한번 Model 클래스를 살펴보면 다음과 같다. 

```python
(./feedback/models.py)

from django.db import models

class Feedback(models.Model):
     name = models.CharField(max_length=100)
     email = models.EmailField()
     comment = models.TextField(null=True)
     createDate = models.DateTimeField(auto_now_add=True)
```



위의 **Feedback 모델 클래스에 기반하여** 폼 클래스를 만들기 위해

 ./feedback/forms.py 를 만들고 아래와 같이 폼 클래스 "FeedbackFrom"를 정의한다. 
FeedbackFrom 클래스는 ModelForm로부터 파생된 클래스이며, 

**Meta 안의 model 속성에 "models.Feedback" 모델 클래스를 지정**하였다. 
**fields는 모델 클래스의 필드들 중 일부만 폼 클래스에서 사용하고자 할 때 지정하는 옵션**으로, 여기서는 createDate를 뺀 나머지 필드들만 사용하도록 정의하였다.
Feedback 모델에는 name,email,comment,createDate 네가지 필드가 있다. id는 따로 지정 안하면 자동생성됨.
ModelForm 생성기능으로 이 필드 중 폼이 필요한 필드만 fields = [ ] 속성을 이용해 폼을 만든다..

```python
# forms.py
from django.forms import ModelForm
from .models import Feedback

class FeedbackForm(ModelForm):
    class Meta:
        model = Feedback # 해당 Model에 맵핑되는 form을 생성함.
        fields = ['id', 'name','email','comment']
```


이렇게 사용자 폼이 정의되었으면, View와 템플릿에서 이 폼을 사용하게 된다. 아래는 ./feedback/views.py 에 추가된 함수로서 새로운 Feedback 데이타를 추가하기 위한 폼을 핸들링하는 함수이다.

```python
# views.py
from django.shortcuts import render, redirect
from .models import *
from .forms import FeedbackForm

def create(request):
    if request.method=='POST':
        form = FeedbackForm(request.POST) # request.POST로 받아온 form 정보를 Form 클래스에 넘겨서 name값과 일치하는 필드명이 있으면 서로 맵핑시킴.
        if form.is_valid():
            form.save() # form에 있는 save()로 Model(row)를 DB에 등록시킨다.
            return redirect('/feedback/list')
    else:
        form = FeedbackForm() # post방식으로 해당 view에 접근한게 아니면(즉 get방식으로 접근했다면), 빈 Form객체를 만들어서 템플릿으로 전송함.
    return render(request, 'feedback.html', {'form': form})
```

위의 함수는 크게 두 부분으로 나눌 수 있는데, 

(1) 데이타를 입력 받는 폼을 보여 주는 부분과 

(2) 사용자가 데이타를 입력하여 저장버튼을 눌렀을 때 이를 DB에 저장하는 부분이다.
우선 데이타를 입력 받는 폼은 POST 가 아닌 부분(즉 else 부분)과 마지막 render 부분으로 입력 부분만 발췌하면 아래과 같다. render()의 첫번째 파라미터는 request를 지정하고, 두번째는 사용할 템플릿 파일을 지정하며, 세번째 파라미터는 템플릿에 전달한 데이타 혹은 객체들을 (흔히 컨텍스트라고 함) 지정한다. 

컨텍스트는 Dictionary로 전달하는데, 여기서는 "form" 이라는 키에 FeedbackFrom() **빈 객체**값을 할당하여 전달하고 있다.

```python
def create(request):
    form = FeedbackForm()
    return render(request, 'feedback.html', {'form': form})
```

위에서 호출하는 템플릿 (./feedback/templates/feedback.html) 예제를 살펴보면 아래와 같다. 
아래 템플릿에서 주목할 부분은 **View 에서 전달한 "form" 객체를 템플릿 변수로 사용하고 있는 부분**이다. 

**Form클래스를 상속받아 만들어진 비어있는 Form의 객체는 템플릿으로 넘겨지면,**

**탬플릿 출력문{{}}을 통해서 해당 폼 필드에 들어가는 값을 받을 수 있는 form, input양식을 html태그 형식으로 자동 구현을 해준다.**!!!! 

아래 예제에선 **{{ form.as_p }} 와 같이 폼을 <p> HTML 태그를 사용**하여 랜더링하도록 하고 있다
 (form.as_p는 폼의 각 필드를 p 태그 안에서 레이블과 텍스트로 배치한다). 
폼을 랜더링하는 옵션으로 form, form.as_p, form.as_table, form.as_ul 등이 있는데, 이 옵션은 각 필드를 어떤 HTML 태그로 Wrapping 할 것인가를 지정하는 것이다.

as_p는 `<p>`태그 형식으로 랩핑하는 것이고 table은 table태그 형식으로 ...그런 식이다.



```html
{% extends "base.html" %}

{% block content %}
    <p>
        <a href="{% url 'list' %}">Goto Feedback List</a>
     </p>
<div>
    <form method="POST">
        {% csrf_token %}
        {{ form.as_p }}
        <button type="submit">저장</button>
    </form>
       </div>
    {% endblock content %}
```

위의 템플릿에서 한가지 더 언급할 만한 점은 

HTML FORM 안에 {% csrf_token %} 를 넣어 준 것이다.

**CSRF (Cross Site Request Forgeries)는 웹 해킹 기법의 하나로 Django는 이를 방지하기 위한 기능을 기본적으로 제공하고 있다.** 

**Django에서 HTTP POST, PUT, DELETE을 할 경우 이 태그를 넣어 주어야 한다.**

그러면 마지막으로 사용자가 데이타를 입력하고 저장 버튼을 눌렀을 때, 데이타를 저장하는 부분을 살펴보자.

form 안의 데이터들(input)을 채우고, 저장 (submit)으로 서버로 전송하면 전송방식(method)에 따라서 서버로 form이 전송된다.

위의 views.py 에 있는 코드 중 request.method 가 POST 인 부분이 저장부분에 해당된다. 

아래 부분 발췌된 코드르 보면, 저장 버튼이 눌려저 HTTP POST가 전달되면, 사용자 정의 폼 FeedbackFrom() 생성자의 파라미터로 POST body 데이타를 패스하여 폼 객체를 생성한다. 

> (주: request.POST는 Dictionary로서 포스트된 데이타를 갖고 있다)

이 시점에 이 FeedbackFrom 객체는 POST로부터 전달된 데이타를 객체의 필드에 갖게 된다. 

이어 is_valid() 매서드를 사용하여 POST 데이타에 잘못된 데이타가 전달되었는지를 체크하고, 만약 정상이면 save() 메서드를 호출하여 DB에 데이타를 저장한다. 저장후 여기서는 list 뷰 (다음 아티클 참조)로 이동하도록 코딩하였다.

```python
def create(request):
    if request.method=='POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('/feedback/list')
    #.....
```



## form 내부에 정의되어 있는 기본 메소드

폼에 검사할 데이터를 전달하여 초기화하여 인스턴스 객체(form)에는 전달된 데이터를 검사하는 몇 가지 인스턴스 메서드를 제공합니다. full_clean()나 clean() 메서드가 폼 데이터를 검사하는 데 사용하는 메서드인데, 실제로는 is_valid() 메서드를 사용하면 됩니다. is_valid() 메서드는 폼에 전달된 데이터를 폼 필드를 기준으로 검사하여 모든 데이터가 유효하면 True를, 하나라도 유효하지 않은 항목이 있으면 False를 반환합니다. 동작은 다음과 같습니다.

`is_valid()` : 폼 검사와 관련된 오류(error)가 있는 지 검사.
`full_clean()` : _clean_fields(), _clean_form(), _post_clean() 메서드를 차례대로 수행하여 폼 데이터 유효성을 검사.
최종 : is_valid()는 오류(errors)가 없으면 True를 반환하고, 있으면 데이터가 유효하지 않아 False를 반환하며, 어떤 항목에 문제가 유효하지 않은 지 여부는 폼 인스턴스 객체의 errors 멤버(프로퍼티)에 사전형 객체처럼 생긴 ErrorDict의 인스턴스 객체로 할당.
데이터가 모두 유효하면 PhotoForm 폼의 인스턴스 객체인 form의 save() 메서드를 실행하고, 이 메서드는 연결된 모델을 이용하여 데이터를 저장합니다. save() 메서드는 ModelForm 클래스에 있는 메서드인데, 모델 폼에 연결한 모델을 이용하여 데이터를 저장하고 저장한 모델의 인스턴스 객체를 반환합니다. PhotoForm에 Photo 모델을 연결하였으므로 Photo 모델로 생성한 인스턴스 객체를 반환하는 셈이지요.



## form에서 파일정보가 request로 전송될 때

PhotoForm(request.POST, request.FILES)

PhotoForm 폼에 첫 번째 인자로 request.POST를, 두 번째 인자로 request.FILES를 전달합니다. 
첫 번째 인자는 폼에서 다룰 데이터를 뜻하며, 사전형(dict) 객체나 사전형 객체처럼 동작하는(비슷한 인터페이스를 제공하는) 객체4여야 합니다. 
파일을 제외한 HTML Form에서 POST 방식으로 전송해온 모든 formdata 데이터가 request.POST에 있습니다. 
**파일은 request.FILES**에 있습니다. 그래서, 이 둘을 분리하여 첫 번째 인자, 두 번째 인자로 전달한 것입니다.

  if request.method == "POST":
​        form.is_bound = True
​        form.data = request.POST
​        form.files = request.FILES

이런 식으로 짜도 되긴 하지만 의미없는 짓이므로 하지말자.
이렇게 하려면
is_bound = True로 해야 함 



## cleaned_data

**.is_valid() 를 통해서 검증에 통과한 값은 cleaned_data 변수명으로 사전타입 으로 제공된다.**

```python


def post_new(request):
	if request.method == 'POST':
		form = PostForm(request.POST, request.FILES) # NOTE: 인자 순서주의 POST, FILES
		if form.is_valid():
			print(form.cleaned_data) # {'title': '테스트', 'content': '내용'}

```

request.POST['key'] 이렇게 하면, POST로 보내온 name의 값이 key가 되어서 key값을 호출해서 해당 input의 값을 확인할 수 있다. 하지만 이건 form의 유효성 검사를 통과하지 않은 값이기 때문에, 맵핑된 model의 필드와 일치하는지 유효성 검사가 되지 않은 값이라서 반려될 수 있다. 

그렇기 때문에 form.cleaned_data['key']를 쓴다.

form의 유효성검사 is_valid()를 통과하고 나면, model의 필드명이 key, 넘겨받은 input값이 value가 되어서 cleaned_data라는 변수에 딕셔너리 형태로 저장된다.

> request.POST 데이터는 form instance의 초기 데이터
> 따라서 form clean 함수 등을 통해 변경될 가능성이 있음

myapp/forms.py

class CommentForm(forms.Form):
​	def clean_message(self): # Form 클래스 내 clean 멤버함수를 통해 값 변경이 가능
​		return self.cleaned_data.get('message', '').strip() # 좌우 공백 제거

myapp/views.py

#### BAD Case!! - request.POST를 통한 접근

```python
form = CommentForm(request.POST)
if form.is_valid():
	# request.POST : 폼 인스턴스 초기 데이터
	message = request.POST['message']
	comment = Comment(message=message)
	comment.save()
	return redirect(post)
```

request로 넘겨받은 form의 input값을 유효성 체크도 하지않고 그대로 갖다 쓰는 꼴이다.

뭐가 문제냐면, 나중에 해당 값을 model을 통해 DB에 저장할 때, input으로 받은 값과 model에서 요구하는 필드의 타입이 일치하지 않아서 값이 들어가지 않을 수 있다.



#### GOOD Case!! - form.cleaned_data를 통한 접근

```python
form = CommentForm(request.POST)
if form.is_valid():
#form.cleaned_data : 폼 인스턴스 내에서 clean 함수를 통해 변환되었을 수도 있을 데이터
	message = form.cleaned_data['message']
    comment = Comment(message=message)
	comment.save()
	return redirect(post)
```

POST데이터를 담고있을 FORM 객체를 만들고, POST의 input값들과 맵핑될 모델의 필드 타입이 일치하는지 is_valid()로 유효성 검사를 한다.

유효성 검사를 통과한 값은 model의 field명이 key, 들어갈 input값이 value가 된다

그 값들은 모여서 cleaned_data 라는 변수에 딕셔너리 형태로 담긴다. 

즉, cleaned_data는 유효성 검사를 통과해서 DB에 들어가도 되는 검증된 데이터라는 뜻이다. 그러므로 유효성검사 후, cleaned_data를 쓰는 것을 습관화 하자.



### 예제

```python

```

데이터의 유효성 검증과 관련된 로직은 전부 Form을 상속받은 클래스에서 처리하도록 해야한다.

검증이 끝났을 경우, 유효성 검증에 통과한 데이터는 cleaned_data속성에 추가된다.

