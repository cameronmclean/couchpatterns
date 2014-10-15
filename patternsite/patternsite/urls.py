from django.conf.urls import patterns, include, url
from django.contrib import admin, auth

#from django.contrib import 

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'patternsite.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'comfyapp.views.home', name='home'),
  # url(r'^home/', 'comfyapp.views.home', name='home'),
    url(r'^add/', 'comfyapp.views.add', name='add'),
    url(r'^nope/', 'comfyapp.views.nope', name='nope'),
    url(r'^accounts/', include('registration.backends.default.urls')),
#	below added to patch url config for registration and django 1.6+
	url(r'^password/change/$', auth.views.password_change, name='password_change'),
	url(r'^password/change/done/$', auth.views.password_change_done, name='password_change_done'),
	url(r'^password/reset/$', auth.views.password_reset, name='password_reset'),
	url(r'^accounts/password/reset/done/$', auth.views.password_reset_done, name='password_reset_done'),
	url(r'^password/reset/complete/$', auth.views.password_reset_complete, name='password_reset_complete'),
	url(r'^password/reset/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$', auth.views.password_reset_confirm, name='password_reset_confirm'),

)
