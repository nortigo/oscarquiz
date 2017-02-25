# -*- coding: utf-8 -*-
from django.conf.urls import url
from django.contrib import admin

from .views import IndexView, QuizView, ResultsView

urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^quiz/(?P<quiz_id>\d+)/(?P<player_id>\d+)/$', QuizView.as_view(), name='quiz'),
    url(r'^results/(?P<quiz_id>\d+)/$', ResultsView.as_view(), name='results'),
    url(r'^admin/', admin.site.urls),
]
