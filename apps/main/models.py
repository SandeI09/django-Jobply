from django.db import models
from django.contrib.auth import get_user_model
from apps.commons.models import DateTimeModel

User = get_user_model()

# Create your models here.
class Category(DateTimeModel):
    title = models.CharField(max_length=50)
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name_plural = "Categories"

    
class Job(DateTimeModel):
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=1000)
    location = models.CharField(max_length=50)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="category_jobs")
    apply_before = models.DateTimeField()
    experience_required = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return self.title
    
APPLIED = "Applied"
SCREENING = "Screening"
DECLINED = "DECLINED"
CALL_FOR_INTERVIEW = "Call for Interview"
REJECTED = "Rejected"
SELECTED = "Selected"
APPLICATION_STATUS = (
    (APPLIED,APPLIED),
    (SCREENING, SCREENING),
    (DECLINED,DECLINED),
    (CALL_FOR_INTERVIEW, CALL_FOR_INTERVIEW),
    (REJECTED, REJECTED),
    (SELECTED, SELECTED)
)

class JobApplicaiton(DateTimeModel):
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name = "job_application")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_applications")
    status = models.CharField(choices=APPLICATION_STATUS, max_length=20)
    interview_date = models.DateField(null=True, blank=True)
    
    def __str__(self):
        return f"Application by {self.user.email} for {self.job.title}"
    