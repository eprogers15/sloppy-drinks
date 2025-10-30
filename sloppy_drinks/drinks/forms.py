from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm, SetPasswordForm, PasswordChangeForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django import forms

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        help_text='Required. Please enter a valid email address.'
    )

    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ("email",)
    
    def clean_email(self):
        """Ensure email is unique"""
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError('A user with this email already exists.')
        return email
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Apply Bootstrap 'form-control' class to all fields
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'form-control',
                'placeholder': field.label,
            })
        
        # Customize specific fields if needed
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Choose a username',
            'autofocus': True,
        })
        
        self.fields['email'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'your.email@example.com',
        })
        
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Enter password',
        })
        
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Confirm password',
        })
        
        # Optionally add help text or remove default help text
        self.fields['username'].help_text = 'Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'
        self.fields['password1'].help_text = 'Your password must contain at least 8 characters.'

class CustomLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Apply Bootstrap classes to username field
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Username',
            'autofocus': True,
        })
        
        # Apply Bootstrap classes to password field
        self.fields['password'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Password',
        })
        
        # Optional: Remove help text if you don't want it
        self.fields['username'].help_text = None

class CustomPasswordResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Apply Bootstrap classes to email field
        self.fields['email'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Enter your email address',
            'autofocus': True,
        })
        
        # Update help text
        self.fields['email'].help_text = 'We\'ll send password reset instructions to this email.'

class CustomSetPasswordForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Apply Bootstrap classes
        self.fields['new_password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'New password',
            'autofocus': True,
        })
        
        self.fields['new_password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Confirm new password',
        })

class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Apply Bootstrap classes to all fields
        self.fields['old_password'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Current password',
            'autofocus': True,
        })
        
        self.fields['new_password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'New password',
        })
        
        self.fields['new_password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Confirm new password',
        })
        
        # Update labels for clarity
        self.fields['old_password'].label = 'Current Password'
        self.fields['new_password1'].label = 'New Password'
        self.fields['new_password2'].label = 'Confirm New Password'