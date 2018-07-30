from django import forms

class ArticleForm(forms.Form):

    title = forms.CharField(label="标题", max_length=256)
    content = forms.CharField(widget=forms.Textarea)
