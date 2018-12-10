# Django의 View

## View란?

Django View
Django에서의 뷰(View)는 다른 일반 MVC Framework에서 말하는 Controller와 비슷한 역활을 한다 (정확히 같은 개념은 아님. 아래 MTV 패턴 참조). 즉, View는 필요한 데이타를 모델 (혹은 외부)에서 가져와서 적절히 가공하여 웹 페이지 결과를 만들도록 컨트롤하는 역활을 한다.

View들은 Django App 안의 views.py 라는 파일에 정의하게 되는데, 각 함수가 하나의 View를 정의한다. 각 View는 HTTP Request를 입력 파라미터로 받아들이고, HTTP Response를 리턴한다.

```python
from django.http import HttpResponse
 
def index(request):
    return HttpResponse("<h1>Hello, World!</h1>")
```

위의 예제는 하나의 View 함수**(함수형 뷰)**를 표현한 것인데, 이 함수는 입력으로 항상 request 를 받아들이고, response 를 리턴하게 된다. 여기서는 간단한 HTML Text를 포함한 HttpResponse() 객체를 리턴하고 있다. 일반적으로 Django 에서는 좀 더 복잡한 HTML을 처리하기 위해 뷰 템플릿(Template)을 사용한다.

## 함수형 뷰

간단하게 말해서, 함수 def 로 구성되어있는 view를 뜻한다.

파이썬에서는 함수 또한 객체이기 때문에 가능한 것으로 추정된다.

```python
from django.http import HttpResponse

def my_view(request):  
    if request.method == 'GET':
        # request가 get방식으로 접근되었을 때 
    elif request.method == 'POST':
        # post방식으로 접근되었을 때 작동
        return HttpResponse('result')
```

이런 식으로 함수로 request를 받아서 처리하는 뷰 형태이다.

딱히 특이한 점은 없지만 request method 방식 별로 내부 로직을 구현하는 데에 일일이 다 직접 구현해 줘야 한다는 단점이 있다.

### 함수형 뷰에서는 데코레이터를 사용할 수 있다.

파이썬의 기본 기능 중에 데코레이터 라는 것이 있다.

기존에 있는 함수에다가 특정 기능들을 덧붙여 주는 것인데, Django에서도 이 기능을 활용하여 여러 데코레이터들을 제공한다.

자주 쓰이는 데코레이터 중에 하나로 , 로그인, 권한관련 데코레이터가 있다.

```python
from django.contrib.auth.decorators import login_required
 
@login_required
def my_view(request):    

```

이런 식으로 어노테이션(@)을 달고 데코레이터 함수를 데코레이팅 하려는 함수 위에 정의 해주면, 해당 함수에 login_required라는 기능이 덧붙여 진 것이다. 



데코레이터에 대한 것은 아직 생소하므로 좀 더 나중에...



## 클래스형 뷰

1. 클래스로 작성되어 있는 뷰 객체를 말한다.(제네릭 뷰는 클래스형 뷰를 자주 쓰이는 특정 기능에 맞춰 세분화 해서 추상화한 뷰를 말한다)
2. 상속과 믹스인 기능 사용으로 코드의 재사용이 가능
3. 뷰의 체계적 관리
4. 제네릭 뷰 작성

**클래스형** **뷰의** **시작점**

클래스형 뷰는 URLconf에서의 사용으로 시작한다. 
 MyView 라는 클래스형 뷰를 사용한다면 URLconf의 모습은 다음과 같을 것이다.

\# urls.py

```python
from django.conf.urls import patterns  

from myapp.views import MyView

 

urlpatterns = patterns('', (r'^about/', MyView.as_view()),

)
```



클래스형 뷰는 클래스로 진입하기 위한 진입 메소드를 제공하는데, 이것이 위 예제에서의 as_view()메소드이며, 아래의 순서로 요청을 처리한다.

1. as_view() 메소드에서 클래스의 인스턴스를 생성한다.
2. 생성된 인스턴스의 dispatch() 메소드를 호출한다.
3. dispatch() 메소드는 요청을 검사해서 HTTP의 메소드(GET, POST)를 알아낸다.
4. 인스턴스 내에 해당 이름을 갖는 메소드로 요청을 중계한다.
5. 해당 메소드가 정의되어 있지 않으면, HttpResponseNotAllowd 예외를 발생시킨다.

**MyView** **클래스의** **정의**

\# views.py

```python
from django.http import HttpResponse  

from django.views.generic import View

 

class MyView(View):  
    def get(self, request): # 해당 view에 Request가 get방식으로 접근했을 시 실행됨.
       # 뷰 로직 작성
       return HttpResponse('result')
```

