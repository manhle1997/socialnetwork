from django.contrib import admin
from app.models import UserProfile


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'user_infor', 'city', 'phone', 'website')

    def user_infor(self, obj):
        return obj.description

    def get_queryset(self, request):
        queryset = super(UserProfileAdmin, self).get_queryset(request)
        queryset = queryset.order_by('phone', 'user')
        return queryset

    user_infor.short_description = 'In4'

admin.site.register(UserProfile, UserProfileAdmin)
