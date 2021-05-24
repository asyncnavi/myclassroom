from django.urls import path

from .views import *

# j stands for joined
# c stands for creatd

urlpatterns = [
    path('', joined_classes, name="joined-classes"),
    path('create', create_class, name="create-class"),
    path('join', join_class, name="join-class"),
    path('j/<str:code>', joined_class_detail, name="detailed-joined-class"),
    path('j/classmates/<str:code>', classmates, name="listed-classmates"),
    path('j/classwork/<str:code>', classwork_list, name="listed-classwork"),
    path('j/classwork/submit', submit_classwork, name="submit-classwork"),
    path('j/classwork/d/<str:code>/<int:pk>', classwork_detail, name="detailed-classwork"),
    # for created classes
    path('created', created_classes, name="created-classes"),
    path('c/<str:code>', created_class_detail, name="detailed-created-class"),
    path('delete', delete_class, name="delete-class"),
]
