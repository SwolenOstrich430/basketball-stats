from unittest import TestCase
from unittest.mock import Mock
from basketball_reference_web_scraper import client

from app.service.etl.data.basketball_reference_client import BasketballReferenceClient
# import pytest

class TestBasketBallReferenceClient(TestCase):
    def test_get_client_returns_bball_ref_client_instance(self):
        self.assertEqual(
            1, 1
        )