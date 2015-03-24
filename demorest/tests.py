import json

from django.core.urlresolvers import reverse
from django.contrib.gis.geos import Point
from django.test import TestCase
from django.utils.timezone import now
from model_mommy.mommy import make

from .models import Event, EventInstance, Place, City


# TODO: django wont reset postgis database between tests... tests will pass only when running single one
class NestedCreateTestCase(TestCase):
    def test_nested_create(self):
        _now = now()
        data = json.dumps({
            'title': '123',
            'instances': [
                {
                    'start': _now.isoformat(),
                    'end': _now.isoformat(),
                    'place': {
                        'name': 'vaska',
                        'lon': 12.3,
                        'lat': 14.5,
                        'city': {
                            'name': 'Spb'
                        }
                    }
                }
            ]
        })

        response = self.client.post(reverse('event-list'), data, content_type='application/json')

        self.assertEqual(response.status_code, 201)

        self.assertEqual(list(Event.objects.values()), [{'description': None, u'id': 1, 'title': u'123'}])

        instance = {'end': _now, 'event_id': 1, 'id': 1, 'place_id': 1, 'start': _now}
        self.assertEqual(list(EventInstance.objects.values()), [instance])

        place = {'point': Point(12.3, 14.5, srid=4326).hexewkb, 'id': 1, 'city_id': 1, 'name': 'vaska'}
        self.assertEqual(list(Place.objects.values()), [place])

        self.assertEqual(list(City.objects.values()), [{'name': 'Spb', 'id': 1}])


class DistanceQueryTestCase(TestCase):
    def test_distance_query(self):
        make(EventInstance, event__title='near', place__point=Point(12.3, 14.5, srid=4326))
        make(EventInstance, event__title='too far', place__point=Point(13.3, 16.5, srid=4326))

        query = {'lon': 12.30001, 'lat': 14.50001, 'radius': 5, 'per_page': 1, 'page': 1}
        response = self.client.get(reverse('event-geosearch'), query)

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        expected_data = {
            'pagination': {'has_next': False, u'has_prev': False},
            'data': [{'description': None, 'id': 1, 'title': 'near'}]
        }
        self.assertEqual(data, expected_data)

