from django import forms
from .models import Note, Todo

class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ["title", "content"]

class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ["task", "done", "due_date", "activity", "activity_custom", "reminder", "is_important"]
        widgets = {
            "due_date": forms.DateInput(attrs={"type": "date"}),
            "activity": forms.Select(),
            "activity_custom": forms.TextInput(attrs={"placeholder": "Enter custom activity (visible when 'Other' selected)"}),
            # Use datetime-local so browsers show a combined date+time picker
            "reminder": forms.DateTimeInput(attrs={"type": "datetime-local"}, format="%Y-%m-%dT%H:%M"),
            "is_important": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # If bound data isn't present, ensure the datetime-local widget displays existing value correctly
        if self.instance and self.instance.reminder:
            # Convert to string matching the widget format (no timezone)
            self.initial.setdefault('reminder', self.instance.reminder.strftime('%Y-%m-%dT%H:%M'))

    def clean(self):
        cleaned = super().clean()
        activity = cleaned.get('activity')
        activity_custom = cleaned.get('activity_custom') or ''
        # If activity is not custom, clear custom field to avoid stray text
        if activity != Todo.ACTIVITY_OTHER:
            cleaned['activity_custom'] = ''
        else:
            cleaned['activity_custom'] = activity_custom.strip()
        # reminder will be parsed by Django; no extra cleaning needed here
        return cleaned
