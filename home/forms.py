from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User, AbstractUser
from django.core.validators import EmailValidator

class UserForm(UserCreationForm):
    
    email = forms.EmailField(validators=[EmailValidator(message='Enter a valid email address.')])
    class Meta:
        model = User
        fields = ('first_name','last_name','username', 'email', 'password1','password2', 'is_superuser')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control m-3 form-floating '})  
            field.help_text=''

        if not self.instance.is_superuser:
            print(self.instance.username, " = ", self.instance.is_superuser)
            self.fields['is_superuser'].widget = forms.HiddenInput()

        self.fields['is_superuser'].widget.attrs.update({'class': 'form-check-input'})
        self.fields['username'].required = False  
        

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match")
        return password2
    