1. MyView 클래스는 View 클래스를 상속받는다.
2. View 클래스에는 as_view() 메소드와 dispatch() 메소드가 정의되어 있다.

### 클래스형 뷰에는 Mixin을 사용할 수 있다.

함수에 데코레이터라는 기존 함수를 수정하지 않고 기능을 덧붙이는 기능이 있었다면,

클래스에는 다중상속을 이용하여(파이썬 특징)기능을 확장, 덧붙이는 Mixin이라는 방법이 있다.

Django에서도 이를 이용해서 클래스형 뷰에서 사용할 수 있는 Mixin들이 있다.

Mixin을 이용할 때에는 규칙이 하나 있는데,

다중상속을 받을 때 기존의 뷰는 가장 오른쪽에 위치시키고, 믹스인 기능을 하는 클래스는 왼쪽에 위치시키는 것이다. 

또 Mixin용 클래스는 항상 object를 상속받아야 한다.

믹스인(Mixin)을 이용한 구현 방법

직접 구현하는 방법
아래와 같이 LoginRequiredMixin 클래스를 직접 구현해 클래스형 뷰에서 상속받아 사용할 수 있다. 폼입력과 로그인 통제가 필요한 곳이면 매번 쓰는 기능인데 여간 귀찮고 번거로운게 아니다.

from django.contrib.auth.decorators import login_required

믹스인 구현

```python
# 믹스인용 클래스는 object를 상속받아야 한다.
class LoginRequiredMixin(object):
    @classmethod
    def as_view(cls, **initkwargs):
        view = super(LoginRequiredMixin, cls).as_view(**initkwargs)
        return login_required(view)
```



구현한 믹스인 가져다 쓰기

```python
# 믹스인클래스는 왼쪽에 위치, 가장 오른쪽에는 기존의 뷰를 위치시켜 상속한다.
class PhotoCreateView(LoginRequiredMixin, CreateView):
    model = Photo
    fields = ['album', 'title', 'image', 'description']
    success_url = reverse_lazy('photo:index')
```



만들어진 믹스인(Mixin) 가져다 쓰기
짝짝짝! Django 1.9부터 사용할 수 있다. 아래와 같이 @login_required 데코레이터를 쓰는 것 만큼이나 무척 간편해졌다. 제네릭뷰(Generic View) 때문에 어쩔 수 없이 클래스형 뷰를 사용하는 사람에게 큰 편리함을 준다.

from django.contrib.auth.mixins import LoginRequiredMixin

바로 위 코드와 비교해보자. 아주 간단해졌다.

```python
class MyView(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
```

### **클래스형** **뷰의** **장점**

함수형 뷰와 비교했을 때 클래스형 뷰가 가지는 장점

GET, POST 등의 HTTP 메소드에 따른 처리를 메소드명으로 구분 할 수 있어, 좀 더 깔끔한 구조의(IF 문이 없는) 코드를 생산할 수 있다.

다중 상속과 같은 객체 지향 기술이 가능하여 코드의 재사용성이나 개발 생산성을 높여준다.

**효율적인** **메소드** **구분**

요청을 수신했을 때 요청의 HTTP 메소드를 처리하는 방식을 함수형 뷰와 클래스형 뷰의 차이점을 비교해보자. 우선, 함수형 뷰는 아래와 같은 로직을 작성한다.

함수형뷰 예제

```python
from django.http import HttpResponse

def my_view(request):  
    if request.method == 'GET':
        # 뷰 로직 작성
        return HttpResponse('result')
```



함수형 뷰에서는 예제에서 볼 수 있듯 HTTP 메소드별 다른 처리가 필요할 때 if 문을 이용해야 한다. 

하지만, 클래스형 뷰는 다음과 같이 코드의 구조가 훨씬 깔끔해짐을 볼 수 있다.

**request의 method가** 

 **get형식으로 오면 get 메소드가 실행되어 get 메소드 안의 로직이 수행된다.**

```python
from django.http import HttpResponse  
from django.views.generic import View

class MyView(View):  

    def get(self, request):
        # 뷰 로직 작성
        return HttpResponse('result')
```



클래스형 뷰에서는 HTTP 메소드 이름으로 클래스 내의 메소드를 정의하면 된다. 

**단, 메소드명은 소문자로~ get, post, head ... 이런 메소드명으로 정의해줘야 한다.**

 이러한 처리가 가능한 것은 내부적으로 dispatch() 메소드가 어떤 HTTP 메소드로 요청되었는지 알아내고, 이를 처리해주기 때문이다.

