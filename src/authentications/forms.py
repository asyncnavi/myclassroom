from django import forms
from django.contrib.auth.forms import UsernameField, UserCreationForm
from django.contrib.auth import get_user_model, password_validation, authenticate
from django.utils.translation import gettext, gettext_lazy as _
from django.core.exceptions import ValidationError

User = get_user_model()


class AdminUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = "__all__"


class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(
        label=_("Password"),
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
    )

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        if username is not None and password:
            user = authenticate(username=username, password=password)
            if user is None:
                raise ValidationError(
                    "Please enter a valid username and password.",
                    code='invalid_login',
                )
            if not user.is_active:
                raise ValidationError(
                    "User is inactive.",
                    code='inactive',
                )
        return super(UserLoginForm, self).clean()


class SignUpForm(forms.ModelForm):
    error_messages = {
        'password_mismatch': _('Both password\'s should be same.'),
        'email_exists': _('Email is already registered.'),
        'username_exists': _('username is already exists.')
    }

    name = forms.CharField(required=True, max_length=30)
    username = forms.CharField(required=True)
    email = forms.EmailField(required=True, max_length=254)
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
    )
    confirmed_password = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        strip=False,
        help_text=_("Enter the same password as before, for verification."),
    )

    class Meta:
        model = User
        fields = ('name', 'username', 'email',
                  'password', 'confirmed_password')
        field_classes = {'username': UsernameField}

    def clean_email(self):
        email = self.cleaned_data.get("email")

        if User.objects.filter(email=email).exists():
            raise ValidationError(
                self.error_messages['email_exists'],
                code="email_exists"
            )
        return email

    def clean_confirmed_password(self):
        password = self.cleaned_data.get("password")
        confirmed_password = self.cleaned_data.get("confirmed_password")
        if password and confirmed_password and password != confirmed_password:
            raise ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return confirmed_password

    def _post_clean(self):
        super()._post_clean()
        password = self.cleaned_data.get('confirmed_password')
        if password:
            try:
                password_validation.validate_password(password, self.instance)
            except ValidationError as error:
                self.add_error('confirmed_password', error)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user
