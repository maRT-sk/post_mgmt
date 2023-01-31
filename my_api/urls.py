from django.urls import path, include
from .views import (
    MyApiView,
    )

urlpatterns = [
    path('posts/', MyApiView.as_view()),
    path('posts/<int:post_id>', MyApiView.as_view()),
    ]
