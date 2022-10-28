from django import forms
from tinymce.widgets import TinyMCE
from .models import Post, Comment


class TinyForm(forms.ModelForm):
    name = forms.CharField(max_length=560)
    content = forms.CharField(widget=TinyMCE(attrs={'cols':80,'rows':30}))

    class Meta:
        model = Post
        fields = ('name', 'content', )


class TinyCommentForm(forms.ModelForm):
    content = forms.CharField(widget=TinyMCE(attrs={'cols':80,'rows':30}))

    class Meta:
        model = Comment
        fields = ('content', )
