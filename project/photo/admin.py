from django.contrib import admin
#
from .models import Post, Comment
# Register your models here.

# ModelAdmin 클래스를 상속받아서 작성한 클래스는 해당 모델에 대해 보여줄 필드 속성 등을 지정할 수 있다.
# 커스텀 ModelAdmin임.
class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'author', 'content', 'image', 'filtered_image', 'created_at', ]

# register(self, cls, executable=None):
admin.site.register(Post, PostAdmin)
admin.site.register(Comment)

# contrib 패키지 안에 admin 패키지로 존재합니다.
# # admin.site.register는 admin 패키지에 있는 sites 모듈에서 AdminSite 클래스를 site라는 이름을 갖는 인스턴스로 만들고,
# # 이 site 객체의 인스턴스 메서드인 register로 지정한 모델을 Admin 영역에서 관리하도록 등록합니다.