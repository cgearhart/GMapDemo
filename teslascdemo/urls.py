from django.conf.urls import patterns, include, url

from django.views.generic import RedirectView, TemplateView

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()


# needed to link rest_framework to registration views - allows login/logout from browsable API
authpatterns = patterns('django.contrib.auth.views',
    url(r'^login/$', 'login', {'template_name': 'registration/login.html'}, name='login'),
    url(r'^logout/$', 'logout', {'template_name': 'registration/logout.html'}, name='logout'),
)

urlpatterns = patterns('',
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    # link chiselRegistration (django-registration backend) to account management
    url(r'^accounts/', include('emailRegistration.urls')),

    # link rest_framework to registration views - allows login/logout from browsable API
    url(r'^accounts/', include(authpatterns, namespace='rest_framework')),

    # Redirect all requests to the restAPI url patterns
    url(r'^', include('restAPI.urls')),

    url(r'index.html', TemplateView.as_view(template_name='index.html')),

    # redirect requests to the base url to the suggested page instead
    url(r'^$', RedirectView.as_view(url='stations/')),
)
