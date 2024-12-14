from .views import *
from rest_framework import routers
from django.urls import path, include

router = routers.SimpleRouter()
router.register(r'user', UserViewSet, basename='users')
router.register(r'category', CategoryViewSet, basename='category')
router.register(r'lesson', LessonViewSet, basename='lessons')
router.register(r'assignment', AssignmentViewSet, basename='assignments')
router.register(r'exam', ExamViewSet, basename='exams')
router.register(r'certificate', CertificateViewSet, basename='certificate')
router.register(r'review', ReviewViewSet, basename='reviews')


urlpatterns = [
    path('', include(router.urls)),
    path('course/', CourseListAPIVew.as_view(), name='course_list'),
    path('course/<int:pk>/', CourseDetailAPIVew.as_view(), name='course_detail'),
    path('questions/', QuestionView.as_view(), name='question-list'),  # Получение вопросов или создание нового
    path('check_answer/', CheckAnswerView.as_view(), name='check-answer'),  # Проверка ответа
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
