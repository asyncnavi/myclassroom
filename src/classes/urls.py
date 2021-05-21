from django.urls import path

from .views import *

urlpatterns = [
    path('', class_index_view, name="classes"),
    path('created', created_classes_view, name="created-classes"),
    path('create', create_class_view, name="create-class"),
    path('delete', delete_class_view, name="delete-class"),

]
