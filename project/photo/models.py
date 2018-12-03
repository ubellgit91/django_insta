from django.db import models

# Create your models here.
class Photo(models.Model):
    image = models.ImageField(upload_to='%Y/%m/%d/origin') # ImageField는 파일을 다루는 필드인 FileField를 상속받은 필드이다. 이미지를 대상하기 때문에 ImageField임.
    filtered_image = models.ImageField(upload_to='%Y/%m/%d/filtered') # 이미지관리를 위한 여러가지 필드옵션을 갖는다. upload_to, height_field, width_filed 등..
    content = models.TextField(max_length=500, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True) # auto_now_add 필드옵션은 객체가 최초 생성될 때의 시간이 기록됨.

    def delete(self, *args, **kwargs):
        self.image.delete()
        self.filtered_image.delete()
        super(Photo, self).delete(*args, **kwargs)