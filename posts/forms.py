from django import forms
from .models import Post, Comment

class PostForm(forms.ModelForm):
    tags = forms.CharField(max_length=100, required=False, help_text='Enter tags separated by commas.')

    class Meta:
        model = Post
        fields = ['image', 'content', 'tags']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Add a comment...'})
        }
