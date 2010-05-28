from django.test import TestCase
from models import Article

class DateQuerySetTest(TestCase):
    fixtures = ['datequeryset_test.json']
    
    def testDatesHoursMinutes(self):
        res = Article.objects.dates('pub_date', 'hour')
        self.assertEqual(repr(res), "[datetime.datetime(2010, 5, 28, 10, 0)]")

        res = Article.objects.dates('pub_date', 'minute')
        self.assertEqual(repr(res), "[datetime.datetime(2010, 5, 28, 10, 15)]")
