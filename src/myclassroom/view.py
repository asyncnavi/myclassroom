from django.shortcuts import render, redirect

def home_view(request):

    if request.user.is_authenticated:
        return redirect("/class")

    return render(request,'home.html')
