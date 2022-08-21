from email import message
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CancelSubscriptionForm
from django.views.generic import FormView, View
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth import get_user_model
from courses.models import Course

import stripe

User = get_user_model()

class CancelSubscriptionView(LoginRequiredMixin, FormView):
    form_class = CancelSubscriptionForm
    
    def get_success_url(self):
        return reverse('user:subscription', kwargs={'username': self.request.user.username})

    def form_valid(self, form):
        stripe.Subscription.delete(self.request.user.subscription.stripe_subscription_id)
        messages.success(self.request, "Has cancelado la subscripción!")
        return super().form_valid(form)


class UserSubscriptionView(View):
    def get(self, request, username, *args, **kwargs):
        user =  get_object_or_404(User, username=username)
        courses = Course.objects.filter(is_active = True)
        subscription = request.user.subscription
        pricing_tier = subscription.price
        print(pricing_tier)
        courses = Course.objects.filter(is_active = True, pricing_tiers = pricing_tier )
        context = {
            'user':user,
            'courses':courses
        }
        return render(request,"users/user_subscription.html",context)