from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('skills/', views.skills, name='skills'),
    path('services/', views.services, name='services'),
    path('projects/', views.projects, name='projects'),
    path('project/<int:pk>/', views.project_detail, name='project_detail'),
    path('experience/', views.experience, name='experience'),
    path('blog/', views.blog, name='blog'),
    path('blog/<slug:slug>/', views.blog_detail, name='blog_detail'),
    path('contact/', views.contact, name='contact'),
    path('download-resume/', views.download_resume, name='download_resume'),
]