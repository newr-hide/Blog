from django import forms
from .models import Post, Comment


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'image', 'content', 'author']
        labels = {
            'title': '',
            'image': '',
            'content': '',
            'author': '',
        }
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Название статьи', 'class': 'w-50'}),
            'content': forms.Textarea(attrs={'placeholder': 'Ваша статья...', 'class': 'w-100'}),
            'author': forms.TextInput(attrs={'placeholder': 'Имя автора', 'class': 'w-50'})
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text', 'author']
        labels = {
            'text': '',
            'author': '',
        }
        widgets = {'text': forms.Textarea(attrs={'placeholder': 'Ваш комментарий...', 'rows': 4, 'class': 'w-100'}),
                   'author': forms.TextInput(attrs={'placeholder': 'имя комментатора...', 'class': 'w-50'})
                   }
