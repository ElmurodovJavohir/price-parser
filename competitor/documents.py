from django_elasticsearch_dsl import Document, Index, fields
from django_elasticsearch_dsl.registries import registry
from django_elasticsearch_dsl_drf.analyzers import edge_ngram_completion
from django_elasticsearch_dsl_drf.compat import KeywordField, StringField
from elasticsearch_dsl import analyzer, token_filter, tokenizer

from competitor.models import Competitor, CompetitorProduct

html_strip = analyzer(
    "html_strip",
    tokenizer="standard",
    filter=[
        "lowercase",
        "stop",
        "snowball",
        "porter_stem",
        "unique",
        token_filter("russian_stop", "stop", stopwords="_russian_"),
        token_filter("english_stop", "stop", stopwords="_english_"),
        token_filter("word_joiner", "word_delimiter", preserve_original=1),
        token_filter("word_joiner", "shingle", output_unigrams=True, token_separator=""),
    ],
    char_filter=["html_strip"],
)


@registry.register_document
class ProductDocument(Document):
    name = StringField(
        analyzer=html_strip,
        fields={
            "raw": KeywordField(),
            "suggest": fields.CompletionField(),
            "edge_ngram_completion": StringField(analyzer=edge_ngram_completion),
            "mlt": StringField(analyzer="russian"),
        },
        similarity="my_similarity",
    )
    competitor = fields.ObjectField(
        properties={
            "id": fields.IntegerField(),
            "name": fields.TextField(),
            "url": fields.TextField(),
        }
    )

    class Django:
        model = CompetitorProduct  # The model associated with this Document

        # The fields of the model you want to be indexed in Elasticsearch
        fields = ["id", "url", "image", "price", "is_available"]
        related_models = [Competitor]

    class Index:
        # Name of the Elasticsearch index
        name = "competitor_product"
        # See Elasticsearch Indices API reference for available settings
        settings = {
            "number_of_shards": 1,
            "number_of_replicas": 0,
            "similarity": {
                "my_similarity": {
                    "type": "DFR",
                    "basic_model": "g",
                    "after_effect": "l",
                    "normalization": "h2",
                    "normalization.h2.c": "3.0",
                }
            },
        }
