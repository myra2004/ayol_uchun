from django.urls import path

from apps.news.views import *

app_name = "news"


urlpatterns = [
    # Post
    path('post/list/', PostListAPIView.as_view(), name='post-list'),
    path('post/create/', PostCreateAPIView.as_view(), name='post-create'),
    path('post/update/<int:id>/', PostUpdateAPIView.as_view(), name='post-update'),
    path('post/delete/<int:id>/', PostDeleteAPIView.as_view(), name='post-delete'),

    # Event
    path('event/list/', EventListAPIView.as_view(), name='event-list'),
    path('event/create/', EventCreateAPIView.as_view(), name='event-create'),
    path('event/update/<int:id>/', EventUpdateAPIView.as_view(), name='event-update'),
    path('event/delete/<int:id>/', EventDeleteAPIView.as_view(), name='event-delete'),

    # Survey
    path('survey/list/', SurveyListAPIView.as_view(), name='survey-list'),
    path('survey/create/', SurveyCreateAPIView.as_view(), name='survey-create'),
    path('survey/update/<int:id>/', SurveyUpdateAPIView.as_view(), name='survey-update'),
    path('survey/delete/<int:id>/', SurveyDeleteAPIView.as_view(), name='survey-delete'),

    # Question
    path('question/list/', QuestionListAPIView.as_view(), name='question-list'),
    path('question/create/', QuestionCreateAPIView.as_view(), name='question-create'),
    path('question/update/<int:id>/', QuestionUpdateAPIView.as_view(), name='question-update'),
    path('question/delete/<int:id>/', QuestionDeleteAPIView.as_view(), name='question-delete'),

    # Question Option
    path('question-option/list/', QuestionOptionListAPIView.as_view(), name='question-option-list'),
    path('question-option/create/', QuestionOptionCreateAPIView.as_view(), name='question-option-create'),
    path('question-option/update/<int:id>/', QuestionOptionUpdateAPIView.as_view(), name='question-option-update'),
    path('question-option/delete/<int:id>/', QuestionOptionDeleteAPIView.as_view(), name='question-option-delete'),

    # Submission
    path('submission/list/', SubmissionListAPIView.as_view(), name='submission-list'),
    path('submission/create/', SubmissionCreateAPIView.as_view(), name='submission-create'),
    path('submission/delete/<int:id>/', SubmissionDeleteAPIView.as_view(), name='submission-delete')
]