from django.test import TestCase
from django.utils import timezone

from service.types import ValidationStatus
from service.views import validate_order


class ValidateTests(TestCase):

    def test_valid_limit_order(self):
        time = timezone.now()
        _, resp = validate_order(dict(
            id="id1",
            account="account_1",
            portfolio="portfolio_1",
            security="GOOG",
            order_type="LIMIT",
            limit_price=1500,
            price=2000,
            time_created=time,
            time_approved=time,
        ))
        self.assertEqual(resp.validated_data["validation_status"], ValidationStatus.VALID.name)

    def test_valid_market_order(self):
        time = timezone.now()
        _, resp = validate_order(dict(
            id="id1",
            account="account_1",
            portfolio="portfolio_1",
            security="APPL",
            order_type="MARKET",
            price=2000,
            time_created=time,
            time_approved=time,
        ))
        self.assertEqual(resp.validated_data["validation_status"], ValidationStatus.VALID.name)

    def test_borderline_market_order(self):
        time = timezone.now()
        _, resp = validate_order(dict(
            id="id1",
            account="account_1",
            portfolio="portfolio_1",
            security="GOOG",
            order_type="MARKET",
            limit_price=1500,
            price=2000,
            time_created=time,
            time_approved=time,
        ))
        self.assertEqual(resp.validated_data["validation_status"], ValidationStatus.BORDERLINE.name)

    def test_invalid_limit_order_missing_limit_price(self):
        time = timezone.now()
        _, resp = validate_order(dict(
            id="id1",
            account="account_1",
            portfolio="portfolio_1",
            security="GOOG",
            order_type="LIMIT",
            price=2000,
            time_created=time,
            time_approved=time,
        ))
        self.assertEqual(resp.validated_data["validation_status"], ValidationStatus.INVALID.name)

    def test_invalid_order_type(self):
        time = timezone.now()
        _, resp = validate_order(dict(
            id="id1",
            account="account_1",
            portfolio="portfolio_1",
            security="GOOG",
            order_type="random",
            price=2000,
            time_created=time,
            time_approved=time,
        ))
        self.assertEqual(resp.validated_data["validation_status"], ValidationStatus.INVALID.name)

    def test_invalid_security(self):
        time = timezone.now()
        _, resp = validate_order(dict(
            id="id1",
            account="account_1",
            portfolio="portfolio_1",
            security="RAND",
            order_type="MARKET",
            price=2000,
            time_created=time,
            time_approved=time,
        ))
        self.assertEqual(resp.validated_data["validation_status"], ValidationStatus.INVALID.name)

    def test_invalid_price_and_quantity(self):
        time = timezone.now()
        _, resp = validate_order(dict(
            id="id1",
            account="account_1",
            portfolio="portfolio_1",
            security="RAND",
            order_type="MARKET",
            price=2000,
            quantity=5,
            time_created=time,
            time_approved=time,
        ))
        self.assertEqual(resp.validated_data["validation_status"], ValidationStatus.INVALID.name)
