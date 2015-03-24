from django.conf.urls import patterns, include, url
from rest_framework.routers import DefaultRouter

from . import views


router = DefaultRouter()
router.register(r'events', views.EventViewSet)


from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',
    url(r'^$', views.EventsListView.as_view(), name="homepage"),
    url(r'^api/1.0/', include(router.urls)),

    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
