from django import forms
from django.core.mail import send_mail

from .models import Post, Comment


class EmailForm(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    description = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': 3}))

    def send_mail(self, request, post):
        post_url = request.build_absolute_uri(post.get_absolute_url())
        title = f"{self.cleaned_data['name']} wants you to read {post.title}"
        description = f"he sent you this message: {self.cleaned_data['description']}. Watch it on {post_url}"
        send_mail(title, description, '80kap.i.toshka@gmail.com', [self.cleaned_data['to']])


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'slug', 'status', 'publish', 'text', 'author']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'mail', 'body']
