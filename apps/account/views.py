from django.forms import BaseModelForm
from django.http import HttpResponse
from django.views.generic import CreateView, FormView, View, DetailView, DeleteView, UpdateView
from .forms import UserRegisterForm, UserLoginForm
from .utils import send_email_actiavation

from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model

from .models import UserAccountActivation, UserProfile
from .forms import *

User = get_user_model()

class UserRegisterView(CreateView):
    form_class = UserRegisterForm
    template_name = "account/user_register.html"
    success_url = reverse_lazy("home_page")

    def form_valid(self, form):
        password1 = form.cleaned_data.pop("password1")
        _ = form.cleaned_data.pop("password2")
        user = form.save()
        user.set_password(password1)
        user.save()
        send_email_actiavation(user, self.request)
        messages.success(self.request, "User added successfully!")
        return redirect("home_page")

    def form_invalid(self, form):
        messages.error(self.request, "User not added!")
        return super().form_invalid(form)


class UserLoginView(FormView):
    form_class = UserLoginForm
    template_name = "account/user_login.html"

    def form_valid(self, form):
        email = form.cleaned_data["email"]
        password = form.cleaned_data["password"]
        user = authenticate(self.request, email=email, password=password)
        if user:
            login(self.request, user)
            messages.success(self.request, "User Logged in!")
            return redirect("home_page")
        messages.error(self.request, "login Failed!")
        return redirect("user_login")

def userLogout(request):
    logout(request)
    messages.success(request, "User Logged Out")
    return redirect("home_page")

class UserAccountActivationView(View):
    def get(self, *args, **kwargs):
        username = kwargs["username"]
        key = kwargs["key"]
        user = User.objects.filter(username=username)
        if user.exists():
            user = user[0]
            us = UserAccountActivation.objects.filter(key=key, email = user.email)
            if us.exists():
                user.is_verified = True
                user.save()
                messages.success(self.request, "Account Activated!")
                return redirect("user_login")
        messages.error(self.request, "Invalid activation link!")
        return redirect("user_login")
    
class ResendEmailActivaiton(View):
    def get(self, *args, **kwargs):
        send_email_actiavation(self.request.user, self.request)
        messages.success(self.request, "Activation link resent!")
        return redirect("home_page")

class UserProfileView(DetailView):
    queryset = User.objects.all()
    template_name = 'account/user_profile.html'
    
class UpdateUserProfileView(UpdateView):
    queryset = User.objects.all()
    template_name = "account/user_profile_update.html"
    form_class = UserProfileForm
    
    def get_success_url(self) -> str:
        return reverse_lazy("user_profile", self.get_object().username)
    
    def get_initial(self) -> dict[str, Any]:
        user = self.get_object()
        initial = super().get_initial()
        try:
            profile = UserProfile.objects.get(user = user)
        except:
            pass
        else:
            initial['phone'] = profile.phone
            initial['address'] = profile.address
            initial['resume'] = profile.resume
            initial['bio'] = profile.bio
            return initial
        
    def form_valid(self, form):
        phone = form.cleaned_data.pop("phone")
        address = form.cleaned_data.pop("address")
        resume = form.cleaned_data.pop("resume")
        bio = form.cleaned_data.pop("bio")
        pp = form.cleaned_data.pop("profile_picture")
        user = form.save()
        u, _ = UserProfile.objects.update_or_create(user=user, defaults={"phone":phone, "address":address, "resume":resume, "bio":bio})
        if pp:
            u.profile_picture = pp
            u.save()
        return redirect("user_profile", user.id)
    