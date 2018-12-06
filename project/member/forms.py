from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

User =get_user_model()


# 로그인 = 인증. 인증관련 폼을 장고에서 제공해주는 인증폼을 상속받아 재정의해서 만들어보자.
class LoginForm(AuthenticationForm):
    # 생성자 . 객체 생성 시점에 인자값 받고 실행됨.
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        class_update_field = ['username', 'password',]
        for field_name in class_update_field:
            self.fields[field_name].widget.attrs.update({
                'class': 'form-control'
            })


class SignupForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        class_update_fields = ['password1', 'password2',]
        for field_name in class_update_fields:
            self.fields[field_name].widget.attrs.update({
                'class': 'form-control'
            })

    class Meta:
        model = User
        fields = (
            'username',
            'password1',
            'password2',
            'img_profile',
            'gender',
        )
        widget = {
            'username': forms.TextInput(
                attrs={
                    'class': 'form-control',
                }
            ),
            'gender': forms.Select(
                attrs={
                    'class': 'form-control',
                }
            )
        }


# class LoginForm(forms.Form):
#     username = forms.CharField(
#         widget=forms.TextInput(
#             attrs={
#                 'class': 'form-control',
#             }
#         )
#     )
#     password = forms.CharField(
#         widget=forms.PasswordInput(
#             attrs={
#                 'class': 'form-control',
#             }
#         )
#     )
#
#
# class SignupForm(forms.Form):
#     username = forms.CharField(
#         widget=forms.TextInput(
#             attrs={
#                 'class': 'form-control',
#             }
#         )
#     )
#     password1 = forms.CharField(
#         widget=forms.PasswordInput(
#             attrs={
#                 'class': 'form-control',
#             }
#         )
#     )
#
#     password2 = forms.CharField(
#         widget=forms.PasswordInput(
#             attrs={
#                 'class': 'form-control',
#             }
#         )
#     )
#     # username필드의 검증에 username이 이미 사용중인지 여부 검사.
#     def clean_username(self):
#         username = self.cleaned_data['username']
#         if User.objects.filter(username=username).exists():
#             raise forms.ValidationError('아이디가 이미 사용중입니다.')
#         return username
#
#     def clean_password2(self):
#         password1 = self.cleaned_data['password1']
#         password2 = self.cleaned_data['password2']
#         if password1 != password2:
#             raise forms.ValidationError('비밀번호와 비밀번호 확인의 값이 일치하지 않습니다.')
#         return password2
#
#     # 자신이 가진 username과 password를 사용해서 유저 생성 후 반환하는 메서드
#     def singup(self):
#         if self.is_valid():
#             return User.objects.create_user(
#                 username=self.cleaned_data['username'],
#                 password=self.cleaned_data['password2']
#             )