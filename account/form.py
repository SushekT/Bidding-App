from django import forms
from .models import Account,gender_list

class editprofileform(forms.ModelForm):
    email = forms.EmailField(label='Email', disabled=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    date_of_birth = forms.DateField(label= 'Date Of Birth',disabled=True, widget=forms.DateInput(attrs={'class':'form-control','type':'date'}))
    country = forms.CharField(label= 'Country', disabled=True,widget=forms.TextInput(attrs={'class':'form-control'}))
    gender = forms.ChoiceField(label= 'Gender',disabled=True, widget=forms.Select(attrs={'class':'form-control'}), choices=gender_list)
    address = forms.CharField(label= 'Address',disabled=True, widget=forms.TextInput(attrs={'class':'form-control'}))
    contact_no = forms.IntegerField(label= 'Contact Number',disabled=True, widget=forms.NumberInput(attrs={'class':'form-control'}))
    image = forms.ImageField(label= 'Update Profile', disabled=True, widget=forms.FileInput(attrs={'class':'form-control'}))
    class Meta:
        model = Account
        exclude = ['password', 'last_login', 'is_admin', 'is_active', 'is_verified','token',]
