from django.db import models
from ckeditor.fields import RichTextField

# Create your models here.
from django.core.validators import MinValueValidator, MaxValueValidator

class Profile(models.Model):
    name = models.CharField(max_length=100)
    title = models.CharField(max_length=200)
    bio = RichTextField()
    profile_image = models.ImageField(upload_to='profile/')
    resume = models.FileField(upload_to='resume/', blank=True, null=True)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    location = models.CharField(max_length=100, blank=True)
    github = models.URLField(blank=True)
    linkedin = models.URLField(blank=True)
    twitter = models.URLField(blank=True)
    instagram = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profile"

class SkillCategory(models.Model):
    name = models.CharField(max_length=100)
    icon = models.CharField(max_length=50, help_text="FontAwesome icon class")
    order = models.IntegerField(default=0)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['order']
        verbose_name = "Skill Category"
        verbose_name_plural = "Skill Categories"

class Skill(models.Model):
    category = models.ForeignKey(SkillCategory, on_delete=models.CASCADE, related_name='skills')
    name = models.CharField(max_length=100)
    proficiency = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Proficiency percentage (0-100)"
    )
    icon = models.CharField(max_length=50, help_text="FontAwesome icon class", blank=True)
    order = models.IntegerField(default=0)
    
    def __str__(self):
        return f"{self.name} ({self.proficiency}%)"
    
    class Meta:
        ordering = ['category', 'order']

class Service(models.Model):
    title = models.CharField(max_length=200)
    description = RichTextField()
    icon = models.CharField(max_length=50, help_text="FontAwesome icon class")
    price_starting = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    is_featured = models.BooleanField(default=False)
    order = models.IntegerField(default=0)
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['order']

class Project(models.Model):
    title = models.CharField(max_length=200)
    description = RichTextField()
    image = models.ImageField(upload_to='projects/')
    tech_stack = models.CharField(max_length=500, help_text="Comma-separated technologies")
    github_url = models.URLField(blank=True)
    demo_url = models.URLField(blank=True)
    is_featured = models.BooleanField(default=False)
    created_date = models.DateField()
    order = models.IntegerField(default=0)
    
    def __str__(self):
        return self.title
    
    def get_tech_list(self):
        return [tech.strip() for tech in self.tech_stack.split(',')]
    
    class Meta:
        ordering = ['-created_date', 'order']

class Experience(models.Model):
    company = models.CharField(max_length=200)
    position = models.CharField(max_length=200)
    description = RichTextField()
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    is_current = models.BooleanField(default=False)
    company_logo = models.ImageField(upload_to='company_logos/', blank=True)
    
    def __str__(self):
        return f"{self.position} at {self.company}"
    
    class Meta:
        ordering = ['-start_date']

class Testimonial(models.Model):
    client_name = models.CharField(max_length=100)
    client_designation = models.CharField(max_length=200)
    client_company = models.CharField(max_length=200, blank=True)
    client_photo = models.ImageField(upload_to='testimonials/', blank=True)
    review = RichTextField()
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        default=5
    )
    is_featured = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.client_name} - {self.rating}★"
    
    class Meta:
        ordering = ['-created_at']

class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    content = RichTextField()
    excerpt = models.TextField(max_length=300)
    featured_image = models.ImageField(upload_to='blog/')
    tags = models.CharField(max_length=200, help_text="Comma-separated tags")
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    
    def get_tags_list(self):
        return [tag.strip() for tag in self.tags.split(',')]
    
    class Meta:
        ordering = ['-created_at']

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Message from {self.name} - {self.subject}"
    
    class Meta:
        ordering = ['-created_at']



TEMPLATE_TYPE_CHOICES = (
    ('app', 'App'),
    ('website', 'Website'),
)

class ProjectTemplate(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    url = models.URLField(blank=True, null=True) 
    icon = models.ImageField(upload_to='templates/icons/', blank=True, null=True)
    template_type = models.CharField(max_length=10, choices=TEMPLATE_TYPE_CHOICES, default='website')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
