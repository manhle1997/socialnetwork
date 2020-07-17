from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView

from app.forms import CustomAuthForm

urlpatterns = [
    #path('', views.home, name='home'),
    path('login/', LoginView.as_view(template_name='accounts/login.html', authentication_form=CustomAuthForm), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
    path('profile/', views.view_profile, name='view_profile'),
    path('profile/<int:pk>/', views.view_profile, name='view_profile_with_pk'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('profile/change-password', views.change_password, name='chane_password'),
    path('profile/reset-password', PasswordResetView.as_view(template_name='accounts/password_reset.html', success_url='reset-password/done', email_template_name='accounts/password_reset_email.html'), name='reset_password'),
    path('profile/reset-password/done', PasswordResetDoneView.as_view(template_name='accounts/password_reset_email.html'), name='password_reset_done'),
    path('profile/reset-password/confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('profile/reset-password/complete/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('profile/edit/addimages/', views.add_image_avatar, name='add_image_avatar')
]
#For debugging purposes you could setup a local smtpserver with this command:
#python -m smtpd -n -c DebuggingServer localhost:1025