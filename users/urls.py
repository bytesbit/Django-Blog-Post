from django.urls import path, include
from . import views


urlpatterns = [
	path("<int:pk>/", views.edit, name='edit-post'),
]