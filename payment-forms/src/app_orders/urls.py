from django.urls import path

from app_orders.views import ItemCheckoutView, ItemView, OrderView, OrderCheckoutView

urlpatterns = [
    path("buy/<int:pk>/", ItemCheckoutView.as_view()),
    path("item/<int:pk>/", ItemView.as_view()),
    path("buy-order/<int:pk>/", OrderCheckoutView.as_view()),
    path("order/<int:pk>/", OrderView.as_view()),
]
