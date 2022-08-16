from django.urls import path
from .views import CancelSubscriptionView,UserSubscriptionView


app_name = 'accounts'

urlpatterns = [
    path('<str:username>/subscription/',CancelSubscriptionView.as_view(), name='cancel-subscription'),
    path('<str:username>/subscription/cancel/',UserSubscriptionView.as_view(), name='subscription'),
]