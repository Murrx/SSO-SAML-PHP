from django.conf.urls import patterns, include, url
from django.conf.urls.static import static

from django.contrib import admin
from django_sso import settings
from django_sso.views import check_username_password, Home, check_token


admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'django_sso.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
#    url(r'^saml2/', include('djangosaml2.urls')),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^check-user/(?P<username>[0-9A-Za-z_@#$-.]+)/(?P<password>[0-9A-Za-z_@#$-]+)$', check_username_password),
    url(r'^check-token/', check_token),
    (r'^rest-auth/', include('rest_auth.urls')),
    url(r'^$', Home.as_view() ),
    #url(r'^accounts/', include()),
)+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
