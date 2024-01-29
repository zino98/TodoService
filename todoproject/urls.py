
from django.contrib import admin
from django.urls import path

from todoapp import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("todo/", views.TodoView.as_view()),  # todo/.. URL 모두 처리
]
