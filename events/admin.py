from django.contrib import admin

from events.models import CouponHold, CouponNumber, Advertisement


@admin.register(CouponHold)
class CouponHoldAdmin(admin.ModelAdmin):
    pass


@admin.register(CouponNumber)
class CouponNumberAdmin(admin.ModelAdmin):
    pass


@admin.register(Advertisement)
class AdvertisementAdmin(admin.ModelAdmin):
    pass
