from django.contrib import admin

from accounts.models import Notify, Basket


@admin.register(Notify)
class NotifyAdmin(admin.ModelAdmin):
    pass


@admin.register(Basket)
class BasketAdmin(admin.ModelAdmin):
    pass
