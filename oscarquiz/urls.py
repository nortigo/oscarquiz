# -*- coding: utf-8 -*-
from django.conf.urls import url
from django.contrib import admin

from .views import IndexView, QuizView

urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^quiz/(?P<quiz_id>\d+)/$', QuizView.as_view(), name='quiz'),
    url(r'^admin/', admin.site.urls),
]
