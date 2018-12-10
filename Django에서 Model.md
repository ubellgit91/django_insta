# Django에서 Model

## Model이란?

Django에서 Model은 **데이타 서비스를 제공하는 Layer**이다. Django의 Model은 각 Django App안에 기본적으로 생성되는 **models.py 모듈 안에 정의**하게 된다. models.py 모듈 안에 하나 이상의 모델 클래스를 정의할 수 있으며, **하나의 모델 클래스는 데이타베이스에서 하나의 테이블에 해당**된다.

Django 모델은 "django.db.models.Model" 의 파생 클래스!!!이며, 모델 클래스의 각 속성(Attribute)은 테이블의 필드에 해당한다. 위의 예를 보면 Feedback이라는 클래스가 modesl.Model의 파생클래스이며, 그 클래스 안에 4개의 클래스 변수 (혹은 Class Attribute)가 있음을 볼 수 있다. (만약 Primary Key가 지정되지 않으면, DB 테이블 생성시 자동으로 id 가 생성된다)

모델 클래스는 필드를 정의하기 위해 인스턴스 변수가 아닌 [**클래스 변수를 사용**]하는데, 이는 그 변수가 테이블 필드의 내용을 갖는 것이 아니라, 
**[테이블의 컬럼 메타 데이타를 정의=테이블에서의 컬럼**]하는 것이기 때문이다. 
필드를 정의하는 각각의 클래스 변수는 models.CharField(), models,IntegerField(), models.DateTimeField(), models.TextField() 등의 각 필드 타입에 맞는 Field 클래스 객체를 생성하여 할당한다. Field 클래스는 여러 종류가 있는데, 생성자 호출시 필요한 옵션들을 지정할 수 있다.

각 Field 클래스마다 반드시 지정해야 주어야 하는 옵션이 있을 수 있는데, 이는 **필드옵션**이라고 한다. 예를 들어 CharField (와 그 서브클래스들)은 필드의 최대 길이를 나타내는 max_length를 항상 지정해 주어야 한다.

**필드 타입**
모델의 필드에는 다양한 타입들이 있는데, 필드 타입에 대한 자세한 정보는 여기 Django 필드 타입 링크를 참고하면 된다. 모든 필드 타입 클래스들은 추상클래스인 "Field" 클래스의 파생클래스들이다. 아래는 주요 필드 타입에 대한 간단한 요약이다.

**Field Type	설명**
CharField	제한된 문자열 필드 타입. 최대 길이를 max_length 옵션에 지정해야 한다. 문자열의 특별한 용도에 따라 CharField의 파생클래스로서, 이메일 주소를 체크를 하는 EmailField, IP 주소를 체크를 하는 GenericIPAddressField, 콤마로 정수를 분리한 CommaSeparatedIntegerField, 특정 폴더의 파일 패스를 표현하는 FilePathField, URL을 표현하는 URLField 등이 있다.
TextField	대용량 문자열을 갖는 필드
IntegerField	32 비트 정수형 필드. 정수 사이즈에 따라 BigIntegerField, SmallIntegerField 을 사용할 수도 있다.
BooleanField	true/false 필드. Null 을 허용하기 위해서는 NullBooleanField를 사용한다.
DateTimeField	날짜와 시간을 갖는 필드. 날짜만 가질 경우는 DateField, 시간만 가질 경우는 TimeField를 사용한다.
DecimalField	소숫점을 갖는 decimal 필드
BinaryField	바이너리 데이타를 저장하는 필드
FileField	파일 업로드 필드
ImageField	FileField의 파생클래스로서 이미지 파일인지 체크한다.
UUIDField	GUID (UUID)를 저장하는 필드

**필드 옵션**
모델의 필드는 필드 타입에 따라 여러 옵션(혹은 Argument)를 가질 수 있다. 예를 들어, CharField는 문자열 최대 길이를 의미하는 max_length 라는 옵션을 갖는다. 필드 옵션은 일반적으로 생성자에서 아규먼트로 지정한다. 다음은 모든 필드 타입에 적용 가능한 옵션들 중 자주 사용되는 몇가지를 요약한 것이다.

