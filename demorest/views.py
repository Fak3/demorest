
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import D
from django.views.generic import TemplateView

from rest_framework import viewsets
from rest_framework.decorators import list_route
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

from .models import Event
from .serializers import EventSerializer


class NextPrevPagination(PageNumberPagination):
    page_size = 1
    page_size_query_param = 'per_page'
    max_page_size = 100

    def get_paginated_response(self, data):
        return Response({
            #'count': self.page.paginator.count,
            'pagination': {
                'has_next': bool(self.get_next_link()),
                'has_prev': bool(self.get_previous_link())
            },
            'data': data
        })


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    pagination_class = NextPrevPagination

    @list_route()
    def geosearch(self, request, *args, **kwargs):
        center = Point(float(request.query_params.get('lon')), float(request.query_params.get('lat')), srid=4326)
        radius_km = request.query_params.get('radius')
        queryset = Event.objects.filter(instances__place__point__distance_lte=(center, D(km=radius_km)))
        queryset = self.paginate_queryset(queryset)
        serializer = EventSerializer(queryset, many=True)
        return self.get_paginated_response(serializer.data)


class EventsListView(TemplateView):
    template_name = 'events_list.html'
