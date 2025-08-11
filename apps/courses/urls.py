from django.urls import path

from apps.courses.views import *


urlpatterns = [
    # Course
    path('course/list/', CourseListAPIVIew.as_view(), name='course-list'),
    path('course/create/', CourseCreatAPIView.as_view(), name='course-create'),
    path('course/update/<int:id>/', CourseUpdateAPIView.as_view(), name='update-course'),
    path('course/delete/<int:id>/', CourseDeleteAPIView.as_view(), name='delete-course'),

    # Webinar
    path('webinar/list/', WebinarListAPIVIew.as_view(), name='webinar-list'),
    path('webinar/create/', WebinarCreatAPIView.as_view(), name='webinar-create'),
    path('webinar/update/<int:id>/', WebinarUpdateAPIView.as_view(), name='update-webinar'),
    path('webinar/delete/<int:id>/', WebinarDeleteAPIView.as_view(), name='delete-webinar'),

    # Lesson
    path('lesson/list/', LessonListAPIVIew.as_view(), name='lesson-list'),
    path('lesson/create/', LessonCreatAPIView.as_view(), name='lesson-create'),
    path('lesson/update/<int:id>/', LessonUpdateAPIView.as_view(), name='update-lesson'),
    path('lesson/delete/<int:id>/', LessonDeleteAPIView.as_view(), name='delete-lesson'),

    # Category
    path('category/list/', CategoryListAPIVIew.as_view(), name='category-list'),
    path('category/create/', CategoryCreatAPIView.as_view(), name='category-create'),
    path('category/delete/<int:id>/', CategoryDeleteAPIView.as_view(), name='delete-category'),

    # Comment
    path('comment/list/', CommentListAPIVIew.as_view(), name='comment-list'),
    path('comment/create/', CommentCreatAPIView.as_view(), name='comment-create'),
    path('comment/delete/<int:id>/', CommentDeleteAPIView.as_view(), name='delete-comment'),
]