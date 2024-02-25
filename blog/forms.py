from django import forms
from .models import Post


class EmailForm(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    description = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': 3}))


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'slug', 'status', 'publish', 'text', 'author']
