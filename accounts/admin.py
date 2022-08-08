from django.contrib import admin

from accounts.models import Notify


@admin.register(Notify)
class NotifyAdmin(admin.ModelAdmin):
    pass
