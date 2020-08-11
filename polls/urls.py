from django.urls import path, include
from . import views			#call the views module form current directory


urlpatterns = [
    path("", views.index, name='polls-home'),
    path("about/", views.about, name='polls-about'),		#views.home means that call the home fucntion from the views module
    path("signin/", views.signin, name='polls-signin'),
]