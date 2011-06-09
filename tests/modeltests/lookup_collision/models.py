from django.db import models, DEFAULT_DB_ALIAS, connection
from django.conf import settings

class RepeatingEvent(models.Model):
    name = models.CharField(max_length=100)
    week_day = models.IntegerField()
    class Meta:
        ordering = ('week_day', 'name', )

class Appointment(models.Model):
    name = models.CharField(max_length=100)
    day = models.DateField()
    repeating = models.ForeignKey(RepeatingEvent)
    class Meta:
        ordering = ('day', 'name', )

class Calendar(models.Model):
    name = models.CharField(max_length=100)
    appointments = models.ManyToManyField(Appointment)
    class Meta:
        ordering = ('name',)

    def __unicode__(self):
        return self.name
