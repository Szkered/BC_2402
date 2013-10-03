"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".
"""

from django.test import TestCase
from django.core.urlresolvers import reverse
import datetime
from django.utils import timezone

def mock_donation(stock_name, unit_measure, unit_price, quantity):
    """
    Simulate an instance of donation
    """
    s = Stock.objects.create(name=stock_name,
                         unit_measure=unit_measure,
                         unit_price=unit_price)
    d = Donor.objects.get_or_create(name="Joe",
                                address="xxx",
                                contact_no=87654321,
                                mailing=True,
                                referral='A') 
    return Donate.objects.create(date=timezone.now(),
                                 quantity=quantity,
                                 stock_id=s,
                                 donor_id=d)

class test_purchase_sum(TestCase):
    def test_purchase_sum_with_donations(self):
        