필드 옵션	설명
null (Field.null)	null=True 이면, Empty 값을 DB에 NULL로 저장한다. DB에서 Null이 허용된다. 예: models.IntegerField(null=True)
blank (Field.blank)	blank=False 이면, 필드가 Required 필드이다. blank=True 이면, Optional 필드이다. 예: models.DateTimeField(blank=True)
primary_key (Field.primary_key)	해당 필드가 Primary Key임을 표시한다. 예: models.CharField(max_length=10, primary_key=True)
unique (Field.unique)	해당 필드가 테이블에서 Unique함을 표시한다. 해당 컬럼에 대해 Unique Index를 생성한다. 예: models.IntegerField(unique=True)
default (Field.default)	필드의 디폴트값을 지정한다. 예: models.CharField(max_length=2, default="WA")
db_column (Field.db_column)	컬럼명은 디폴트로 필드명을 사용하는데, 만약 다르게 쓸 경우 지정한다.

## 기본적인 모델의 예제

```python
class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='%Y/%m/%d/origin') # ImageField는 파일을 다루는 필드인 FileField를 상속받은 필드이다. 이미지를 대상하기 때문에 ImageField임.
    filtered_image = models.ImageField(upload_to='%Y/%m/%d/filtered') # 이미지관리를 위한 여러가지 필드옵션을 갖는다. upload_to, height_field, width_filed 등..
    content = models.TextField(max_length=500, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True) # auto_now_add 필드옵션은 객체가 최초 생성될 때의 시간이 기록됨.

    def delete(self, *args, **kwargs):
        self.image.delete()
        self.filtered_image.delete()
        super(Post, self).delete(*args, **kwargs)
        
    def get_absolute_url(self):
        url = reverse_lazy('detail', kwargs={'pk': self.pk})
        return url

    def __str__(self):
        return 'Post (PK: {pk}, Author: {username})'.format(pk=self.pk, username=self.author.username)
```

모델은 기본적으로 django.db.models.Model 클래스를 상속받은 클래스로 만들어진다.

필드를 정의하는 각각의 클래스 변수는 models.CharField(), models,IntegerField(), models.DateTimeField(), models.TextField() 등의 각 필드 타입에 맞는 Field 클래스 객체를 생성하여 할당한다.

모델 클래스에 정의된 클래스 변수들이 테이블에서 쓰일 칼럼명이며, 해당 변수에 할당된 값들이 이 칼럼에서 쓰일 데이터의 타입(필드타입)이다. 

클래스에 정의된 메소드(클래스 내부의 함수는 메소드라고 부른다)들은 

해당 모델객체를 제어하기 위해서 정의한다. 

Model에 정의된 Model을 상속받은 클래스들은 각각이 테이블을 의미하며, 해당 클래스을 기반으로 객체를 생성하면, 그 객체는 테이블의 record(row)가 된다.

그 테이블의 row를 제어하기 위해 모델클래스의 내부에 메소드를 정의해서 쓰는 것.



## Model 객체의 ModelManager 사용법



> Django는 디폴트로 모든 Django 모델 클래스에 대해 "objects" 라는 Manager (django.db.models.Manager) 객체를 자동으로 추가한다 (이 objects라는 이름을 변경할 수도 있지만, 대부분 그대로 사용한다). Django 에서 제공하는 이 Manager를 통해 특정 데이타를 필터링 할 수도 있고 정렬할 수도 있으며 기타 여러 기능들을 사용할 수 있다.
>
> 데이타를 읽어오기 위해서는 **Django 모델의 Manager 즉 "모델클래스.objects" 를 사용**한다. 예를 들어, Feedback 이라는 모델의 경우 "Feedback.objects" 를 사용한다 (객체명이 아니라 클래스명을 사용함에 주의).Django Model API에는 기본적으로 제공하는 여러 쿼리 메서드들이 있는데, 여기서는 자주 사용되는 주요 메서드 몇 가지만 살펴보자. (Feedback 모델 클래스를 기준으로 설명)

