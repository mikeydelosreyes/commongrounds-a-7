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
    STATUS_CHOICES = {
        "Open" : "Open",
        "Full" : "Full",
    }
    status = models.CharField(choices=STATUS_CHOICES, default="Open")
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
    STATUS_CHOICES = {
        "1_OPEN" : "Open",
        "2_FULL" : "Full",
    }
    status = models.CharField(choices=STATUS_CHOICES, default="1_OPEN")

    def __str__(self):
        return self.role
    
    class Meta:
        ordering = ['status', '-manpower_required', 'role']

class JobApplication(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name="applications")
    applicant = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="job_applications")
    STATUS_CHOICES = {
        "1_PEND" : "Pending",
        "2_ACPT" : "Accepted",
        "3_RJCT" : "Rejected",
    }
    status = models.CharField(choices=STATUS_CHOICES, default="1_PEND")
    applied_on = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['status', '-applied_on']

    def __str__(self):
        return f"{self.job} - {self.applicant}"
