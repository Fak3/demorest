
from django.contrib.gis.geos import Point
from rest_framework.serializers import ModelSerializer, SerializerMethodField

from .models import Event, EventInstance, Place, City

class CitySerializer(ModelSerializer):
    class Meta:
        model = City
        fields = ('id', 'name',)


class PlaceSerializer(ModelSerializer):
    city = CitySerializer()
    lon = SerializerMethodField()
    lat = SerializerMethodField()

    class Meta:
        model = Place
        fields = ('id', 'name', 'lon', 'lat', 'city')

    def get_lon(self, obj):
        return obj.point.x

    def get_lat(self, obj):
        return obj.point.y

    def to_internal_value(self, data):
        point = Point(data.pop('lon'), data.pop('lat'))
        result = super(PlaceSerializer, self).to_internal_value(data)
        return dict(result, point=point)


class InstanceSerializer(ModelSerializer):
    place = PlaceSerializer()

    class Meta:
        model = EventInstance
        fields = ('start', 'end', 'place')


class EventSerializer(ModelSerializer):
    instances = InstanceSerializer(many=True, required=False)

    class Meta:
        model = Event
        fields = ('id', 'title', 'description', 'instances')

    def __init__(self, *args, **kwargs):
        many = args and hasattr(args[0], '__iter__')
        super(EventSerializer, self).__init__(*args, **kwargs)
        if many:
            # Events list should not have details of instances.
            self.fields.pop('instances', None)

    def create(self, validated_data):
        instances = validated_data.pop('instances', [])
        event = Event.objects.create(**validated_data)
        for instance in instances:
            place = instance.pop('place')
            city, _ = City.objects.get_or_create(name=place.pop('city')['name'])
            place, _ = Place.objects.get_or_create(city=city, **place)

            EventInstance.objects.get_or_create(event=event, place=place, **instance)
        return event
