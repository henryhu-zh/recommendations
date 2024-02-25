"""
Test cases for Pet Model
"""

import os
import logging
from unittest import TestCase
from wsgi import app
from service.models import Recommendation, RecommendationType, DataValidationError, db
from tests.factories import RecommendationFactory

DATABASE_URI = os.getenv(
    "DATABASE_URI",
    "postgresql+psycopg://postgres:postgres@localhost:5432/recommendationdb",
)


######################################################################
#  R E C O M M E N D A T I O N   M O D E L   T E S T   C A S E S
######################################################################
# pylint: disable=too-many-public-methods
class TestRecommendation(TestCase):
    """Test Cases for Recommendation Model"""

    @classmethod
    def setUpClass(cls):
        """This runs once before the entire test suite"""
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        app.app_context().push()

    @classmethod
    def tearDownClass(cls):
        """This runs once after the entire test suite"""
        db.session.close()

    def setUp(self):
        """This runs before each test"""
        db.session.query(Recommendation).delete()  # clean up the last tests
        db.session.commit()

    def tearDown(self):
        """This runs after each test"""
        db.session.remove()

    ######################################################################
    #  T E S T   C A S E S
    ######################################################################

    def test_recommendation_type_values(self):
        """It should contain all desired types of recommendation"""
        target_values = ["UP_SELL", "CROSS_SELL", "ACCESSORY", "BUNDLE"]
        values = [type.value for type in RecommendationType]
        for target_value in target_values:
            self.assertTrue(target_value in values)

    def test_create_recommendation(self):
        """It should Create a recommendation and assert that it exists"""
        recommendation = Recommendation(
            product_a_sku="AA0001",
            product_b_sku="AA0002",
            type=RecommendationType.UP_SELL,
        )
        self.assertEqual(
            str(recommendation), "<Recommendation AA0001-AA0002 id=[None]>"
        )
        self.assertTrue(recommendation is not None)
        self.assertEqual(recommendation.id, None)
        self.assertEqual(recommendation.product_a_sku, "AA0001")
        self.assertEqual(recommendation.product_b_sku, "AA0002")
        self.assertEqual(recommendation.type, RecommendationType.UP_SELL)

        # test new recommendation
        recommendation = Recommendation(
            product_a_sku="AB1111",
            product_b_sku="BA2222",
            type=RecommendationType.CROSS_SELL,
        )
        self.assertEqual(recommendation.product_a_sku, "AB1111")
        self.assertEqual(recommendation.product_b_sku, "BA2222")
        self.assertEqual(recommendation.type, RecommendationType.CROSS_SELL)

    def test_add_recommendation(self):
        """It should create a recommendation and add it to the database"""
        recommendations = Recommendation.all()
        self.assertEqual(recommendations, [])
        recommendation = Recommendation(
            product_a_sku="A1", product_b_sku="B1", type=RecommendationType.UP_SELL
        )
        self.assertTrue(recommendation is not None)
        self.assertEqual(recommendation.id, None)
        recommendation.create()

        # Assert that it was assigned an id and shows up in the database
        self.assertIsNotNone(recommendation.id)
        recommendations = Recommendation.all()
        self.assertEqual(len(recommendations), 1)
        self.assertEqual(recommendations[0].product_a_sku, "A1")
        self.assertEqual(recommendations[0].product_b_sku, "B1")
        self.assertEqual(recommendations[0].type, RecommendationType.UP_SELL)

    def test_read_recommendation(self):
        """It should Read a Recommendation"""
        recommendation = RecommendationFactory()
        logging.debug(recommendation)
        recommendation.id = None
        recommendation.create()
        self.assertIsNotNone(recommendation.id)

        # Fetch it back
        found_recommendation = Recommendation.find(recommendation.id)
        self.assertEqual(found_recommendation.id, recommendation.id)
        self.assertEqual(
            found_recommendation.product_a_sku, recommendation.product_a_sku
        )
        self.assertEqual(
            found_recommendation.product_b_sku, recommendation.product_b_sku
        )
        self.assertEqual(found_recommendation.type, recommendation.type)
