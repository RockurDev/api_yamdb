from rest_framework import filters, mixins, viewsets


class GenreCategoryBaseViewSet(
        mixins.ListModelMixin,
        mixins.CreateModelMixin,
        mixins.DestroyModelMixin,
        viewsets.GenericViewSet,
):
    """Mixin class for genre, category viewsets."""

    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ['name']
