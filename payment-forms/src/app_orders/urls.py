from django.urls import path

from app_orders.views import ItemCheckoutView, ItemView, OrderView, OrderCheckoutView, StripeWebhook, CancelView, \
    SuccessView

urlpatterns = [
    path("buy-item/<int:pk>/", ItemCheckoutView.as_view()),
    path("item/<int:pk>/", ItemView.as_view()),
    path("buy-order/<int:pk>/", OrderCheckoutView.as_view()),
    path("order/<int:pk>/", OrderView.as_view()),
    path("webhooks/stripe/", StripeWebhook.as_view()),
    path('cancel/', CancelView.as_view(), name='cancel'),
    path('success/', SuccessView.as_view(), name='success'),
]
