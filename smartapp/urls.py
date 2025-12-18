from django.contrib import admin
from django.urls import path
from core import views
urlpatterns = [
    path("", views.dashboard, name="dashboard"),

    # Notes
    path("notes/", views.notes_list, name="notes_list"),
    path("notes/add/", views.notes_add, name="notes_add"),
    path("notes/edit/<int:id>/", views.notes_edit, name="notes_edit"),
    path("notes/delete/<int:id>/", views.notes_delete, name="notes_delete"),

    # Todos
    path("todos/", views.todos_list, name="todos_list"),
    path("todos/add/", views.todos_add, name="todos_add"),
    path("todos/edit/<int:id>/", views.todos_edit, name="todos_edit"),
    path("todos/delete/<int:id>/", views.todos_delete, name="todos_delete"),
    # Todos calendar
    path("todos/calendar/", views.todos_calendar, name="todos_calendar"),

    # Reminders JSON endpoint for live polling
    path("reminders/status/", views.reminders_status, name="reminders_status"),

    # Admin
    path("admin/", admin.site.urls),
]
