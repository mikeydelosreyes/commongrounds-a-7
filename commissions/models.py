from django.db import models
from datetime import datetime
from django.urls import *
from django.db.models import Case, When, Value, IntegerField
from accounts.models import Profile


class CommissionType(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('commissiontype_list', args=[str(self.name)])

    class Meta:
        ordering = ['name']
        verbose_name = 'commission type'
        verbose_name_plural = 'commission types'


class Commission(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    type = models.ForeignKey(CommissionType, on_delete=models.SET_NULL, null=True)
    maker = models.ForeignKey(Profile, on_delete=models.CASCADE)
    status = models.CharField(choices=(('Open', 'Open'), ('Full', 'Full')), default='Open')
    people_required = models.PositiveIntegerField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('commissions:commission_detail', args=[str(self.pk)])

    class Meta:
        ordering = ['created_on']
        verbose_name = 'commission'
        verbose_name_plural = 'commissions'

class Job(models.Model):
    commission = models.ForeignKey(Commission, on_delete=models.CASCADE, related_name="jobs")
    role = models.CharField(max_length=255)
    manpower_required = models.PositiveIntegerField()
    status = models.CharField(choices=(('Open', 'Open'), ('Full', 'Full')), default='Open')

    def __str__(self):
        return self.role
    
    class Meta:
        ordering = [Case(
            When(status='Open', then=Value(1)),
            When(status='Full', then=Value(2)),
            output_field=IntegerField(),
        ), 
        '-manpower_required', 'role']

class JobApplication(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name="applications")
    applicant = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="role")
    status = models.CharField(choices=(('Pending', 'Pending'), ('Accepted', 'Accepted'), ('Rejected', 'Rejected')), default='Pending')
    applied_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.job
    
    class Meta:
        ordering = [Case(
            When(status='Pending', then=Value(1)),
            When(status='Accepted', then=Value(2)),
            When(status='Rejected', then=Value(3)),
            output_field=IntegerField(),
        ), '-applied_on']
