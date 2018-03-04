# -*- coding: utf-8 -*-
from django.urls import path
from django.contrib import admin
from oscarquiz.views import IndexView, QuizView, ResultsView


urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('quiz/<uuid:identifier>/', QuizView.as_view(), name='quiz'),
    path('results/<int:quiz_id>/', ResultsView.as_view(), name='results'),
    path('admin/', admin.site.urls),
]
