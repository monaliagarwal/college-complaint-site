from django.urls import path
from django.shortcuts import redirect
from . import views

urlpatterns = [
    path('', lambda request: redirect('login'), name='home'),
    path('register/',                           views.register_view,      name='register'),
    path('login/',                              views.login_view,         name='login'),
    path('logout/',                             views.logout_view,        name='logout'),
    path('submit/',                             views.submit_complaint,   name='submit_complaint'),
    path('dashboard/',                          views.student_dashboard,  name='student_dashboard'),
    path('admin-dashboard/',                    views.admin_dashboard,    name='admin_dashboard'),
    path('update-status/<int:complaint_id>/',   views.update_status,      name='update_status'),
    path('complaint/<int:complaint_id>/',       views.complaint_detail,   name='complaint_detail'),
]