장고에서 제공하는 모델을 사용하기 위해선 일단

`from 앱이름.models import 모델명, 모델명`과 같이 선언해야 한다.

### Model API -> ModelManager를 이용해보기.

Select

> Get

단일 행 결과를 반환하는 **model.objects.get()**는 타입이 Query Set이 아닌 단일행 (모델타입)으로 나옴

사용은 value_name.column_name 과 같이 . 으로 컬럼 이름을 써서 사용합니다.

get() 안에 조건을 제시할 수 있습니다.(**sql**의**where**절**과** **동일**)

**get()은 단일행을 반환하므로 다른 method들을 get() 다음에 연결하여 사용할 수 없습니다.**

​      key = model1.objects.get(pk=pk)   print(key.name)      

만약 get을 사용했는데 반환되는 값이 1개 이상일 경우 에러가 나옵니다.

> All

전체 자료를 불러오는 **model.objects.all()**은 **QuerySet 타입**으로 반환

사용은 dictionary를 사용하는 것과 동일하게 사용.

​      key =   model2.objects.all()   print(key[0]['name'])      

만약 get()과 같이 단일 행의 결과가 존재하지 않을 경우 모델명.DoesNotExist의 exception으로 처리가 되지만 all()과 같은 여러 행이 나오는 경우엔 exception이 아닌 빈값으로 처리가 됩니다.

> Filter

앞에서 get()은 단일행을 조건을 걸어 출력하는 것이면, filter는 조건에 맞는 여러 행을 출력하는 것입니다. 사용은 **model.objects.filter()**로 타입은 QuerySet입니다. (**objects.all().filter()** 와 동일한 기능입니다. (all() 생략) )

​      value = key   = model2.objects.filter(name='lee')   print(key[0]['name'])      

**get****과** **filter**에 각 조건을 걸 수 있으며 조건은 **and**로 결합됩니다.

**조건** **키워드**

