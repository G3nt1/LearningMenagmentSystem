from django.urls import path
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from lms.views import home, userview, exercises

urlpatterns = [
    path('', home.home, name='home'),
    path('register/', userview.register_user, name='register'),
    path('login/', userview.login_user, name='login'),
    path('logout/', userview.userLogout, name='logout'),

    # resete password
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

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
