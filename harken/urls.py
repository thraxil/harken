from django.conf.urls.defaults import *
from django.contrib import admin
from django.conf import settings
from django.views.generic.simple import direct_to_template
import os.path
admin.autodiscover()
import staticmedia

site_media_root = os.path.join(os.path.dirname(__file__),"../media")

redirect_after_logout = getattr(settings, 'LOGOUT_REDIRECT_URL', None)
auth_urls = (r'^accounts/',include('django.contrib.auth.urls'))
logout_page = (r'^accounts/logout/$','django.contrib.auth.views.logout', {'next_page': redirect_after_logout})
if hasattr(settings,'WIND_BASE'):
    auth_urls = (r'^accounts/',include('djangowind.urls'))
    logout_page = (r'^accounts/logout/$','djangowind.views.logout', {'next_page': redirect_after_logout})

urlpatterns = patterns('',
                       # Example:
                       # (r'^harken/', include('harken.foo.urls')),
		       auth_urls,
		       logout_page,
                       (r'^$', 'harken.main.views.index'),
                       (r'^add/$', 'harken.main.views.add'),
                       (r'^search/$', 'harken.main.views.search'),

                       (r'^response/date/(?P<year>\d{4})/$',
                        'harken.main.views.response_year_archive'),
                       (r'^response/date/(?P<year>\d{4})/(?P<month>\d{2})/$',
                        'harken.main.views.response_month_archive'),
                       (r'^response/date/(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/$',
                        'harken.main.views.response_day_archive'),

                       (r'^response/(?P<id>\d+)/$', 'harken.main.views.response'),
                       (r'^response/(?P<id>\d+)/raw/$',
                        'harken.main.views.response_raw'),
                       (r'^response/(?P<id>\d+)/patch/$',
                        'harken.main.views.response_patch'),
                       (r'^response/(?P<id>\d+)/delete/$',
                        'harken.main.views.delete_response'),
                       (r'^url/(?P<id>\d+)/delete/$',
                        'harken.main.views.delete_url'),
                       (r'^domain/(?P<id>\d+)/delete/$',
                        'harken.main.views.delete_domain'),
                       (r'^url/(?P<id>\d+)/$',
                        'harken.main.views.url_view'),
                       (r'^domain/$',
                        'harken.main.views.domain_index'),
                       (r'^domain/(?P<id>\d+)/$',
                        'harken.main.views.domain'),

                       (r'term/(?P<id>\d+)/$', 'harken.main.views.term'),
                       (r'term/$', 'harken.main.views.term_index'),
                       (r'^term/(?P<id>\d+)/delete/$',
                        'harken.main.views.delete_term'),

                       (r'^admin/', include(admin.site.urls)),
                       (r'^munin/',include('munin.urls')),
											 (r'^stats/', direct_to_template, {'template': 'stats.html'}),
                       (r'^site_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': site_media_root}),
                       (r'^uploads/(?P<path>.*)$','django.views.static.serve',{'document_root' : settings.MEDIA_ROOT}),
) + staticmedia.serve()

