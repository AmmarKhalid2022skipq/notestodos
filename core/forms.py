from django import forms
from .models import Note, Todo

class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ["title", "content"]

class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ["task", "done", "due_date"]  # only valid fields
        widgets = {
            "due_date": forms.DateInput(attrs={"type": "date"})
        }
