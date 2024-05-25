from django.shortcuts import render

# Create your views here.
from django_elasticsearch_dsl_drf.constants import (
    LOOKUP_FILTER_TERMS,
    LOOKUP_FILTER_RANGE,
    LOOKUP_FILTER_PREFIX,
    LOOKUP_FILTER_WILDCARD,
    LOOKUP_QUERY_IN,
    LOOKUP_QUERY_EXCLUDE,
)
from django_elasticsearch_dsl_drf.filter_backends import (
    FilteringFilterBackend,
    OrderingFilterBackend,
    DefaultOrderingFilterBackend,
    SearchFilterBackend,
)
from django_elasticsearch_dsl_drf.viewsets import DocumentViewSet

# Example app models
from avtoelon.documents import AutoDocument
from avtoelon.serializers import AutoDocumentSerializer


class AutoDocumentView(DocumentViewSet):
    """The AutoDocument view."""

    document = AutoDocument
    serializer_class = AutoDocumentSerializer
    lookup_field = "id"
    filter_backends = [
        FilteringFilterBackend,
        OrderingFilterBackend,
        DefaultOrderingFilterBackend,
        SearchFilterBackend,
    ]
    # Define search fields
    search_fields = (
        "brand.title.raw",
        "description",
        "transmission",
        "body_type",
        "engine_fuel",
        "engine_capacity",
        "year",
        "price",
    )
    # # Define filtering fields
    filter_fields = {
        "id": {
            "field": "_id",
            "lookups": [
                LOOKUP_FILTER_RANGE,
                LOOKUP_QUERY_IN,
            ],
        },
        "drive_unit": "drive_unit",
        "description": "description",
        "transmission": "drive_unit",
        "body_type": "body_type",
        "engine_fuel": "body_type",
        "engine_capacity": "engine_capacity",
        "price": "price",
        # "publication_date": "publication_date",
        # "isbn": "isbn.raw",
        # "tags": {
        #     "field": "tags",
        #     "lookups": [
        #         LOOKUP_FILTER_TERMS,
        #         LOOKUP_FILTER_PREFIX,
        #         LOOKUP_FILTER_WILDCARD,
        #         LOOKUP_QUERY_IN,
        #         LOOKUP_QUERY_EXCLUDE,
        #     ],
        # },
        # "tags.raw": {
        #     "field": "tags.raw",
        #     "lookups": [
        #         LOOKUP_FILTER_TERMS,
        #         LOOKUP_FILTER_PREFIX,
        #         LOOKUP_FILTER_WILDCARD,
        #         LOOKUP_QUERY_IN,
        #         LOOKUP_QUERY_EXCLUDE,
        #     ],
        # },
    }
    # Define ordering fields
    ordering_fields = {
        "id": "id",
        # "title": "title.raw",
        # "price": "price.raw",
        # "state": "state.raw",
        # "publication_date": "publication_date",
    }

    # Specify default ordering
    # ordering = (
    #     "id",
    #     "title",
    # )
