from django.contrib import admin

from accounts.models import Notify, Bucket


@admin.register(Notify)
class NotifyAdmin(admin.ModelAdmin):
    pass


@admin.register(Bucket)
class BucketAdmin(admin.ModelAdmin):
    pass
