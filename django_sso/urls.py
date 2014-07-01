from django.conf.urls import patterns, include, url

from django.contrib import admin
from django_sso.views import check_username_password

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'django_sso.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^saml2/', include('djangosaml2.urls')),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^check-user/(?P<username>[0-9A-Za-z]+)/(?P<password>[0-9A-Za-z]+)$', check_username_password),
    (r'^rest-auth/', include('rest_auth.urls')),
    #url(r'^accounts/', include()),
)
