from django.contrib import admin
from django.urls import path
from vendas.views import dashboard_view, forecast_sales

urlpatterns = [
    path('admin/', admin.site.urls),  # Admin URL
    path('', dashboard_view, name='dashboard'),  # Root URL points to dashboard_view
    path('dashboard/', dashboard_view, name='dashboard'),  # Optional: keep dashboard URL
    path('forecast/', forecast_sales, name='forecast_sales'),  # Forecast URL
]