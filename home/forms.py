from django import forms
from home.models import Post, Comment


class HomeForm(forms.ModelForm):

    #gán thuộc tính css bootstrap cho django form
    post = forms.CharField(widget=forms.Textarea(
        attrs= {
            'class': 'form-control',
            'placeholder': 'Bạn đang nghĩ gì đấy',
            'style': 'height: 100px',
        }
    ))

    class Meta:
        model = Post
        fields = ('post',)


class CommentForm(forms.ModelForm):
    body = forms.CharField(widget=forms.Textarea(
        attrs= {
            'class': 'form-control',
            'placeholder': 'Để lại một bình luận',
            'style': 'height: 70px',
        }
    ))
    def __init__(self, *args, **kwargs):
        self.author = kwargs.pop('author', None)
        self.post = kwargs.pop('post', None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        comment = super().save(commit=False)
        comment.author = self.author
        comment.post = self.post
        comment.save()

    class Meta:
        model = Comment
        fields = ["body"]