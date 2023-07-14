from elasticsearch_dsl import Q

from competitor.documents import ProductDocument
from competitor.models import CompetitorProduct
from product.models import Product


def match_competitor_product():
    from django.core.management import call_command

    call_command("search_index", "--rebuild", "-f")
    products = Product.objects.all()
    for product in products:
        product_indexs = ProductDocument.search().query(
            "bool",
            should=[
                Q(
                    {
                        "match": {
                            "name": {
                                "query": product.name,
                                "fuzziness": "auto",
                                "minimum_should_match": "100%",
                                
                            }
                        }
                    }  # type: ignore
                )
            ],
        )[:10]
        product_competitors = {}
        for product_index in product_indexs:
            if product_index["competitor"]["id"] not in product_competitors:
                product_competitors[product_index["competitor"]["id"]] = product_index["id"]

        competitor_products = CompetitorProduct.objects.filter(id__in=product_competitors.values())
        product.competitor_products.set(competitor_products)
