from django.db import models
from django.urls import reverse_lazy
from django.conf import settings

# Create your models here.


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


# comment
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()

    def __str__(self):
        return 'Comment (PK: {pk}, Author: {username})'.format(pk=self.pk, username=self.author.username)