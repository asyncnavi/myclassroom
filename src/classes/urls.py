from django.urls import path

from .views import *

urlpatterns = [
    path('', class_index_view, name="classes"),
    path('detail/<str:code>', class_detail_view),
    path('classmates/<str:code>', classmates_view),
    path('classwork/<str:code>', classwork_view),
    path('classwork/<str:code>/<str:pk>', classwork_submit_view),
    path('created', created_classes_view, name="created-classes"),
    path('create', create_class_view, name="create-class"),
    path('delete', delete_class_view, name="delete-class"),
    path('join', join_class_view, name="join-class"),

]
