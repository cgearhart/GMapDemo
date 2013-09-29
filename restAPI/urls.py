from django.conf.urls import patterns, url
from restAPI import views

# TODO: https://docs.djangoproject.com/en/dev/topics/http/urls/#named-groups
# Use named groups to parameterize queries on the view sets (test to see if
# it applies all parameters as filters, e.g.) to search for things like
# "color", etc.

urlpatterns = patterns('',
    url(r'^stations/$', views.StationList.as_view()),
)
