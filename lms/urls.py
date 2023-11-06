from django.urls import path
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from lms.views import home, userview


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
    path('details_lesson/<int:lesson_id>', home.lesson_details, name='details_lesson')

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)