from django_elasticsearch_dsl import Document, Index, fields
from django_elasticsearch_dsl_drf.compat import KeywordField, StringField
from django_elasticsearch_dsl.registries import registry
from avtoelon.models import Auto


@registry.register_document
class AutoDocument(Document):
    class Index:
        # Name of the Elasticsearch index
        name = "auto"
        # See Elasticsearch Indices API reference for available settings
        settings = {"number_of_shards": 1, "number_of_replicas": 0}

    class Django:
        model = Auto
        queryset_pagination = 10000

    drive_unit = StringField(
        fields={
            "raw": KeywordField(),
            "suggest": fields.CompletionField(),
        },
    )

    transmission = StringField(
        fields={
            "raw": KeywordField(),
            "suggest": fields.CompletionField(),
        },
    )
    body_type = StringField(
        fields={
            "raw": KeywordField(),
            "suggest": fields.CompletionField(),
        },
    )
    engine_fuel = StringField(
        fields={
            "raw": KeywordField(),
            "suggest": fields.CompletionField(),
        },
    )
    engine_capacity = StringField(
        fields={
            "raw": KeywordField(),
            "suggest": fields.CompletionField(),
        },
    )
    year = fields.IntegerField()
    price = fields.IntegerField()
    link = fields.ObjectField(
        properties={
            "link": StringField(
                fields={
                    "raw": KeywordField(),
                    "suggest": fields.CompletionField(),
                },
            ),
            "is_parsed": fields.BooleanField(),
        }
    )
    brand = fields.ObjectField(
        properties={
            "title": StringField(
                fields={
                    "raw": KeywordField(),
                    "suggest": fields.CompletionField(),
                },
            ),
        }
    )
    model = fields.ObjectField(
        properties={
            "title": StringField(
                fields={
                    "raw": KeywordField(),
                    "suggest": fields.CompletionField(),
                },
            ),
        }
    )
    position = fields.ObjectField(
        properties={
            "title": StringField(
                fields={
                    "raw": KeywordField(),
                    "suggest": fields.CompletionField(),
                },
            ),
        }
    )
    city = fields.ObjectField(
        properties={
            "title": StringField(
                fields={
                    "raw": KeywordField(),
                    "suggest": fields.CompletionField(),
                },
            ),
        }
    )
