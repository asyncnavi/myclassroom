from django.shortcuts import render, redirect, Http404
from .models import Classroom, Submission
from .forms import CreateClassForm
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from .helpers import redirect_back


# --------Joined classes-------
def joined_classes(request):
    if not request.user.is_authenticated:
        redirect_back(request, "/")

    classes = Classroom.objects.filter(students=request.user)

    context = {
        'joined_classes': classes
    }

    return render(request, 'classes/index.html', context)


# --------Created classes-------
def created_classes(request):
    if not request.user.is_authenticated:
        return redirect("/")

    classrooms = Classroom.objects.filter(teacher=request.user)

    context = {
        "created_classes": classrooms
    }

    return render(request, 'classes/created.html', context)


# --------Creating new class-------
def create_class(request):
    if not request.user.is_authenticated:
        return redirect("/")
    form = CreateClassForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            intance = form.save(commit=False)
            intance.teacher = request.user
            intance.save()

            messages.success(request, f"class created with code successfully")
            return redirect("/class/created")

    context = {
        'form': form
    }
    return render(request, "classes/create.html", context)


# --------Delete class(By teacher)-------
def delete_class(request):
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


# --------Join a class-------
def join_class(request):
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


# --------Class detailed view-------
def joined_class_detail(request, code):
    context = {}
    if not request.user.is_authenticated:
        return redirect("/")

    class_code = code.strip()
    classroom = None
    try:
        classroom = Classroom.objects.get(code=class_code)
    except Classroom.DoesNotExist:
        pass

    if request.user in classroom.students.all():
        posts = classroom.post_set.all()
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

    return render(request, "classes/j_detail.html", context)


def created_class_detail():
    pass


# --------Classmates-------
def classmates(request, code):
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

    return render(request, "classes/j_classmates.html", context)


def classwork_list(request, code):
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

    return render(request, "classes/j_classwork.html", context)


def classwork_detail(request, code, pk):
    context = {}
    if not request.user.is_authenticated:
        return redirect("/")
    else:
        class_code = code.strip()
        classroom = Classroom.objects.get(code=class_code)
        if request.user in classroom.students.all():
            classwork = classroom.classwork_set.get(pk=pk)
            submission = None
            is_submitted = False
            try:
                submission = classwork.submission_set.get(student=request.user)
                is_submitted = True
            except Submission.DoesNotExist:
                is_submitted = False

            context = {
                'classroom': classroom,
                'classwork': classwork,
                'is_submitted': is_submitted,
                'submission': submission
            }
        else:
            messages.error("Your not registered in this class enter class code and join.")
            return redirect("/class/join")

    return render(request, "classes/j_submit_classwork.html", context)


def submit_classwork(request):
    if not request.user.is_authenticated:
        return redirect("/")

    if request.method == "POST":
        user = request.user
        file = request.FILES.get("uploaded_file")
        code = request.POST["class_code"]
        classwork_id = request.POST["classwork_id"]
        print(f"code = {code}", f"claswork_id =  {classwork_id}")
        classroom = None
        classwork = None
        class_code = code.strip()
        try:
            classroom = Classroom.objects.get(code=class_code)
        except Classroom.DoesNotExist:
            pass

        try:
            classwork = classroom.classwork_set.get(pk=classwork_id)
        except Classroom.DoesNotExist:
            pass

        if classwork.is_submission_ended():
            messages.error(request, "Deadline is ended")
            return redirect(f"/class/classwork/{class_code}/{classwork_id}")

        submission = Submission.objects.create(student=user, classwork=classwork, uploaded_file=file, is_submitted=True)
        submission.save()
        messages.success(request, "Your work was uploaded")
        return redirect(f"/class/classwork/{class_code}/{classwork_id}")
    return Http404(request)
