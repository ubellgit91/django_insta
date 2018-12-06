from django.shortcuts import render, redirect
from django.contrib.auth import login as django_login, logout as django_logout, authenticate
from django.views.generic import View

from .forms import LoginForm, SignupForm


class LoginView(View):
    def get(self, request):
        login_form = LoginForm()
        context = {
            'login_form': login_form,
        }
        return render(request, 'member/login.html', context)

    def post(self, request):
        next = request.GET.get('next')
        # Data bounded form 인스턴스 생성
        # AuthencationForm의 생성자에 들어가는 첫 번째 인수는 해당 request가 되어야 한다.
        # 이렇게 key=value 형태로 인자값을 넘기면, **kwargs 매개변수가 값을 받음.
        login_form = LoginForm(request=request, data=request.POST)
        # 유효성 검사에 성공할 경우
        # AuthenticationForm을 사용하면 authenticate과정까지 완료되어야 유효성 검증을 통과한다
        if login_form.is_valid():
            # AuthenticatonForm에서 인증(authenticate)에 성공한 유저를 가져오려면 이 메서드를 사용한다
            user = login_form.get_user()
            # Django의 auth앱에서 제공하는 login함수를 실행해 앞으로의 요청/응답에 세션을 유지한다.
            django_login(request, user)
            # next가 존재하면 해당 위치로, 없으면 목록으로 이동
            return redirect(next if next else 'photo:list')
        # 인증에 실패하면 login_form에 non_field_error를 추가함.
        login_form.add_error(None, '아이디 또는 비밀번호가 올바르지 않습니다.')


class LogoutView(View):
    def get(self, request):
        django_logout(request)
        return redirect('photo:list')


class SignupView(View):
    def get(self, request):
        signup_form = SignupForm()
        context = {
            'signup_form': signup_form,
        }
        return render(request, 'member/signup.html', context)

    def post(self, request):
        signup_form = SignupForm(request.POST)
        # 유효성 검증에 통과한 경우
        if signup_form.is_valid():
            user = signup_form.save()
            django_login(request, user)
            return redirect('photo:list')

