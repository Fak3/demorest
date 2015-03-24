from django.db.models import Model, DateTimeField, TextField, ManyToManyField, ForeignKey, FloatField
from django.contrib.gis.db.models import PointField


class EventCategory(Model):
    name = TextField()


class Event(Model):
    title = TextField()
    description = TextField(null=True, blank=True)
    categories = ManyToManyField('EventCategory', blank=True)


class EventInstance(Model):
    event = ForeignKey('Event', related_name='instances')
    start = DateTimeField()
    end = DateTimeField()
    place = ForeignKey('Place')


class Place(Model):
    city = ForeignKey('City')
    name = TextField()
    point = PointField()
    #lon = FloatField()
    #lat = FloatField()


class City(Model):
    name = TextField()
