from django.conf.urls import patterns, include, url

import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'MentorFinder2.views.home', name='home'),
    # url(r'^MentorFinder2/', include('MentorFinder2.foo.urls')),
    url(r'^$', views.get_entry, name='get_entry'),

    )