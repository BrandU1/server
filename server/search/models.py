from django.db import models
from rest_framework.exceptions import PermissionDenied, NotFound

from accounts.models import Profile
from core.mixins import BaseModel


class Search(BaseModel):
    profile = models.ForeignKey('accounts.Profile', on_delete=models.CASCADE)
    search_word = models.CharField(max_length=100)

    @staticmethod
    def search_keyword(query: str | None, profile: Profile | None) -> None:
        if query is None:
            raise NotFound('query is None')

        if profile is None:
            raise PermissionDenied('profile is None')

        search_word = Search.not_deleted.filter(profile=profile, search_word=query)
        if search_word.exists():
            search_word.update(is_deleted=True)
        Search.objects.create(profile=profile, search_word=query)
