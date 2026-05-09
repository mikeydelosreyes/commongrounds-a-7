from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.db.models import Q, Avg
from django.shortcuts import redirect
from .models import *
from .forms import *


class ProjectListView(ListView):
    model = Project
    template_name = 'diyprojects/project_list.html'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['projects'] = Project.objects.all().distinct()
        if self.request.user.is_authenticated:
            profile = self.request.user.profile
            context['created'] = Project.objects.filter(creator=profile).distinct()
            context['favorites'] = Project.objects.filter(favorites__profile=profile).distinct()
            context['reviewed'] = Project.objects.filter(reviews__reviewer=profile).distinct()

            context['projects'] = Project.objects.exclude(creator=profile
                                                ).exclude(favorites__profile=profile
                                                ).exclude(reviews__reviewer=profile).distinct()
        return context



class ProjectDetailView(DetailView):
    model = Project
    template_name = 'diyprojects/project_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project = self.object
        context['favorites'] = project.favorites.count()
        context['average_score'] = project.ratings.aggregate(Avg('score'))['score__avg']
        context['rating_form'] = ProjectRatingForm()
        context['review_form'] = ProjectReviewForm()
        context['reviews'] = project.reviews.all()
        if self.request.user.is_authenticated:
            context['is_favorited'] = project.favorites.filter(profile=self.request.user.profile).exists()
        return context
    
    def post(self, request, *args, **kwargs):
        project = self.get_object()       
        profile = request.user.profile


        if 'check_favorite' in request.POST:
            favorite = Favorite.objects.filter(project=project, profile=profile).exists()
            
            if favorite:
                Favorite.objects.filter(project=project, profile=profile).delete()
            else:
                Favorite.objects.create(project=project, profile=profile)                
            return redirect(self.get_success_url())


        
        if 'submit_rating' in request.POST:
            rating = ProjectRatingForm(request.POST)
            if rating.is_valid():
                
                if project.ratings.filter(profile=profile).exists():
                    project.ratings.filter(profile=profile).update(score = rating.instance.score)
                else:
                    ProjectRating.objects.create(profile=profile, project=project, score = rating.instance.score)
                return redirect(self.get_success_url())
            
            return redirect(self.get_success_url())



        if 'submit_review' in request.POST:
            review = ProjectReviewForm(request.POST, request.FILES)
            if review.is_valid():
                ProjectReview.objects.create(reviewer=profile, project=project, comment = review.instance.comment,
                                                                                image = review.instance.image)                
            else:
                get_review = project.reviews.filter(reviewer=profile).first()
                get_review.comment = review.instance.comment
                if review.instance.image:
                    get_review.image = review.instance.image
                get_review.save()

            return redirect(self.get_success_url())
    

    def get_success_url(self):
        return reverse_lazy('diyprojects:project_detail', kwargs={'pk': self.kwargs['pk']})
    



class ProjectCreateView(CreateView):
    role_required = "Project Creator"
    model = Project
    template_name = "diyprojects/project_form.html"
    form_class = ProjectForm


    def test_func(self):
        return self.request.user.profile.role == "Project Creator"

    def form_valid(self, form):
        form.instance.creator = self.request.user.profile
        return super().form_valid(form)   

    
    
class ProjectUpdateView(UpdateView):
    role_required = "Project Creator"
    model = Project
    template_name = "diyprojects/project_update.html"
    form_class = ProjectUpdateForm

    def test_func(self):
        return (self.request.user.profile.role == "Project Creator")