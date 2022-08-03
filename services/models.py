from django.db import models

from core.mixins import BaseModel


class Notice(BaseModel):
    title = models.CharField(max_length=100)
    description = models.TextField()


class MainInfo(BaseModel):
    title = models.CharField(max_length=100)
    description = models.TextField()


class FAQ(BaseModel):
    title = models.CharField(max_length=100)
    description = models.TextField()


class Inquiry(BaseModel):
    profile = models.ForeignKey('accounts.Profile', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()

    @property
    def is_answer(self) -> bool:
        return bool(InquiryAnswer.objects.filter(inquiry=self).exists())


class InquiryAnswer(BaseModel):
    inquiry = models.OneToOneField('services.Inquiry', on_delete=models.CASCADE)
    description = models.TextField()
