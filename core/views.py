from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.http import JsonResponse
from .services import NoteService, TodoService

note_service = NoteService()
todo_service = TodoService()

# ---------------------------
# Dashboard
# ---------------------------
def dashboard(request):
    query = request.GET.get("q", "")
    now = timezone.now()

    # Get base stats and search results
    stats = todo_service.get_dashboard_stats(query)

    # Get reminders
    reminders = todo_service.get_reminders(now)

    # Get new features data
    # 1. TODAY'S FOCUS
    today_todos = todo_service.get_daily_focus(now)
    
    # 2. PRIORITY MATRIX
    matrix = todo_service.get_priority_matrix(now)

    context = {
        "notes_count": stats["notes_count"],
        "todos_count": stats["todos_count"],
        "completed_todos": stats["completed_todos"],
        "query": query,
        "notes_results": stats["notes_results"],
        "todos_results": stats["todos_results"],
        
        "upcoming_reminders": reminders["upcoming"],
        "overdue_reminders": reminders["overdue"],
        "soon_reminders": reminders["soon"],
        "overdue_count": reminders["overdue_count"],
        "soon_count": reminders["soon_count"],
        "show_reminder_alert": (reminders["overdue_count"] > 0) or (reminders["soon_count"] > 0),

        # New features
        "today_todos": today_todos,
        "important_urgent": matrix["important_urgent"],
        "important_not_urgent": matrix["important_not_urgent"],
        "all_important": matrix["all_important"],
    }
    return render(request, "dashboard.html", context)


def reminders_status(request):
    """AJAX endpoint returning JSON with overdue and soon reminders for client polling."""
    now = timezone.now()
    data = todo_service.get_reminders_status_data(now)
    return JsonResponse(data)


# ---------------------------
# Notes CRUD
# ---------------------------
def notes_list(request):
    notes = note_service.list_all()
    return render(request, "notes_list.html", {"notes": notes})

def notes_add(request):
    if request.method == "POST":
        success, result = note_service.create(request.POST)
        if success:
            return redirect("notes_list")
        form = result
    else:
        form = note_service.form_class()
    return render(request, "notes_form.html", {"form": form})

def notes_edit(request, id):
    # Retrieve object first to ensure 404 if not found (handled by get_by_id)
    note = note_service.get_by_id(id)
    
    if request.method == "POST":
        success, result = note_service.update(id, request.POST)
        if success:
            return redirect("notes_list")
        form = result
    else:
        form = note_service.form_class(instance=note)
    return render(request, "notes_form.html", {"form": form})

def notes_delete(request, id):
    note_service.delete(id)
    return redirect("notes_list")


# ---------------------------
# Todos CRUD
# ---------------------------
def todos_list(request):
    todos = todo_service.list_all()
    return render(request, "todos_list.html", {"todos": todos})

def todos_add(request):
    if request.method == "POST":
        success, result = todo_service.create(request.POST)
        if success:
            return redirect("todos_list")
        form = result
    else:
        form = todo_service.form_class()
    return render(request, "todos_form.html", {"form": form})

def todos_edit(request, id):
    todo = todo_service.get_by_id(id)
    if request.method == "POST":
        success, result = todo_service.update(id, request.POST)
        if success:
            return redirect("todos_list")
        form = result
    else:
        form = todo_service.form_class(instance=todo)
    return render(request, "todos_form.html", {"form": form})

def todos_delete(request, id):
    todo_service.delete(id)
    return redirect("todos_list")


# ---------------------------
# Todos Calendar
# ---------------------------
def todos_calendar(request):
    context = todo_service.get_calendar_data()
    return render(request, "todos_calendar.html", context)
