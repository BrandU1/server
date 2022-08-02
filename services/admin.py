from django.contrib import admin

from services.models import Notice


@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):
    pass
