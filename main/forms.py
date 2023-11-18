from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import ReadingList, Story
from ckeditor.widgets import CKEditorWidget


class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
            userReadingList = ReadingList(assigned_user=user)
        return user 

class StoryForm(ModelForm):
        date = forms.DateField(help_text="(Year-Month-Day)")
        content = forms.CharField(required=False, widget=CKEditorWidget(), help_text="Copy and pasting images from Google Docs")
        story_image = forms.ImageField(required=False, help_text="<br> <strong>Please credit image in first article sentence. Clear last image and save to change photo.</strong>")
        class Meta:
            model = Story
            fields = ["title", "category", "story_image", "date", "content"]