from django.contrib import admin

from accounts.models import Notify, Basket, Profile, Point


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    pass


@admin.register(Notify)
class NotifyAdmin(admin.ModelAdmin):
    pass


@admin.register(Basket)
class BasketAdmin(admin.ModelAdmin):
    pass


@admin.register(Point)
class PointAdmin(admin.ModelAdmin):
    pass
