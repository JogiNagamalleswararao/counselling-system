from django.urls import path
from . import views

urlpatterns=[
    path('', views.splash, name='splash'),
    path('Home',views.base,name='base'),
    path('login/',views.login,name='login'),
    path('student_r/',views.student_r,name='student_r'),
    path('parent_r/',views.parent_r,name='parent_r'),
    path('teacher_r/',views.teacher_r,name='teacher_r'),
    path('logout/', views.logout, name='logout'),
    path('student/', views.student_details, name='student_details'),
    path('teacher/', views.teacher_dashboard, name='teacher_dashboard'),
    path('parent', views.parent_dashboard, name='parent_dashboard'),
    path('approve_request/', views.approve_request, name='approve_request'),
    path('success_remove/', views.success_remove, name='success_remove'),
    path('success_sent/', views.success_sent, name='success_sent'),
    


]
from django.conf.urls.static import static
from django.conf import  settings
urlpatterns  += static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)