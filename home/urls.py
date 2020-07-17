from django.urls import path
from . import views


urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('connect/(?P<operation>.+)/<int:pk>/', views.change_friend, name='change_friend'),
    path('<int:id>/', views.post_detail, name = 'detail_post')
]