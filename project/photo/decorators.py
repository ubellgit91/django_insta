from functools import wraps
from urllib.parse import urlparse

from django.contrib.auth.decorators import login_required as django_login_required
from django.contrib.auth.views import redirect_to_login
from django.core.handlers.wsgi import WSGIRequest


def login_required(view_func):
    @wraps(view_func)
    def decorator(*args, **kwargs):
        if args:
            request = args[0]
            # Django의 view에서 첫 번째 매개변수는 HttpRequest타입의 변수이며, 이를 확인한다
            # 또한 요청 메서드가 POST인지 확인한다
            if isinstance(request, WSGIRequest) and request.method == 'POST':
                # request의 user가 존재하며 인증되어있는지 확인한다
                user = getattr(request, 'user')
                if user and user.is_authenticated:
                    return view_func(*args, **kwargs)
                # 인증되지 않았을 경우, HTTP_REFERER의 path를 가져온다
                path = urlparse(request.META['HTTP_REFERER']).path
                # 로그인 뷰로 이동하며 GET파라미터의 next값을 path로 지정해주는
                # redirect_to_login함수를 되돌려준다
                return redirect_to_login(path)
        # 위에 해당하지 않는 경우, Django에서 제공하는 기본 login_required를 데코레이터로 사용한다
        return django_login_required(view_func)(*args, **kwargs)
    return decorator