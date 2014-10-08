from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'patternsite.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'comfyapp.views.home', name='home'),
  # url(r'^home/', 'comfyapp.views.home', name='home'),
    url(r'^add/', 'comfyapp.views.add', name='add'),
    url(r'^nope/', 'comfyapp.views.nope', name='nope'),

)
