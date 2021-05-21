from django.shortcuts import render, redirect
from .models import Classroom
from .forms import CreateClassForm
from django.contrib import messages
# Create your views here.


def class_index_view(request):

    if not request.user.is_authenticated:
        return redirect
    else:
        joined_classes = Classroom.objects.filter(students = request.user)    

    context = {
        'joined_classes': joined_classes 
    }    
    return render(request,'classes/index.html', context)

def created_classes_view(request):

    if not request.user.is_authenticated:
        return redirect
    else:
        created_classes = Classroom.objects.filter(teacher = request.user)

    context = {
        "created_classes" : created_classes
    }

    return render(request, 'classes/created.html', context)         



def create_class_view(request):

    if not request.user.is_authenticated:
        return redirect
    else:
        
        if request.method == "POST":
            form = CreateClassForm(request.POST)

            if form.is_valid():
                intance = form.save(commit=False)
                intance.teacher = request.user
                intance.save()


                messages.success(request, f"class created with code successfully")
                return redirect("/class/created")

    context = {
        'form' : CreateClassForm()
    }            
    return render(request,"classes/create.html",context)        

def delete_class_view(request):

    if request.method == "POST":
        class_id = request.POST.get("class_id")
        classroom = Classroom.objects.get(pk=class_id)

        if not request.user == classroom.teacher:
            messages.error(request, "your are not creater of this class so you cannot delete it.")
            return redirect("/class/created")
        else:
            classroom.delete()
            messages.success(request, "class was deleted by you.")
            return redirect("/class/created")
    return redirect("/class/created")        


def class_detail_view(request):
    pass

def posts_view(request):
    pass

def post_detail_view(request):
    pass

def assignements_view(request):
    pass

def assignments_detail_view():
    pass    
    