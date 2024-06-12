from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from .models import Job

class HomePageView(ListView):
    template_name = "main/home.html"
    queryset = Job.objects.all().order_by("-created_at")
    paginate_by = 6