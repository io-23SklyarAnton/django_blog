from django import forms

from .models import Post, Comment


class EmailForm(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    description = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': 3}))


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'slug', 'status', 'publish', 'text', 'tags']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']
        widgets = {
            'body': forms.Textarea(attrs={'cols': 200, 'rows': 3, 'font_size': 16})
        }
        labels = {
            'body': 'Comment'
        }
