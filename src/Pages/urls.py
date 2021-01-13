from django.urls import path, include
from . import views

urlpatterns = [
	path('Problem_Solving/', views.Problem_Solving_View),
	path('signin/', views.Signin_View),
	path('aboutus/', views.About_Us_View),
    path('postsignin/', views.Post_Signin_View),
    path('aptitude/', views.Aptitude_View),
    path('home/', views.Home_View),
    path('blog/', views.Blog_Page_View),
    path('resources/', views.Resources_View),
    path('blog-single/<blog_id>/', views.Blog_Single_View, name="blog_single"),
    path('edit-post/<blog_id>/', views.Edit_Post_View, name="blog_edit"),
    path('delete-post/<blog_id>/', views.Delete_Post, name="blog_delete"),
    path('manage-posts/', views.Manage_Posts_View),
    path('create-post/', views.Create_Post_View),
    path('logout/', views.logout, name='log')
]
