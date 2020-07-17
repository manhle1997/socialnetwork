import re
from django.conf import settings
from django.urls import reverse
from django.shortcuts import redirect
from django.contrib.auth import logout

#Thực hiện chức năng nếu đã đăng nhập tài khoản rồi thì sẽ không thể
# đăng nhập hay đăng kí được nữa

EXEMPT_URLS = [re.compile(settings.LOGIN_URL.lstrip('/'))]
if hasattr(settings, 'LOGIN_EXEMPT_URLS'):
    EXEMPT_URLS += [re.compile(url) for url in settings.LOGIN_EXEMPT_URLS]

class LoginRequiredMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        assert hasattr(request, 'user')
        path = request.path_info.lstrip('/')
        print(path)


        url_is_exempt = any(url.match(path) for url in EXEMPT_URLS)
        # Hàm any(interable) return True nếu có một giá trị trong interable là True
        # Và return False nếu tất cả interable trả về False hoặc interable rỗng
        # ý nghĩa của url_is_exempt sẽ so sánh url hiện tại với từng url trong EXEMPT_URLS nếu chỉ 1 cái trùng thì sẽ trả về True

        if path == reverse('logout').lstrip('/'):
            logout(request)

        if request.user.username and url_is_exempt:
            return redirect(settings.LOGIN_REDIRECT_URL)
        elif request.user.username or url_is_exempt:
            return None
        else:
            return redirect(settings.LOGIN_URL)

