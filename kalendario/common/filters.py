from rest_framework import filters


class OwnerFilter(filters.BaseFilterBackend):

    def filter_queryset(self, request, queryset, view):
        if request.user.owner_id is None:
            return None
        if queryset.model.__name__ == 'Company':
            return queryset.filter(id=request.user.owner_id)
        return queryset.filter(owner_id=request.user.owner_id)
