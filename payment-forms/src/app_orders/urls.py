from django.urls import path

from app_orders.views import ItemCheckoutView, ItemView

urlpatterns = [
    path("buy/<int:pk>/", ItemCheckoutView.as_view()),
    path("item/<int:pk>/", ItemView.as_view()),
]