아래의 예는 HTTP의 HEAD 메소드로 코딩하는 예를 보여준다.

```python
from django.http import HttpResponse  
from django.views.generic import ListView  
from books.models import Book

 

class BookListView(ListView):  
    model = Book

    def head(self, *args, **kwargs):
        last_book = self.get_queryset().latest('publication_date')
        response = HttpResponse('')
        response['Last-Modified'] = last_book.publication_date.strftime('%a, %d %b %y %H:%M:%S GMT')
        return response
```



위 예제는 서점에 방문한 직후에 새롭게 출간된 책이 있는지를 문의하는 로직이다. 최근 발간된 책이 없는데도 책 리스트를 서버로부터 받아 오게되면 네트워크 대역폭이 낭비되므로, 이를 방지하기 위해 HEAD 메소드를 사용한다. **HEAD 요청에 대한 응답은 바디 없이 헤더만 보내주면 된다.**

> **상속** **기능** **가능**

개발자가 작성하는 대부분의 클래스형 뷰는 장고가 제공해주는 제네릭 뷰를 상속받아 작성한다.

### 제네릭 뷰

*뷰 개발 과정에서 공통적으로 사용할 수 있는 기능들을 추상화하고, 장고에서 기본적으로 제공해주는 클래스형 뷰*

```python
# some_app/urls.py
from django.conf.urls import patterns  
from some_app.views import AboutView

urlpatterns = patterns('', (r'^about/', AboutView.as_view()),
)

# some_app/views.py
from django.views.generic import TemplateView

class AboutView(TemplateView):  
    template_name = "about.html"
```



views.py 파일의 소스는 단 2줄. 이것이 가능한 이유가 **TemplateView라는 제네릭 뷰를 상속**받아 사용하고 있기 때문이다. TemplateView는 내부속성으로 template_name이라는 속성을 가지고 있는데, 이 속성을 오버라이딩해서 재정의해줘서 해당 뷰로직 수행 후 이동하고자 하는 템플릿의 이름을 지정해주면 request 요청을 받으면 해당 템플릿으로 이동하는 역할을 한다.



아래 예제코드는 URLconf 의 작성만으로 위 예제와 같은 역할을 수행한다.

```python
from django.conf.urls import patterns  
from django.views.generic import TemplateView

urlpatterns = patterns('',  
    (r'^about/', TemplateView.as_view(template_name="about.html")),
)
# 하지만 urls.py에 이런 식으로 뷰의 로직을 정의해버리는 것을 Django의 철학에 위배되므로 권장되지 않는다고 한다. 이렇게 하지말고 필요한 view의 로직은 views.py 안에서 정의하도록 하자.
```

TemplateView 는 특별한 로직이 없고, **URL 맞춰 해당 템플릿 파일의 내용만 보여줄 때 사용하는 제네릭 뷰**이기 때문에 위의 예제들과 같이 사용할 수 있는 것이다.

#### **Django** **의** **제네릭** **뷰**의 종류들

Django 에서 제공하는 제네릭 뷰는 다음과 같이 4가지로 분류할 수 있다.

·         Base View: 뷰 클래스를 생성하고, 다른 제네릭 뷰의 부모 클래스를 제공하는 기본 제네릭 뷰

·         Generic Display View: 객체의 리스트를 보여주거나, 특정 객체의 상세 정보를 보여준다.

·         Generic Edit View: 폼을 통해 객체를 생성, 수정, 삭제하는 기능을 제공한다.

·         Generic Date View: 날짜 기반 객체의 년/월/일 페이지로 구분해서 보여준다.

아래는 위 4가지 분류에 따른 구체 뷰 클래스에 대한 설명을 보여준다.

·         Base View

o    View: 가장 기본이 되는 최상위 제네릭 뷰

o    TemplateView: 템플릿이 주어지면 해당 템플릿을 렌더링한다.

o    RedirectView: URL이 주어지면 해당 URL로 리다이렉트 시켜준다.

·         Generic Display View

o    DetailView: 객체 하나에 대한 상세한 정보를 보여준다.

o    ListView: 조건에 맞는 여러 개의 객체를 보여준다.

·         Generic Edit View

o    FormView: 폼이 주어지면 해당 폼을 보여준다.

o    CreateView: 객체를 생성하는 폼을 보여준다.

o    UpdateView: 기존 객체를 수정하는 폼을 보여준다.

o    DeleteView: 기존 객체를 삭제하는 폼을 보여준다.

