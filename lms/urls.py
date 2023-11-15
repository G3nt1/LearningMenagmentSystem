from django.urls import path
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from lms.views import home, userview, exercises, answers

urlpatterns = [
    path('', home.home, name='home'),
    path('register/', userview.register_user, name='register'),
    path('login/', userview.login_user, name='login'),
    path('logout/', userview.userLogout, name='logout'),

    path('profile/<int:user_id>', userview.profile, name='profile'),
    path('edit_profile/<int:user_id>', userview.edit_profile, name='edit_profile'),

    # reset password
    path('reset_password/', auth_views.PasswordResetView.as_view
    (template_name='users/reset_password.html'), name='password_reset'),

    path('reset_password/sent/', auth_views.PasswordResetDoneView.as_view
    (template_name='users/password_reset_done.html'), name='password_reset_done'),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view
    (template_name='users/password_reset_confirm.html'), name='password_reset_confirm'),

    path('reset-password/complete/', auth_views.PasswordResetCompleteView.as_view
    (template_name='users/password_reset_complete.html'), name='password_reset_complete'),

    path('new_lesson/', home.create_lesson, name='new_lesson'),
    path('details_lesson/<int:lesson_id>', home.lesson_details, name='details_lesson'),
    path('edit_lesson/<int:lesson_id>', home.edit_lesson, name='edit_lesson'),
    path('delete_lesson/<int:lesson_id>', home.delete_lesson, name='delete_lesson'),
    path('home/<str:category_name>/', home.home, name='home'),

    path('create_classroom', home.create_classroom, name='create_classroom'),
    path('create_test', exercises.create_test, name='create_test'),
    path('tests', exercises.tests, name='tests'),
    path('tests/<int:test_id>', exercises.edit_test, name='edit_test'),
    path('delete_test/<int:test_id>', exercises.delete_test, name='delete_test'),

    # Questions
    path('questions/<int:test_id>/', exercises.questions, name='questions'),
    path('create_question/<int:test_id>/', exercises.create_question, name='create_question'),
    path('create_options/<int:question_id>/', exercises.create_options, name='create_options'),
    path('edit_question/<int:question_id>/', exercises.edit_question, name='edit_question'),
    path('edit_options/<int:question_id>/', exercises.edit_options, name='edit_options'),
    path('delete_question/<int:question_id>/', exercises.delete_question, name='delete_question'),

    # Answers
    path('answers/<int:test_id>', answers.show_answers, name='answers'),
    path('submit_answer/<int:test_id>', answers.submit_answers, name='submit_answer'),



    path('search', exercises.search, name='search'),


]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
