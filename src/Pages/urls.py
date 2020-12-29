from django.urls import path, include
from . import views

urlpatterns = [
	path('Problem_Solving/', views.Problem_Solving_View),
	path('signin/', views.Signin_View),
	path('aboutus/', views.About_Us_View),
    path('postsignin/', views.Post_Signin_View),
    path('aptitude/', views.Aptitude_View),
    path('home/', views.Home_View)
]
