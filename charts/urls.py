from django.urls import path, include
from .views import show_stats, server_details, show_server_detail

urlpatterns = [
    path('server/<int:pk>', show_server_detail, name='detail'),
    path('server/', show_stats, name="show_stats"),
    path('server-details', server_details, name="server_details")
]
