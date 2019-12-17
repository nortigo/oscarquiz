# -*- coding: utf-8 -*-
from django.urls import path
from django.contrib import admin
from oscarquiz.views import IndexView, QuizView, ResultsView


admin.site.site_header = "Oscar Quiz Admin"
admin.site.site_title = "Oscar Quiz Admin Portal"


urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('quiz/<uuid:identifier>/', QuizView.as_view(), name='quiz'),
    path('results/<int:quiz_id>/', ResultsView.as_view(), name='results'),
    path('admin/', admin.site.urls),
]
