from django.urls import path, include
from . import views

urlpatterns = [
	path('Problem_Solving/', views.Problem_Solving_View),
	path('login/', views.Login_View),
	path('aboutus/', views.About_Us_View),
    path('blank/', views.blank)
]
