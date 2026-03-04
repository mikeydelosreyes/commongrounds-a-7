from django.db import models
from django.urls import reverse
from datetime import datetime

# Create your models here.

class ProjectCategory(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('diyprojects_detail', args=[str(self.pk)])

    class Meta:
        ordering = ['title']
        verbose_name = 'project list'
        verbose_name_plural = 'projects lists'

class Project(models.Model):
    title = models.CharField(max_length=255)
    category = models.ForeignKey(ProjectCategory, on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    materials = models.TextField(blank=True)
    steps = models.TextField(blank=True)
    created_on = models.DateTimeField(auto_now_add=True, null=True, blank=True)  
    updated_on = models.DateTimeField(auto_now=True, null=True, blank=True)  

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('diyprojects_detail', args=[str(self.pk)])

    class Meta:
        ordering = ['created_on']
        verbose_name = 'project'
        verbose_name_plural = 'projects'