from django_filters import rest_framework as drf

from reviews.models import Title


class SlugFilter(drf.FilterSet):
    category = drf.CharFilter(field_name='category__slug', lookup_expr='exact')
    genre = drf.CharFilter(field_name='genre__slug', lookup_expr='exact')

    class Meta:
        model = Title
        fields = ['name', 'year', 'category', 'genre']
