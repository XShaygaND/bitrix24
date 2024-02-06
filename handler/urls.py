from django.urls import path

from .views import HandlerView


urlpatterns = [
    path('handler/', HandlerView.as_view(), name='handler'),
]
