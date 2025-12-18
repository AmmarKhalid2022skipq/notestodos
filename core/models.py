from django.db import models

class Note(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Todo(models.Model):
    task = models.CharField(max_length=255)
    done = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateField(null=True, blank=True)  # optional due date

    # Activities: choices plus an optional custom text field
    ACTIVITY_SHOPPING = 'shopping'
    ACTIVITY_MEETING = 'meeting'
    ACTIVITY_OUTDOOR = 'outdoor'
    ACTIVITY_WORKOUT = 'workout'
    ACTIVITY_OTHER = 'custom'

    ACTIVITY_CHOICES = [
        (ACTIVITY_SHOPPING, 'Shopping'),
        (ACTIVITY_MEETING, 'Meeting'),
        (ACTIVITY_OUTDOOR, 'Outdoor'),
        (ACTIVITY_WORKOUT, 'Workout'),
        (ACTIVITY_OTHER, 'Other (custom)')
    ]

    activity = models.CharField(max_length=50, choices=ACTIVITY_CHOICES, default=ACTIVITY_OTHER)
    activity_custom = models.CharField(max_length=100, blank=True, default='')

    # Reminder datetime (optional)
    reminder = models.DateTimeField(null=True, blank=True)

    # Priority marker - user can mark if task is important
    is_important = models.BooleanField(default=False)

    def get_activity_display(self):
        """Return the display label for the activity, preferring custom text when set."""
        if self.activity == self.ACTIVITY_OTHER and self.activity_custom:
            return self.activity_custom
        return dict(self.ACTIVITY_CHOICES).get(self.activity, self.activity)

    def __str__(self):
        # show custom activity when provided
        activity_display = self.get_activity_display()
        # include reminder in the string if present
        if self.reminder:
            return f"{self.task} [{activity_display}] (reminder: {self.reminder})"
        return f"{self.task} [{activity_display}]"
