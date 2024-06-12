from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView, DetailView, View
from .models import Job, JobApplicaiton, APPLIED
from django.contrib import messages


class HomePageView(ListView):
    template_name = "main/home.html"
    queryset = Job.objects.all().order_by("-created_at")
    paginate_by = 6
    
class JobDetailView(DetailView):
    template_name = "main/job_detail.html"
    queryset = Job.objects.all()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        job = self.get_object()
        if self.request.user.is_authenticated:
            application = JobApplicaiton.objects.filter(user=self.request.user, job=job)
            context["has_applied"] = application
            return context
    
class ApplyJobView(View):
    def get(self, *args, **kwargs):
        if not self.request.user.is_verified:
            messages.error(self.request, "Please verify your email first!")
            return redirect("home_page")
        if not self.request.user.userprofile.resume:
            messages.error(self.request, "Please upload your resume!")
            return redirect("home_page")
        job_id = kwargs["job_id"]
        job = Job.objects.get(id=job_id)
        JobApplicaiton.objects.create(job=job, user=self.request.user, status=APPLIED)
        messages.success(self.request, "Successfully applied to the Job!")
        return redirect("home_page")
    
class MyJobs(ListView):
    template_name = "main/my_jobs.html"
    
    def get_queryset(self):
        return JobApplicaiton.objects.filter(user=self.request.user)
    