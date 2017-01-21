from django import forms
from django.contrib.auth.models import User
from rango.models import Page, Category, UserProfile, data

class CategoryForm(forms.ModelForm):
    name = forms.CharField(max_length=128,
                           help_text="please enter the category name.")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Category
        fields = ('name',)

class PageForm(forms.ModelForm):
    title = forms.CharField(max_length=128,
                            help_text="Please enter the title of the page.")
    url = forms.URLField(max_length=200,
                        help_text="Please enter the URL of the page.")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

    class Meta:
        model = Page
        exclude = ('category',)

    def clean(self):
        cleaned_data = self.cleaned_data
        url = cleaned_data.get('url')

        if url and not url.startswith('http://'):
            url = 'http://' + url
            cleaned_data['url'] = url
            return cleaned_data

class dataForm(forms.ModelForm):
    class Meta:
        model = data
        fields = ('date','treatment','notes','satisfaction',)
    
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, help_text="*")
    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        help_texts = {
            'username': "*",
            'email': "*",
            }

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('legalName', 'knownName', 'birthDate', 'gender', 'birthGender')
        help_texts = {
            'legalName': "*",
            'birthDate': "*",
            'birthGender': "*",
        }
