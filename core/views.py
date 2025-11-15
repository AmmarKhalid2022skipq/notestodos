from django.shortcuts import render, get_object_or_404, redirect
from .models import Note, Todo
from .forms import NoteForm, TodoForm

# ---------------------------
# Dashboard
# ---------------------------
def dashboard(request):
    query = request.GET.get("q", "")

    notes_count = Note.objects.count()
    todos_count = Todo.objects.count()
    completed_todos = Todo.objects.filter(done=True).count()

    notes_results = Note.objects.filter(title__icontains=query) if query else []
    todos_results = Todo.objects.filter(task__icontains=query) if query else []

    context = {
        "notes_count": notes_count,
        "todos_count": todos_count,
        "completed_todos": completed_todos,
        "query": query,
        "notes_results": notes_results,
        "todos_results": todos_results,
    }
    return render(request, "dashboard.html", context)


# ---------------------------
# Notes CRUD
# ---------------------------
def notes_list(request):
    notes = Note.objects.all().order_by("-created_at")
    return render(request, "notes_list.html", {"notes": notes})

def notes_add(request):
    if request.method == "POST":
        form = NoteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("notes_list")
    else:
        form = NoteForm()
    return render(request, "notes_form.html", {"form": form})

def notes_edit(request, id):
    note = get_object_or_404(Note, id=id)
    if request.method == "POST":
        form = NoteForm(request.POST, instance=note)
        if form.is_valid():
            form.save()
            return redirect("notes_list")
    else:
        form = NoteForm(instance=note)
    return render(request, "notes_form.html", {"form": form})

def notes_delete(request, id):
    note = get_object_or_404(Note, id=id)
    note.delete()
    return redirect("notes_list")


# ---------------------------
# Todos CRUD
# ---------------------------
def todos_list(request):
    todos = Todo.objects.all().order_by("-created_at")
    return render(request, "todos_list.html", {"todos": todos})

def todos_add(request):
    if request.method == "POST":
        form = TodoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("todos_list")
    else:
        form = TodoForm()
    return render(request, "todos_form.html", {"form": form})

def todos_edit(request, id):
    todo = get_object_or_404(Todo, id=id)
    if request.method == "POST":
        form = TodoForm(request.POST, instance=todo)
        if form.is_valid():
            form.save()
            return redirect("todos_list")
    else:
        form = TodoForm(instance=todo)
    return render(request, "todos_form.html", {"form": form})

def todos_delete(request, id):
    todo = get_object_or_404(Todo, id=id)
    todo.delete()
    return redirect("todos_list")


# ---------------------------
# Todos Calendar
# ---------------------------
def todos_calendar(request):
    # Pending and completed todos
    pending_todos = Todo.objects.filter(due_date__isnull=False, done=False).order_by("due_date")
    completed_todos = Todo.objects.filter(due_date__isnull=False, done=True).order_by("due_date")

    # Group todos by month
    def group_by_month(todos):
        grouped = {}
        for todo in todos:
            month = todo.due_date.strftime("%B %Y")  # e.g., "October 2025"
            grouped.setdefault(month, []).append(todo)
        return grouped

    grouped_pending = group_by_month(pending_todos)
    grouped_completed = group_by_month(completed_todos)

    context = {
        "grouped_pending": grouped_pending,
        "grouped_completed": grouped_completed,
    }
    return render(request, "todos_calendar.html", context)
