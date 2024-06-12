from django.urls import path
from . import views

urlpatterns = [
    path("", views.HomePageView.as_view(), name="home_page"),
    path("apply-job/<int:job_id>", views.ApplyJobView.as_view(), name="apply_job"),
    path("job/detail/<int:pk>", views.JobDetailView.as_view(), name="job_detail"),
    path("my-jobs/", views.MyJobs.as_view(), name="my_jobs"),
]
