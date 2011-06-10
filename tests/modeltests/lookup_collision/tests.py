from datetime import datetime
from django.test import TestCase
from models import RepeatingEvent, Appointment, Calendar


class LookupCollisionTests(TestCase):
    """Test for collisions between lookup type names and field names"""

    def setUp(self):
        # Create a RepeatingEvent
        self.rep1 = RepeatingEvent(name="Every Thursday", week_day=5)
        self.rep1.save()
        # Create an Appointment
        self.ap1 = Appointment(name="Today and every thursday", day=datetime(2011, 6, 9), repeating=self.rep1)
        self.ap1.save()
        # Create a Calendar
        self.cal = Calendar(name="My Calendar")
        self.cal.save()
        self.cal.appointments = [self.ap1, ]
        self.cal.save()

    def test_query_simple(self):
        """Test simple queries with colliding names without traversing relations"""
        self.assertTrue(RepeatingEvent.objects.filter(week_day=5).exists())
        self.assertTrue(Appointment.objects.filter(day=datetime(2011, 6, 9)).exists())

    def test_query_related(self):
        """Test queries through related fields with colliding field names"""
        self.assertTrue(Appointment.objects.filter(repeating__week_day=5).exists())

        self.assertTrue(Calendar.objects.filter(appointments__day=datetime(2011, 6, 9)).exists())
        self.assertTrue(Calendar.objects.filter(appointments__repeating__week_day=5).exists())

    def test_query_related_with_lookup(self):
        """Test queries through related fields with colliding names with explicit lookup types"""
        self.assertTrue(RepeatingEvent.objects.filter(week_day__exact=5).exists())

        self.assertTrue(Appointment.objects.filter(day__exact=datetime(2011, 6, 9)).exists())
        self.assertTrue(Appointment.objects.filter(day__week_day=5).exists())
        self.assertTrue(Appointment.objects.filter(repeating__week_day__exact=5).exists())

        self.assertTrue(Calendar.objects.filter(appointments__day__exact=datetime(2011, 6, 9)).exists())
        self.assertTrue(Calendar.objects.filter(appointments__day__week_day=5).exists())
        self.assertTrue(Calendar.objects.filter(appointments__repeating__week_day__exact=5).exists())
