from django import forms
from django.core.cache import cache
from django.forms import modelformset_factory
from tasks.fields import EmailListField
from tasks.models import SubscribedEmail, Task


# Model based form
class TaskForm(forms.ModelForm):
    watchers = EmailListField(required=False)

    def __init__(self, *args, **kwargs):
        super(TaskForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields["watchers"].initial = ", ".join([watcher.email for watcher in self.instance.watchers.all()])

    class Meta:
        model = Task
        fields = (
            "title",
            "description",
            "status",
            "watchers",
            "file_upload",
            "image_upload",
        )

    def save(self, commit=True):
        task = super(TaskForm, self).save(commit=False)

        if commit and task.pk:
            task.watchers.all().delete()

        for email_str in self.cleaned_data["watchers"]:
            SubscribedEmail.objects.create(email=email_str, task=task)

        return task


class TaskFormWithRedis(forms.ModelForm):
    uuid = forms.UUIDField(required=False, widget=forms.HiddenInput)
    watchers = EmailListField(required=False)

    def __init__(self, *args, **kwargs):
        super(TaskFormWithRedis, self).__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields["watchers"].initial = ", ".join([watcher.email for watcher in self.instance.watchers.all()])

    class Meta:
        model = Task
        fields = (
            "title",
            "description",
            "status",
            "watchers",
            "file_upload",
            "image_upload",
        )

    def save(self, commit=True):
        task = super(TaskFormWithRedis, self).save(commit=False)

        if commit and task.pk:
            task.watchers.all().delete()

        for email_str in self.cleaned_data["watchers"]:
            SubscribedEmail.objects.create(email=email_str, task=task)

        return task

    def clean_uuid(self):
        uuid_value = str(self.cleaned_data.get("uuid", ""))

        was_set = cache.set(uuid_value, "submitted", nx=True)

        if not was_set:
            # If was_set is False, then the key already exists
            raise forms.ValidationError("Form already submitted")

        return uuid_value


class ContactForm(forms.Form):
    from_email = forms.EmailField(required=True)
    subject = forms.CharField(required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)


EpicFormSet = modelformset_factory(Task, form=TaskForm, extra=0)
