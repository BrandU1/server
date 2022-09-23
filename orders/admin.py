from django.contrib import admin

from orders.models import Order, Delivery


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    pass


@admin.register(Delivery)
class DeliveryAdmin(admin.ModelAdmin):
    pass
