from django.db import models
from django.urls import reverse
from accounts.models import *
from datetime import datetime


class ProjectCategory(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('diyprojects:project_list')

    class Meta:
        ordering = ['name']
        verbose_name = 'project list'
        verbose_name_plural = 'project lists'

class Project(models.Model):
    title = models.CharField(max_length=255)
    category = models.ForeignKey(ProjectCategory, on_delete=models.SET_NULL,
                                 related_name='projects', null=True)
    creator = models.ForeignKey(Profile, on_delete=models.SET_NULL,
                                related_name='projects', null=True )
    description = models.TextField()
    materials = models.TextField()
    steps = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True, null=True)  
    updated_on = models.DateTimeField(auto_now=True, null=True)  

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('diyprojects:project_detail', args=[str(self.pk)])

    class Meta:
        ordering = ['-created_on']
        verbose_name = 'project'
        verbose_name_plural = 'projects'

class Favorite(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE,
                                related_name='favorites')
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE,
                                related_name='favorites') 
    date_favorited = models.DateTimeField(auto_now_add=True, null=True)
    project_status = models.CharField(max_length=100, choices=[
        ('backlog','Backlog'), 
        ('to-do','To-Do'), 
        ('done', 'Done')
        ])

class ProjectReview(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE,
                                related_name='reviews')
    reviewer = models.ForeignKey(Profile, on_delete=models.CASCADE,
                                 related_name='reviews') 
    comment = models.TextField()
    image = models.ImageField(upload_to='images/', null=True)

class ProjectRating(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE,
                                related_name='ratings')
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE,
                                related_name='ratings') 
    score = models.IntegerField(max=10, min=1)
