from drf_rw_serializers import viewsets as drf

from kalendario.common.mixins import RenderParserPaginationMixin


class GenericViewSet(RenderParserPaginationMixin, drf.GenericViewSet):
    pass


class ModelViewSet(RenderParserPaginationMixin, drf.ModelViewSet):
    pass


class ReadOnlyModelViewSet(RenderParserPaginationMixin, drf.ReadOnlyModelViewSet):
    pass


class ReadCreateOnlyModelViewSet(RenderParserPaginationMixin,
                                 drf.CreateModelMixin,
                                 drf.ReadOnlyModelViewSet):
    pass


class RetrieveUpdateModelViewSet(drf.RetrieveModelMixin,
                                 drf.UpdateModelMixin,
                                 GenericViewSet):
    pass
