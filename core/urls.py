from django.urls import path, include
from core import views as core_views
from django.conf.urls import handler404, handler500
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

handler404 = 'core.views.error_404'
handler500 = 'core.views.error_500'

urlpatterns = [
    path('', core_views.home_view,name='home'),
    path('register/',core_views.register,name='register'),
    path('profile/',core_views.profile,name="profile"),
    path('login/',auth_views.LoginView.as_view(template_name='core/login.html'),name='login'),
    path('logout/',auth_views.LogoutView.as_view(),name='logout'),
    path('invite_people/<int:pk>/',core_views.invite_people,name='invite'),
    path('create_class/',core_views.create_class,name='create_class'),
    path('join_class/<int:pk>/<code>/',core_views.join_class,name='join_class'),
    path('classroom/<int:pk>/',core_views.classroom,name='classroom'),
    path('create_question/<int:pk>/',core_views.create_question,name='create_question'),
    path('question-details/<int:pk>/',core_views.question_details,name="question-details"),
    path('answer-short/<int:pk>/',core_views.answer_short,name="answer-short"),
    path('answer-mcq/<int:pk>/',core_views.answer_mcq,name="answer-mcq"),
    path('classroom/<int:pk>/session/create/',core_views.create_session,name="create-session"),
    path('session/<int:pk>/',core_views.class_session,name="session"),
    path('session/<int:pk>/q/<int:qk>/answer/',core_views.session_answers,name='session_answers'),
    # path('session/<int:pk>/marks',core_views.session_marks,name='marks'),

] + static(settings.STATIC_URL,document_root = settings.STATIC_ROOT)
