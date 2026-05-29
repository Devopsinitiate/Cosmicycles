from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile, Business, JournalEntry


class SignUpForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'w-full bg-gray-700 border border-gray-600 text-white rounded-lg px-4 py-2 focus:outline-none focus:border-purple-500 focus:ring-1 focus:ring-purple-500',
            'placeholder': 'Enter your email',
        })
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['birth_date', 'gender']
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'})
        }

class BusinessForm(forms.ModelForm):
    class Meta:
        model = Business
        fields = ['name', 'start_date']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'})
        }

class JournalEntryForm(forms.ModelForm):
    class Meta:
        model = JournalEntry
        fields = ['content', 'mood']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3, 'placeholder': 'How did your day go? What activities aligned with your cycles?'}),
            'mood': forms.Select(choices=[(1, 'Poor'), (2, 'Fair'), (3, 'Good'), (4, 'Great'), (5, 'Excellent')]),
        }