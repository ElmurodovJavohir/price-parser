from django_elasticsearch_dsl_drf.serializers import DocumentSerializer

from avtoelon.documents import AutoDocument


class AutoDocumentSerializer(DocumentSerializer):
    """Serializer for address document."""

    class Meta:
        """Meta options."""

        document = AutoDocument
        fields = "__all__"
