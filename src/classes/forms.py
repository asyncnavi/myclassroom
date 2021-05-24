from django import forms
from .models import Classroom, Submission
from django.core.exceptions import ValidationError

class CreateClassForm(forms.ModelForm):
    name = forms.CharField(max_length=50)
    subject = forms.CharField(max_length=50)

    class Meta:
        model = Classroom
        fields = ('name', 'subject',)

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if not name or len(name) < 10:
            raise ValidationError(
                'Classname cannot be less than 10 characters',
            )
        if len(name) > 50:
            raise ValidationError(
                'Classname cannot be greated than 50 characters',
            )
        return name

    def clean_subject(self):
        subject = self.cleaned_data.get('subject')
        if not subject or len(subject) < 2:
            raise ValidationError(
                'Subject should be greater than 2 characters',
            )
        if len(subject) > 50:
            raise ValidationError(
                'Subject should be less than 50 character',
            )

        return subject
