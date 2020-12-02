from django.shortcuts import render

# Create your views here.
def Problem_Solving_View(request, *args, **kwargs):
	return render(request, 'Problem_Solving.html',{})
