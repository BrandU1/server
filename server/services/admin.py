from django.contrib import admin

from services.models import Notice, MainInfo, FAQ, Inquiry


@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):
    pass


@admin.register(MainInfo)
class MainInfoAdmin(admin.ModelAdmin):
    pass


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    pass


@admin.register(Inquiry)
class InquiryAdmin(admin.ModelAdmin):
    pass
