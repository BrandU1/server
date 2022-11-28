from rest_framework import serializers

from search.models import Search


class SearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Search
        fields = ['id', 'created', 'search_word']


class SearchRankSerializer(serializers.ModelSerializer):
    count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Search
        fields = ['count', 'search_word']