·         Generic Date View

o    YearArchiveView: 년도가 주어지면 그 년도에 해당하는 객체를 보여준다.

o    MonthArchiveView: 월이 주어지면 그 월에 해당하는 객체를 보여준다.

o    DayArchiveView: 날짜가 주어지면 그 날짜에 해당하는 객체를 보여준다.

제네릭 뷰의 전체 리스트는 [여기](https://docs.djangoproject.com/en/1.8/ref/class-based-views/)에서 확인 가능하다.

### **클래스** **형** **뷰에서의** **폼** **처리**

```python
from django.http import HttpResponseRedirect  
from django.shortcuts import render  
from django.views.generic import View
from .forms imports MyForm

class MyFormView(View):  
    form_class = MyForm
    initial = {'key': 'value'}
    template_name = 'form_template.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form}

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
        # cleaned_data로 관련 로직 처리
            return HttpResponseRedirect('/success/')
        return render(request, self.template_name, {'form':form})
```

클래스형 뷰에서의 폼처리는 **get, post 방식을 메소드로 구분하여 처리함**으로써, 코드 구조가 깔끔해진다. 
 이 코드를 위에서 봤었던 제네릭 뷰인 FormView 를 상속받아 처리하면 아래와 같이 더 간결해지는 것을 볼 수 있다.

```python
from .forms imports MyForm  
from django.views.generic.edit import FormView

class MyFormView(FormView):  
    form_class = MyForm
    template_name = 'form_template.html'
    success_url = '/thanks/'

    def form_valid(self, form)
        return super(MyFormView, self).form_valid(form)
```



get, post 메소드가 사라졌습니다. 그리고 여기에서는 아래 항목들만 유의해서 지정해주면 됩니다.

·         form_class: 사용자에 보여줄 폼을 정의한 forms.py 파일 내의 클래스명

·         template_name: 폼을 포함하여 렌더링할 템플릿 파일 이름

·         success_url: MyFormView 처리가 정상적으로 완료되었을 때 리다이렉트 될 URL

·         form_valid() 함수: 유효한 폼 데이터로 처리할 로직 코딩. 반드시 super() 함수를 호출해야 함.

> 제네릭 뷰가 편리하고 코드의 길이를 많이 줄여주긴 하지만, 
>
> 각 제네릭 뷰 내부에 정의되어있는 속성을 알아야 쓰기 편하기 때문에 무작정 쓰는 건 힘들다. Documentation을 참조해서 써야함.
>
> form_class 나 success_url이 정확히 무슨 역할을 하는지 명확하게 드러나질 않고, 이런 필요한 속성명들을 정확하게 알고 있어야 하기 때문에 마냥 편한 건 아닌 듯하다. 

-----------------------------------------



### 정규식 패턴에 대해서

캐럿(^)은 "패턴이 문자열의 시작과 일치해야 함"을 의미하고 

달러 기호($)는 "패턴이 문자열의 끝과 일치해야합니다"를 의미합니다.

urlpatterns = patterns('',
​    url(r'^hello/$', hello),
)

Without the dollar sign at the end it will match any url starting with hello like
hello/satish
hello/gandham/
hello/satish/123/pqr
Note: use url(r'^$', my_homepage_view), to match root.

URL패턴 만드는 방법이 궁금하다면, 다음 표기법을 확인하세요. 이 중 몇 가지 규칙만 사용할 거에요.

^ : 문자열이 시작할 떄
$ : 문자열이 끝날 때
\d : 숫자
: 바로 앞에 나오는 항목이 계속 나올 때
() : 패턴의 부분을 저장할 때
이외에도 문자열을 이용해 url을 만들 수 있어요.

http://www.mysite.com/post/12345/라는 사이트가 있다고 합시다. 여기에서 12345는 글 번호를 의미합니다.

뷰마다 모든 글 번호을 일일이 매기는 것은 정말 힘들죠. 정규표현식으로 url패턴을 만들어 숫자값과 매칭되게 할 수 있어요. 이렇게 말이죠. ^post/(\d+)/$. 어떤 뜻인지 하나씩 살펴봅시다.

^post/ : url이(오른쪽부터) post/로 시작합니다. 캐럿(^) 은 정규식의 시작을 알린다.
(\d+) : 숫자(한 개 이상)가 있습니다. 이 숫자로 조회하고 싶은 게시글을 찾을 수 있어요.
/ : /뒤에 문자가 있습니다.
$ : url 마지막이 /로 끝납니다. 달러($)는 정규식의 끝을 알림.