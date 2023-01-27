from rest_framework import routers

from .views import QuizViewSet, AnswerViewSet

app_name = 'quiz__api'


router = routers.SimpleRouter()
router.register('quiz', QuizViewSet, basename='quiz')
router.register('answer', AnswerViewSet, basename='answer')

urlpatterns = router.urls
