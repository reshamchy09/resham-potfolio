
# views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from .models import *
from .forms import ContactForm
import os
from .models import ProjectTemplate

def get_profile():
    """Get the first profile or return None"""
    return Profile.objects.first()

def home(request):
    profile = get_profile()
    featured_projects = Project.objects.filter(is_featured=True)[:6]
    featured_services = Service.objects.filter(is_featured=True)[:6]
    featured_testimonials = Testimonial.objects.filter(is_featured=True)[:6]
    recent_blogs = BlogPost.objects.filter(is_published=True)[:3]
    
    context = {
        'profile': profile,
        'featured_projects': featured_projects,
        'featured_services': featured_services,
        'featured_testimonials': featured_testimonials,
        'recent_blogs': recent_blogs,
    }
    return render(request, 'home.html', context)

def about(request):
    profile = get_profile()
    experiences = Experience.objects.all()
    
    context = {
        'profile': profile,
        'experiences': experiences,
    }
    return render(request, 'about.html', context)

def skills(request):
    profile = get_profile()
    skill_categories = SkillCategory.objects.prefetch_related('skills').all()
    
    context = {
        'profile': profile,
        'skill_categories': skill_categories,
    }
    return render(request, 'skills.html', context)

def services(request):
    profile = get_profile()
    all_services = Service.objects.all()
    featured_services = all_services.filter(is_featured=True)
    regular_services = all_services.filter(is_featured=False)
    
    context = {
        'profile': profile,
        'featured_services': featured_services,
        'regular_services': regular_services,
        'all_services': all_services,
    }
    return render(request, 'services.html', context)

def projects(request):
    profile = get_profile()
    search_query = request.GET.get('search', '')
    tech_filter = request.GET.get('tech', '')
    
    projects_list = Project.objects.all()
    
    if search_query:
        projects_list = projects_list.filter(
            Q(title__icontains=search_query) | 
            Q(description__icontains=search_query) |
            Q(tech_stack__icontains=search_query)
        )
    
    if tech_filter:
        projects_list = projects_list.filter(tech_stack__icontains=tech_filter)
    
    # Get all unique technologies for filter
    all_projects = Project.objects.all()
    all_techs = set()
    for project in all_projects:
        all_techs.update(project.get_tech_list())
    all_techs = sorted(list(all_techs))
    
    paginator = Paginator(projects_list, 9)
    page_number = request.GET.get('page')
    projects = paginator.get_page(page_number)
    
    context = {
        'profile': profile,
        'projects': projects,
        'search_query': search_query,
        'tech_filter': tech_filter,
        'all_techs': all_techs,
    }
    return render(request, 'projects.html', context)

def project_detail(request, pk):
    profile = get_profile()
    project = get_object_or_404(Project, pk=pk)
    related_projects = Project.objects.exclude(pk=pk).filter(
        tech_stack__icontains=project.get_tech_list()[0] if project.get_tech_list() else ''
    )[:3]
    
    context = {
        'profile': profile,
        'project': project,
        'related_projects': related_projects,
    }
    return render(request, 'project_detail.html', context)

def experience(request):
    profile = get_profile()
    experiences = Experience.objects.all()
    
    context = {
        'profile': profile,
        'experiences': experiences,
    }
    return render(request, 'experience.html', context)

def blog(request):
    profile = get_profile()
    search_query = request.GET.get('search', '')
    tag_filter = request.GET.get('tag', '')
    
    blogs_list = BlogPost.objects.filter(is_published=True)
    
    if search_query:
        blogs_list = blogs_list.filter(
            Q(title__icontains=search_query) | 
            Q(content__icontains=search_query) |
            Q(excerpt__icontains=search_query)
        )
    
    if tag_filter:
        blogs_list = blogs_list.filter(tags__icontains=tag_filter)
    
    # Get all unique tags for filter
    all_blogs = BlogPost.objects.filter(is_published=True)
    all_tags = set()
    for blog in all_blogs:
        all_tags.update(blog.get_tags_list())
    all_tags = sorted(list(all_tags))
    
    paginator = Paginator(blogs_list, 6)
    page_number = request.GET.get('page')
    blogs = paginator.get_page(page_number)
    
    context = {
        'profile': profile,
        'blogs': blogs,
        'search_query': search_query,
        'tag_filter': tag_filter,
        'all_tags': all_tags,
    }
    return render(request, 'blog.html', context)

def blog_detail(request, slug):
    profile = get_profile()
    post = get_object_or_404(BlogPost, slug=slug, is_published=True)
    related_posts = BlogPost.objects.filter(is_published=True).exclude(slug=slug)[:3]
    
    context = {
        'profile': profile,
        'post': post,
        'related_posts': related_posts,
    }
    return render(request, 'blog_detail.html', context)

def contact(request):
    profile = get_profile()
    
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thank you for your message! I will get back to you soon.')
            return redirect('contact')
    else:
        form = ContactForm()
    
    context = {
        'profile': profile,
        'form': form,
    }
    return render(request, 'contact.html', context)

def download_resume(request):
    profile = get_profile()
    if profile and profile.resume:
        file_path = profile.resume.path
        if os.path.exists(file_path):
            with open(file_path, 'rb') as fh:
                response = HttpResponse(fh.read(), content_type="application/pdf")
                response['Content-Disposition'] = f'attachment; filename="{profile.name}_Resume.pdf"'
                return response
    raise Http404("Resume not found")

def template_list(request):
    filter_type = request.GET.get('type')  # 'app', 'website', or None
    if filter_type in ['app', 'website']:
        templates = ProjectTemplate.objects.filter(template_type=filter_type)
    else:
        templates = ProjectTemplate.objects.all()
    return render(request, "template_list.html", {"templates": templates, "filter_type": filter_type})


def template_preview(request, pk):
    template = get_object_or_404(ProjectTemplate, pk=pk)
    return render(request, "template_preview.html", {
        "template": template
    })

from django.shortcuts import render


def services_page(request):
    profile = Profile.objects.first()  # assuming only one profile
    context = {
        'profile': profile,
    }
    return render(request, 'mobile_app_calculator.html', context)

