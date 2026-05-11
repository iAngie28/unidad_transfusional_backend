from django.db.models import Q
from rest_framework import permissions


class AuthenticatedViewSetMixin:
    permission_classes = [permissions.IsAuthenticated]


class AuditoriaViewSetMixin(AuthenticatedViewSetMixin):
    def perform_create(self, serializer):
        model = getattr(getattr(serializer, "Meta", None), "model", None)
        tiene_created_by = (
            model is not None
            and any(field.name == "created_by" for field in model._meta.fields)
        )

        if tiene_created_by:
            serializer.save(created_by=self.request.user)
            return

        serializer.save()


class SearchableQuerySetMixin:
    model = None
    search_param = "search"
    search_fields = ()
    select_related_fields = ()
    prefetch_related_fields = ()
    ordering_fields = ()

    def get_base_queryset(self):
        if self.model is not None:
            queryset = self.model.objects.all()
        else:
            queryset = super().get_queryset()

        if self.select_related_fields:
            queryset = queryset.select_related(*self.select_related_fields)

        if self.prefetch_related_fields:
            queryset = queryset.prefetch_related(*self.prefetch_related_fields)

        if self.ordering_fields:
            queryset = queryset.order_by(*self.ordering_fields)

        return queryset

    def get_search_query(self, search):
        query = Q()
        for field in self.search_fields:
            query |= Q(**{f"{field}__icontains": search})
        return query

    def get_queryset(self):
        queryset = self.get_base_queryset()
        search = self.request.query_params.get(self.search_param)

        if search and self.search_fields:
            queryset = queryset.filter(self.get_search_query(search))

        return queryset
