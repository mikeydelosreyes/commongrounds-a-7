from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Case, When, Value, IntegerField

from .models import *
from .forms import *

from accounts.mixins import RoleRequiredMixin
from accounts.models import Profile


class CommissionListView(ListView):
    model = Commission
    template_name = "commissions/commissions_list.html"
    context_object_name = "all_commissions"

    def get_queryset(self):
        return Commission.objects.annotate(
            status_order=Case(
                When(status='Open', then=Value(0)),
                When(status='Full', then=Value(1)),
                When(status='Completed', then=Value(2)),
                When(status='Discontinued', then=Value(3)),
                default=Value(4),
                output_field=IntegerField()
            )
        ).order_by('status_order', '-created_on')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        qs = self.get_queryset()

        if self.request.user.is_authenticated:
            current_profile = Profile.objects.get(user=self.request.user)
            created_commissions = qs.filter(maker=current_profile)
            applied_commissions = qs.filter(
                jobs__applications__applicant=current_profile)
            other_commissions = qs.exclude(
                    id__in=created_commissions).exclude(
                    id__in=applied_commissions)

            ctx["created_commissions"] = created_commissions
            ctx["applied_commissions"] = applied_commissions
            ctx["other_commissions"] = other_commissions

        return ctx


class CommissionDetailView(DetailView):
    model = Commission
    template_name = "commissions/commissions_detail.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        commission = self.object
        jobs = commission.jobs.all()

        all_jobs_full = True

        for job in jobs:
            job.accepted_count = job.applications.filter(
                status='2_ACPT').count()
            if job.accepted_count >= job.manpower_required:
                if job.status != '2_FULL':
                    job.status = '2_FULL'
                    job.save()
                else:
                    all_jobs_full = False
                    if job.status == "2_FULL":
                        job.status == "1_OPEN"
                        job.save()

        if not jobs.exclude(status='2_FULL').exists() and all_jobs_full:
            if commission.status != 'Full':
                commission.status = 'Full'
                commission.save()
            elif not all_jobs_full:
                if commission.status == 'Full':
                    commission.status = 'Open'
                    commission.save()

        total_manpower = sum(job.manpower_required for job in jobs)
        accepted = sum(job.applications.filter(status='2_ACPT').count()
                       for job in jobs)

        open_manpower = total_manpower - accepted

        if open_manpower <= 0:
            commission.status = 'Full'
        else:
            commission.status = 'Open'
        commission.save()

        ctx['jobs'] = jobs
        ctx['total_manpower'] = total_manpower
        ctx['open_manpower'] = max(0, open_manpower)

        if self.request.user.is_authenticated:
            ctx['current_profile'] = self.request.user.profile

        ctx['jobs'] = jobs

        return ctx

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        job_id = request.POST.get('job_id')

        if not request.user.is_authenticated:
            return redirect('login')

        job = self.object.jobs.get(id=job_id)
        profile = Profile.objects.get(user=self.request.user)

        if JobApplication.objects.filter(job=job, applicant=profile).exists():
            return redirect('commissions:commission_detail', pk=self.object.pk)

        JobApplication.objects.create(
            job=job,
            applicant=profile
        )

        return redirect('commissions:commission_detail', pk=self.object.pk)


class CommissionCreateView(LoginRequiredMixin, RoleRequiredMixin, CreateView):
    role_name = "Commission Maker"
    model = Commission
    form_class = CommissionForm
    template_name = "commissions/commissions_create.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = JobFormSet(self.request.POST,
                                            instance=self.object)
        else:
            context['formset'] = JobFormSet(instance=self.object)
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
            return render(self.request, self.template_name,
                          self.get_context_data(form=form))


class CommissionUpdateView(LoginRequiredMixin, RoleRequiredMixin, UpdateView):
    role_name = "Commission Maker"
    model = Commission
    form_class = CommissionForm
    template_name = "commissions/commissions_update.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = JobFormSet(self.request.POST,
                                            instance=self.object)
        else:
            context['formset'] = JobFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']

        form.instance.maker = self.request.user.profile

        if formset.is_valid():
            if not self.object.jobs.exclude(status='2_FULL').exists():
                self.object.status = "Full"
            else:
                self.object.status = "Open"
            self.object = form.save()
            formset.instance = self.object
            formset.save()

            return redirect('commissions:commission_detail', pk=self.object.pk)
        else:
            return render(self.request, self.template_name,
                          self.get_context_data(form=form))
