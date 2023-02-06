from rest_framework import routers

from .views import QuizViewSet, AnswerViewSet, NomineeViewSet

app_name = 'quiz__api'


router = routers.SimpleRouter()
router.register('quiz', QuizViewSet, basename='quiz')
router.register('answer', AnswerViewSet, basename='answer')
router.register('nominee', NomineeViewSet, basename='nominee')

urlpatterns = router.urls
