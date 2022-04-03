from django import forms
from django.utils.text import slugify
from django.conf.global_settings import LANGUAGES

from .models import Author, Book


class BookForm(forms.ModelForm):

    class Meta:
        model = Book
        fields = '__all__'
        widgets = {'publication_date': forms.widgets.DateInput(attrs={'type': 'date'})}


class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        exclude = ['slug']
        widgets = {'date_of_birth': forms.widgets.DateInput(attrs={'type': 'date'}),
                   'date_of_death': forms.widgets.DateInput(attrs={'type': 'date'})}

    def clean(self, *args, **kwargs):
        # Is new author unique?
        cleaned_data = super(AuthorForm, self).clean(*args, **kwargs)
        name = cleaned_data.get('first_name')
        surname = cleaned_data.get('last_name')
        if name and surname:
            slug = slugify(surname + ' ' + name)
            qs = Author.objects.filter(slug=slug).exists()
            if qs:
                raise forms.ValidationError("Autor już istnieje")
        return cleaned_data


lang = LANGUAGES.copy()
lang.insert(0, (None, '-'))


class SearchForm(forms.Form):
    title = forms.CharField(required=False, label='Tytuł')
    author = forms.CharField(required=False, label='Autor')
    language = forms.ChoiceField(choices=lang, required=False, label='Język')
    date_begin = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}), required=False, label='Data od')
    date_end = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}), required=False, label='Data do')


class GoogleForm(forms.Form):
    q = forms.CharField(required=False, label='Szukaj')
    intitle = forms.CharField(required=False, label='Tytuł')
    inauthor = forms.CharField(required=False, label='Autor')
    inpublisher = forms.CharField(required=False, label='Wydawnictwo')
    subject = forms.CharField(required=False, label='Tematyka')
    isbn = forms.CharField(required=False, label='ISBN')
    lccn = forms.CharField(required=False, label='LCCN')
    oclc = forms.CharField(required=False, label='OCLC')