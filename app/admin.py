from django.contrib import admin
from .models import *

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['name', 'title', 'email']
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'title', 'bio', 'profile_image')
        }),
        ('Contact Information', {
            'fields': ('email', 'phone', 'location')
        }),
        ('Social Links', {
            'fields': ('github', 'linkedin', 'twitter', 'instagram')
        }),
        ('Files', {
            'fields': ('resume',)
        }),
    )

@admin.register(SkillCategory)
class SkillCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'icon', 'order']
    list_editable = ['order']

class SkillInline(admin.TabularInline):
    model = Skill
    extra = 1

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'proficiency', 'order']
    list_filter = ['category']
    list_editable = ['proficiency', 'order']

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['title', 'price_starting', 'is_featured', 'order']
    list_filter = ['is_featured']
    list_editable = ['is_featured', 'order']

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_date', 'is_featured', 'order']
    list_filter = ['is_featured', 'created_date']
    list_editable = ['is_featured', 'order']
    prepopulated_fields = {'github_url': ('title',)}

@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ['position', 'company', 'start_date', 'end_date', 'is_current']
    list_filter = ['is_current', 'start_date']

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ['client_name', 'client_company', 'rating', 'is_featured', 'created_at']
    list_filter = ['rating', 'is_featured']
    list_editable = ['is_featured']

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_published', 'created_at']
    list_filter = ['is_published', 'created_at']
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ['title', 'content']

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'is_read', 'created_at']
    list_filter = ['is_read', 'created_at']
    readonly_fields = ['name', 'email', 'subject', 'message', 'created_at']
    list_editable = ['is_read']