from django.shortcuts import render, redirect, get_object_or_404
from .models import Classroom
from .forms import CreateClassForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist


# --------Joined classes-------
def class_index_view(request):
    if not request.user.is_authenticated:
        return redirect("/")

    joined_classes = Classroom.objects.filter(students=request.user)

    context = {
        'joined_classes': joined_classes
    }

    return render(request, 'classes/index.html', context)


# --------Created classes-------
def created_classes_view(request):
    if not request.user.is_authenticated:
        return redirect("/")
    else:
        created_classes = Classroom.objects.filter(teacher=request.user)

    context = {
        "created_classes": created_classes
    }

    return render(request, 'classes/created.html', context)


# --------Creating new class-------
def create_class_view(request):
    if not request.user.is_authenticated:
        return redirect("/")
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
        'form': CreateClassForm()
    }
    return render(request, "classes/create.html", context)


# --------Join a class-------
def join_class_view(request):
    if request.method == "POST":
        class_code = request.POST.get('class_code')
        code = class_code.strip()

        try:
            classroom = Classroom.objects.get(code=code)
        except ObjectDoesNotExist:
            messages.error(request, "Invalid class code")
            return redirect("/class/join")

        if request.user == classroom.teacher:
            messages.error(request, "Your are owner of this class so you cannot join.")
            return redirect("/class")
        else:
            classroom.students.add(request.user)
            messages.success(request, f"Your were added to {classroom.name}.")
            return redirect("/class")
    return render(request, "classes/join.html", )


# --------Delete class(By teacher)-------
def delete_class_view(request):
    if request.method == "POST":
        class_id = request.POST.get("class_id")
        classroom = Classroom.objects.get(pk=class_id)

        if not request.user == classroom.teacher:
            messages.error(request, "Your are not creater of this class so you cannot delete it.")
            return redirect("/class/created")
        else:
            classroom.delete()
            messages.success(request, "class was deleted by you.")
            return redirect("/class/created")
    return redirect("/class/created")


# --------Exit from class(By teacher)-------
def exit_class_view(request):
    pass


# --------Class detailed view-------
def class_detail_view(request, code):
    context = {}
    if not request.user.is_authenticated:
        return redirect("/")
    else:
        class_code = code.strip()
        classroom = Classroom.objects.get(code=class_code)

        if request.user in classroom.students.all():
            posts = classroom.post_set.all()
            print(posts)
            context = {
                'posts': posts,
                'classroom': classroom
            }
        else:
            if request.user == classroom.teacher:
                return redirect(f"/class/t/detail/{class_code}")
            else:
                messages.error(request, "Your not registered in this class enter class code and join.")
                return redirect("/class/join")

        return render(request, "classes/detail.html", context)


# --------Classmates-------
def classmates_view(request, code):
    context = {}
    if not request.user.is_authenticated:
        return redirect("/")
    else:
        class_code = code.strip()
        classroom = Classroom.objects.get(code=class_code)

        if request.user in classroom.students.all():
            classmates = classroom.students.all()
            context = {
                'classroom': classroom,
                'classmates': classmates
            }
        else:
            messages.error("Your not registered in this class enter class code and join.")
            return redirect("/class/join")

    return render(request, "classes/classmates.html", context)


def classwork_view(request, code):
    context = {}
    if not request.user.is_authenticated:
        return redirect("/")
    else:
        class_code = code.strip()
        classroom = Classroom.objects.get(code=class_code)

        if request.user in classroom.students.all():
            classworks = classroom.classwork_set.all()

            context = {
                'classroom': classroom,
                'classworks': classworks
            }
        else:
            messages.error("Your not registered in this class enter class code and join.")
            return redirect("/class/join")

    return render(request, "classes/classwork.html", context)


def classwork_submit_view(request, code, pk):
    context = {}
    if not request.user.is_authenticated:
        return redirect("/")
    else:
        class_code = code.strip()
        classroom = Classroom.objects.get(code=class_code)

        if request.user in classroom.students.all():
            classwork = classroom.classwork_set.get(id=pk)
            context = {
                'classroom': classroom,
                'classwork': classwork
            }
        else:
            messages.error("Your not registered in this class enter class code and join.")
            return redirect("/class/join")

    return render(request, "classes/classwork.html", context)
