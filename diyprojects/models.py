from django.db import models
from django.urls import reverse
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
                                 related_name='categories', null=True)
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