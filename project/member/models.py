from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

# User에 관한 커스텀 유저모델을 만들 땐, 다른 model과 다르게 AbstractUser를 상속받아야 한다고 함
# 상위 클래스에 있는 부분에서 필요한 부분은 오버라이딩해서 재정의 하고, 아니면 걍 덧붙인다.
class User(AbstractUser):
    # pass
    GENDER_MALE = 'm'
    GENDER_FEMALE = 'f'
    GENDER_OTHER = 'o'
    CHOICES_GENDER = (
        (GENDER_MALE, '남성'),
        (GENDER_FEMALE, '여성'),
        (GENDER_OTHER, '기타'),
    )
    img_profile = models.ImageField(upload_to='user', blank=True)
    gender = models.CharField(max_length=1, choices=CHOICES_GENDER)
    like_posts = models.ManyToManyField('photo.Post', blank=True, related_name='like_users')

    def __str__(self):
        return self.username