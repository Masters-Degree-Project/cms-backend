from django.urls import path
from .views import ContentView, ContentDetailView

urlpatterns = [
    path('contents/', ContentView.as_view(), name='contents'),
    path('contents/<int:content_id>', ContentDetailView.as_view(), name='content_detail'),
]
