from django.urls import path
from rest_framework import routers

from .views import QuizViewSet, AnswerViewSet, NomineeViewSet, NomineesView

app_name = 'quiz__api'


router = routers.SimpleRouter()
router.register('quiz', QuizViewSet, basename='quiz')
router.register('answer', AnswerViewSet, basename='answer')
router.register('nominee', NomineeViewSet, basename='nominee')

urlpatterns = router.urls

urlpatterns += [path('nominees/', NomineesView.as_view(), name='nominees')]
