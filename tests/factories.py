"""
Test Factory to make fake objects for testing
"""

import factory
from factory.fuzzy import FuzzyChoice, FuzzyText, FuzzyInteger
from service.models import Recommendation, RecommendationType


class RecommendationFactory(factory.Factory):
    """Creates fake recommendations"""

    class Meta:  # pylint: disable=too-few-public-methods
        """Maps factory to data model"""

        model = Recommendation

    id = factory.Sequence(lambda n: n)
    product_a_sku = FuzzyText(length=8)
    product_b_sku = FuzzyText(length=8)
    recommendation_type = FuzzyChoice(choices=RecommendationType)
    likes = FuzzyInteger(low=0)
