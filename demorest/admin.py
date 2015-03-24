from django.contrib import admin
from .models import Event, EventInstance, City, Place


def register(model):
    def wrapper(cls):
        admin.site.register(model, cls)
        return cls
    return wrapper


class PlaceInline(admin.StackedInline):
    model = Place
    textfield_size = {('subject',): 150}



class InstanceInline(admin.StackedInline):
    model = EventInstance
    textfield_size = {('subject',): 150}


@register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description')
    search_fields = ('id', 'title', )
    inlines = [InstanceInline]


@register(City)
class CityAdmin(admin.ModelAdmin):
    inlines = [PlaceInline]
