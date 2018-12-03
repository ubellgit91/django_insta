from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
#
from django.views import View
from .models import Photo
# Create your views here.


def hello(request):
    return HttpResponse("ㅎㅇ")


class DetailView(View):
    def get(self, request, pk):
        photo = get_object_or_404(Photo, pk=pk) # model 클래스의 객체를 pk에 맞춰서 get하고, 없으면 404 에러 페이지를 보냄.
        message = ('<p>{pk}번 사진 보여줍니다.</p>'.format(pk=photo.pk),
                   '<p>주소는 {url}</p>'.format(url=photo.image.url),
                   '<p><img src="{img}"/></p>'.format(img=photo.image.url), #이대로 url만 넘김녀 오류가 발생함.
                   )

        return HttpResponse('\n'.join(message))

