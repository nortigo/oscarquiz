from django.urls import path, include


app_name = 'api'

urlpatterns = [
    path('', include('account.api.urls', namespace='account')),
    path('', include('quiz.api.urls', namespace='quiz')),
]
