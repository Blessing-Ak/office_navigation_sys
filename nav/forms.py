# forms.py
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate

UserModel = get_user_model()

class CustomSignupForm(forms.ModelForm):
    password = forms.CharField(label="Password", widget=forms.PasswordInput)
    confirm_password = forms.CharField(label="Confirm Password", widget=forms.PasswordInput)

    class Meta:
        model = UserModel
        fields = ['email', 'phone_number']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user



class CustomLoginForm(forms.Form):
    identifier = forms.CharField(label="Email or Phone Number")
    password = forms.CharField(label="Password", widget=forms.PasswordInput)

    def clean(self):
        identifier = self.cleaned_data.get('identifier')
        password = self.cleaned_data.get('password')
        from django.contrib.auth import get_user_model
        UserModel = get_user_model()
        try:
            # If identifier contains an '@', assume it's an email; otherwise, phone number.
            if '@' in identifier:
                user_obj = UserModel.objects.get(email=identifier)
            else:
                user_obj = UserModel.objects.get(phone_number=identifier)
        except UserModel.DoesNotExist:
            raise forms.ValidationError("Invalid email or phone number.")

        # Authenticate using the email (which is our USERNAME_FIELD)
        user = authenticate(username=user_obj.email, password=password)
        if user is None:
            raise forms.ValidationError("Invalid login credentials.")
        self.user = user
        return self.cleaned_data

    def get_user(self):
        return self.user
