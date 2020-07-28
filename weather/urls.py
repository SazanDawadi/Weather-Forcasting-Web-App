from django.urls import path

from . import views

urlpatterns = [
        #Leave as empty string for base url
	path('', views.home, name="home"),
        path('search-result', views.home, name="search-result"),

]