from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Case, When, Value, IntegerField, Count, Q

from .models import *
from .forms import *

class CommissionListView(ListView):
    model = Commission
    template_name = "commissions/commissions_list.html"
    context_object_name = "all_commissions"

    def get_queryset(self):
        return Commission.objects.annotate(
            status_order=Case(
             When(status='Open', then=Value(1)), 
             When(status='Full', then=Value(2)), 
             When(status='Completed', then=Value(3)), 
             When(status='Discontinued', then=Value(4)), 
            default=Value(5),
            output_field=IntegerField(), 
        )).order_by('status_order', '-created_on')   
                
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        qs = self.get_queryset()

        if self.request.user.is_authenticated:
            profile = self.request.user.profile
            created_qs = qs.filter(maker=profile)
            applied_qs = qs.filter(jobs__applications__applicant=profile).distinct()
            all_other_qs = qs.exclude(id__in=created_qs).exclude(id__in=applied_qs)

            context['created_commissions'] = created_qs 
            context['applied_commissions'] = applied_qs 
            context['all_commissions'] = all_other_qs          

        return context

class CommissionDetailView(DetailView):
    model = Commission
    template_name = "commissions/commissions_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        commission = self.object

        jobs = commission.jobs.annotate(
            accepted_count=Count('applications', 
                                 filter=Q(applications__status='Accepted'))
        )
        total_manpower = sum(job.manpower_required for job in jobs)
        open_manpower = sum((job.manpower_required - job.accepted_count) for job in jobs)
        
        context['jobs'] = jobs
        context['total_manpower'] = total_manpower
        context['open_manpower'] = max(0, open_manpower) 

        if self.request.user.is_authenticated:
            context['application_form'] = JobApplicationForm()
            
        return context  
    
    def post(self, request):
        self.object = self.get_object()
        
        if not request.user.is_authenticated:
            return redirect('login')

        job_pk = request.POST.get('job_pk')
        if job_pk:
            job = Job.objects.get(pk=job_pk)
            has_applied = JobApplication.objects.filter(job=job, applicant=request.user.profile).exists()
            
            accepted_count = job.applications.filter(status='Accepted').count()
            if not has_applied and accepted_count < job.manpower_required:
                JobApplication.objects.create(
                    job=job,
                    applicant=request.user.profile,
                    status='Pending'
                )
                
        # Redirect back to the same page
        return redirect('commissions:commission_detail', pk=self.object.pk)
    
class CommissionCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Commission
    form_class = CommissionForm
    template_name = "commissions/commissions_create.html"  

    def test_func(self):
        return self.request.user.profile.role == 'Commission Maker'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = JobFormSet(self.request.POST)
        else:
            context['formset'] = JobFormSet()
        return context
    
    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']

        form.instance.maker = self.request.user.profile

        if formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()

            return redirect('commissions:commission_detail', pk=self.object.pk)
        
        else:
            return self.render_to_response(self.get_context_data(form=form))

class CommissionUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Commission
    template_name = "commissions/commissions_update.html"    

    def test_func(self):
        return self.request.user.profile.role == 'Commission Maker'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = JobFormSet(self.request.POST, instance=self.object)
        else:
            context['formset'] = JobFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']

        form.instance.maker = self.object.maker

        if formset.is_valid():
            self.object = form.save()
            formset.save()

            jobs = self.object.jobs.all()
            if jobs.exists() and all(job.status == 'Full' for job in jobs):
                self.object.status = 'Full'
                self.object.save()

            return redirect('commissions:commission_detail', pk=self.object.pk)
        else:
            return self.render_to_response(self.get_context_data(form=form))    