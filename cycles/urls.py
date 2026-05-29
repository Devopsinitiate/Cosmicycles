from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('profile/update/', views.profile_update_api, name='profile_update_api'),
    path('businesses/', views.business_list, name='business_list'),
    path('businesses/add/', views.business_create, name='business_create'),
    path('businesses/<int:pk>/edit/', views.business_edit, name='business_edit'),
    path('businesses/<int:pk>/delete/', views.business_delete, name='business_delete'),
    path('businesses/<int:pk>/delete/json/', views.business_delete_api, name='business_delete_api'),
    path('api/cycles/<str:cycle_type>/', views.user_cycle_api, name='user_cycle_api'),
    path('education/', views.education, name='education'),
    path('education/quiz/<int:period_id>/', views.education_quiz, name='education_quiz'),
    path('education/<str:cycle_type>/', views.education_detail, name='education_detail'),
    path('education/<str:cycle_type>/<int:period_id>/', views.education_period_detail, name='education_period_detail'),
    path('visualizations/', views.visualizations, name='visualizations'),
    path('report/pdf/', views.generate_report_pdf, name='generate_report_pdf'), # New PDF report URL
    path('journal/', views.journal_list, name='journal_list'),
    path('journal/add/', views.journal_create, name='journal_create'),
    path('journal/<int:pk>/delete/', views.journal_delete, name='journal_delete'),
    path('alerts/', views.alerts, name='alerts'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('verify-email/<str:token>/', views.verify_email, name='verify_email'),
    path('verify-email/resend/', views.resend_verification, name='resend_verification'),
    path('htmx/cycles/<str:cycle_type>/', views.htmx_cycle_tab, name='htmx_cycle_tab'),
]
