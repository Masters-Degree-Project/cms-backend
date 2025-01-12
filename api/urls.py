from django.urls import path
from .views import ContentView, ContentDetailView, LanguageView, ContentLanguageDetailView


urlpatterns = [
    path('contents/', ContentView.as_view(), name='contents'),
    path('contents/<int:content_id>', ContentDetailView.as_view(), name='content_detail'),

    path('contents/<int:content_id>/languages/<int:content_language_id>', ContentLanguageDetailView.as_view(), name='languages'),

    path('languages/', LanguageView.as_view(), name='languages'),
]
