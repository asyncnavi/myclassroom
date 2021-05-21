from django import forms
from .models import Classroom


class CreateClassForm(forms.ModelForm):

    name = forms.CharField(max_length=50)
    subject = forms.CharField(max_length=50)

    class Meta:
        model = Classroom
        fields = ('name', 'subject')

    def clean(self):

        name = self.cleaned_data.get('name')
        subject = self.cleaned_data.get('subject')

        if not name or len(name) < 10:
            raise forms.ValidationError(
                {'name': ['Classname cannot be less than 10 characters']}
            )
        if len(name) > 50:
            raise forms.ValidationError(
               { 'name' : ['Classname cannot be greated than 50 characters']} 
            )
        if not subject or len(subject) < 2:
            raise forms.ValidationError(
                { 'subject' : ['Subject should be greater than 2 characters'] }
            )    
        if len(subject) > 50:
            raise forms.ValidationError(
               { 'subject' : ['Subject should be less than 50 character']} 
            )

        return super(CreateClassForm, self).clean()