| **키워드**                            | **설** **명**                                                | **사용예**                                                   |
| ------------------------------------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| `    __lt / __gt   __lte / __gte   `  | 보 다 작다 / 보다 크다   같거나 보다 작다 / 같거나 보다 크다 | id가 1보다 큰 자료 검색   >>> Department.objects.filter(id__gt=1)   [<Department: Computer Science>] |
| `   __in   `                          | 주어진 리스트 안에 존재하는 자료 검색                        | id 가 2, 3, 5 인 자료 검색    >>> Department.objects.filter(id__in=[2, 3, 5])    [<Department: Computer Science>] |
| `    __year / __month / __day   `     | 해당 년도, 월, 일 자료 검색                                  | >>>Entry.objects.filter(pub_date__year=2005)                 |
| `  __isnull  `                        | 해 당 열의 값이 null 인 자료  검색                           | >>   Department.objects.filter(dName__isnull=True)   []      |
| `    __contains / __icontains   `     | 해당 열의 값이 지정한 문자열을 포함하는 자료 검색   (__icontains 는 대소문자를 구별하지 않음) | >>> Department.objects.filter(dName__contains='puter')   [<Department: Computer Science>] |
| `    __startswith / __istartswith   ` | 해당 열의 값이 지정한 문자열로 시작하는 자료 검색   (__istartswith 는 대소문자를 구별하지 않음) | >>>   Department.objects.filter(dName__startswith='Com')    [<Department: Computer Science>] |
| `    __endswith / __iendswith   `     | 해당 열의 값이 지정한 문자열로 끝나는 자료 검색   (__iendswith 는 대소문자를 구별하지 않음) | >>>   Department.objects.filter(dName__contains='nce')    [<Department: Computer Science>] |
| `   __range   `                       | 문 자, 숫자, 날짜의 범위를 지정함   (SQL의 BETWEEN에         | >>> Department.objects.filter(id__range=(2,   10))           |

> Order by

**model.objects.order_by()**로 사용하며 기본 정렬순서는 오름차순 정렬입니다. 내림차순으로 정렬할 경우 컬러명 앞에 -를 붙여 사용합니다.

​      value =   model.objects.order_by('-pk') # 내림차순 정렬   value =   model.objects.order_by('pk') # 오름차순 정렬      

> Value

**model.objects.values()**와 같이 사용하며 기능은 sql의 select에 해당합니다. value를 사용하지 않으면 **sql****의** **select \*** 와 같이 전체 컬럼을 출력합니다.

​      value =   model.objects.values('pk') # query set 타입으로 pk만 출력      

> Aggregate

sql에서 max, min, count 등과 같이 다중 행을 단일 행으로 출력해주는 기능을 해줍니다.

**model.objects.aggregate()**와 같이 사용되며 단일행을 반환하므로 aggregate()뒤에 다른 method를 붙여 사용할 수 없습니다.

​      from   django.db.models import Max   value =   model.objects.aggregate(temp_name=Max('pk')) # temp_name은 사용자가 임의로 정할 수 있음   print(value['temp_name'])      

 

​      from   django.db.models import Max   from   django.db.models.functions import Coalesce   value =   model.objects.aggregate(temp_name=Coalesce(Max('pk'),10000)) # temp_name은 사용자가 임의로 정할 수 있음   print(value['temp_name'])      

Annotate

----------------;;--------------------------

​    

----------------------------------------------------

### DB에 데이터를 CRUD하는 방법들.



> Insert

Django Model 사용

모델을 사용하여 insert를 하는 방법은 2가지가 있습니다. 보통의 경우는 rest framework를 사용해 저장할 값에 대한 validation check를 한 다음 저장하는 형식이 안전하기 때문에 rest framework를 사용하는 것을 권장합니다.

**save()** **사용**

```python
data = Model(name='g') # 이런 식으로 모델의 객체를 생성하고
data.save() # 상속받은 models.Model 클래스 내부에 정의되어있는 메소드 save()를 이용해 데이터를 insert한다.
```

Model 클래스의 객체를 생성하게 되면, **해당 테이블에 하나의 row가 생성되는 것과 동일하다**!

그렇게 테이블에 들어갈 row를 생성하고 , 상속받은 메소드 save()를 이용해서 테이블에 저장하는 것이다.

save()를 하지 않을 경우 메모리 상에 저장할 데이터의 Instance만 존재하고 테이블에 저장되지는 않습니다.

**objects.create()** **사용**

```python
data =  model2.objects.create(name='lee') 
```

ModelManager인 objects를 이용하는 방법.

objects.create를 할 경우 .save()를 할 필요가 없이 바로 저장이 됩니다.

**Rest framework 사용**

Django로 rest api를 만드려고 할 때, 가장 널리 쓰이는 프레임워크 중 하나입니다. 해당 프레임워크를 사용해 손쉽게 insert를 할 수 있습니다. (설치 및 사용법은 [Django REST Framework](http://wiki.duzon.com:8080/display/~tweety2411/Django+REST+Framework)에 설명되어 있습니다.)

```python
serializer = CommonTax1InSerializer(data=json_format_data, partial=True)       
if serializer.is_valid():       
    serializer.save()      
```

​      serializer =   CommonTax1InSerializer(data=json_format_data, partial=True)       if   serializer.is_valid():       serializer.save()      

**json_format_data**는 json(dict)형식의 데이터입니다. 

serializer는 데이터를 직렬화 시키는 클래스임. 테이블에 들어갈 , 혹은 출력시킬 데이터들을 받아서 일정한 형식으로 직렬화 시킨다. (Restful API로 이용할 땐, DB에서 뽑아온 정보를 json이나 xml으로 직렬화 시켜서 전송시켜줌)

**partial**은 테이블 내의 일부분만 insert할 때, 필요한 아규먼트입니다. 만약 partial을 제외하고 serializer에 명시한 값 중 일부분만 insert하려하면 에러가 나게 됩니다.

.save()를 하기 위해선 먼저 validation 확인을 한 다음 진행해야 됩니다.

> Update

Django Model 사용

**단일** **업데이트**

먼저 1개 단일 행의 데이터를 변경하는 것은 다음과 같습니다.

```python
  data =   model2.objects.get(pk=pk)
  data.name =   'kim'   # pk가 일치하는 model객체(row)를 가져와서, 그 model(row)에 있는 name 필드(칼럼)의 값을 kim으로 수정한다.
  data.save()    # 그리고 저장함. ==> update와 같음.
```

insert와 유사하게 save()를 사용합니다. 만약 해당 object가 기존 테이블에 존재하지 않으면 insert 기능을 수행하고, 그렇지 않으면 update 기능을 수행합니다.

**위처럼** **get()으로** **받아와서** **update**를 **하는** **경우는** **pk**가 **단일** **컬럼으로** **잡혀있는** **경우에만** **사용이** **가능합니다**

 (여러컬럼이 묶여 **하나의** **pk**를 **이루는** **형태에서는** **불가능**)

**다중** **업데이트**

여러 행의 데이터 및 여러 컬럼이 묶여 하나의 pk를 이루는 형태의 테이블에서 데이터를 변경하는 것은 다음과 같습니다.

```python
 model2.objects.filter(name='lee',   age='20').update(**update_dict)      
```

***\*update_dict****에** **대한** **설명은** **다음** [**parameter (****또는** **argument)** **앞에** ***, \**** **의미**](http://wiki.duzon.com:8080/pages/viewpage.action?pageId=3690568)**에** **정리되어** **있습니다****.**

Rest framework 사용

**단일** **업데이트**

먼저 1개 단일 행의 데이터를 변경하는 것은 다음과 같습니다.

```python
pk =   model2.objects.get(pk=pk)   
serializer =  model2(pk, data=json_data) 
# pk값을 기준으로 얻어온 해당 row를 update하고자하는 값이 담긴 json_data를 넘겨 새로운 model객체로 만든다.
if serializer.is_valid():       
    serializer.save()      
```

먼저 업데이트할 단일행을 구한다음, 모델 클래스의 아규먼트로 instance에 pk를 넣고 data에 변경할 값의 json(dict) 값을 넣습니다.

**다중** **업데이트**

먼저 다중 행의 데이터를 변경하는 것은 다음과 같습니다.

```python
queryset =  model2.objects.all()   
serializer =  BookSerializer(queryset, many=True)   
if serializer.is_valid():       
    serializer.save()
```



여러 컬럼이 묶여 하나의 pk를 이루고 있는 형태에서 rest framework를 사용해 update를 하려고 할 때 방법이 복잡하기 때문에 django model을 사용하는 것이 낫습니다.

​    

> Delete

delete는 update와 유사하게 동작하지만 단일 행이나 복수 행 구분없이 똑같이 delete()메소드를 사용합니다. 또한 rest framework나 django model 둘 다 같은 방식을 사용하고 있습니다.

**단일** **삭제**

먼저 1개 단일 행의 데이터를 삭제하는 것은 다음과 같습니다.

```python
pk =   model2.objects.get(pk=pk)   
pk.delete()     
# delete()메소드는 Model클래스 내부에 정의되어 있음. 다른 기능이 필요하다면 재정의해서 사용가능.
```



**다중** **삭제**

여러 행 및 쿼리 결과의 데이터를 삭제하는 것은 다음과 같습니다.

```python
model2.objects.filter(name='lee',age='20').delete() 
```

