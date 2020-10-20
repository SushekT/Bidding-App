from django import forms
from .models import Post, Category, Bidding

class PostForm(forms.ModelForm):
    title = forms.CharField(label='Title of the Product', widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'E.g. Asus ROG 2', 'style':'width:150%;'}))
    minimumprice = forms.FloatField(label = 'Minimum Price', widget=forms.NumberInput(attrs={'class':'form-inline', 'placeholder':'E.g. 1000', 'style':'width:50%;'}))
    lastbiddate = forms.DateField(label = 'Last Bid Date', widget=forms.DateInput(attrs={'type':'date', 'class':'form-control', 'style':'width:25%; height:10%; border-radius:35%;'}))
    dayused = forms.IntegerField(label='Day Used',widget=forms.NumberInput(attrs={'class': 'form-inline', 'placeholder': 'E.g. 15','style':'width:50%;'}))
    description = forms.CharField(label='Description', widget=forms.Textarea(attrs={'class':'form-control', 'placeholder': 'E.g. This is a description'}))
    category = forms.ModelChoiceField(queryset=Category.objects.all(), widget=forms.Select(attrs={'class':'form-control'}))

    class Meta:
        model = Post
        exclude = ['slug', 'user']

class Biddingform(forms.ModelForm):
    bidingprice = forms.FloatField(label= 'Bidding Price', widget=forms.NumberInput(attrs={'class':'form-control'}))
    message = forms.CharField(label= 'Message', widget=forms.Textarea(attrs={'class':'form-control'}))
    class Meta:
        model = Bidding
        exclude = ['user', 'status', 'post', 'date', 'first_time']