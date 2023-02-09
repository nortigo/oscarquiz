from django.urls import path
from rest_framework import routers

from .views import QuizViewSet, AnswerView, NomineeViewSet, NomineesView

app_name = 'quiz__api'


router = routers.SimpleRouter()
router.register('quiz', QuizViewSet, basename='quiz')
router.register('nominee', NomineeViewSet, basename='nominee')

urlpatterns = router.urls

urlpatterns += [
    path('answer/', AnswerView.as_view(), name='answer'),
    path('nominees/', NomineesView.as_view(), name='nominees'),
]
