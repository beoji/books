from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.shortcuts import render

from .models import Author, Book
from .forms import BookForm, AuthorForm, SearchForm, GoogleForm

import requests


# Book Views


class BookList(ListView):

    context_object_name = 'books'
    model = Book
    paginate_by = 100
    template_name = 'catalog/book-list.html'

    def get_queryset(self):
        # Wyszukiwanie w katalogu
        title = self.request.GET.get('title')
        author = self.request.GET.get('author')
        language = self.request.GET.get('language')
        date_begin = self.request.GET.get('date_begin')
        date_end = self.request.GET.get('date_end')
        qs = Book.objects.all()
        if title:
            qs = qs.filter(title__icontains=title)
        if author:
            qs = qs.filter(Q(author__first_name__icontains=author) |
                           Q(author__last_name__icontains=author))
        if language:
            qs = qs.filter(language__icontains=language)
        if date_begin:
            qs = qs.filter(publication_date__gte=date_begin)
        if date_end:
            qs = qs.filter(publication_date__lte=date_end)
        return qs

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(BookList, self).get_context_data(**kwargs)
        context['search_form'] = SearchForm(self.request.GET or None)
        return context


class BookCreate(CreateView):

    form_class = BookForm
    template_name = 'catalog/book-add.html'
    success_url = reverse_lazy('book-list')


class BookUpdate(UpdateView):

    form_class = BookForm
    model = Book
    template_name = 'catalog/book-add.html'
    success_url = reverse_lazy('book-list')


class BookDelete(DeleteView):

    model = Book
    template_name = 'catalog/book-delete.html'
    success_url = reverse_lazy('book-list')


# Author Views


class AuthorList(ListView):

    context_object_name = 'authors'
    model = Author
    paginate_by = 100
    template_name = 'catalog/author-list.html'


class AuthorCreate(CreateView):

    form_class = AuthorForm
    template_name = 'catalog/book-add.html'
    success_url = reverse_lazy('author-list')


class AuthorUpdate(UpdateView):

    form_class = AuthorForm
    model = Author
    template_name = 'catalog/book-add.html'
    success_url = reverse_lazy('author-list')


class AuthorDelete(DeleteView):

    model = Author
    template_name = 'catalog/book-delete.html'
    success_url = reverse_lazy('auhtor-list')


# Google Api Views


def google_search(request):
    temlpate_name = 'catalog/google-search.html'
    form = GoogleForm(request.POST or None)
    context = {'form': form}

    if form.is_valid() and form.is_bound:
        # request.session['google_form'] = form
        if not request.session.get('books_per_page'):
            request.session['books_per_page'] = 12
        count = request.session['books_per_page']
        start = request.GET.get('start', 0)
        url = make_url(form, count, start)
        response = requests.get(url)
        book_data = response.json()
        books = book_data['items']
        count_books = book_data['totalItems']
        context.update({'books': books, 'count_books': count_books})
    return render(request, temlpate_name, context=context)

def make_url(form, count, start):
    url = 'https://www.googleapis.com/books/v1/volumes'
    url += '?q=' + form.cleaned_data['q']
    for key, value in form.cleaned_data.items():
        if value != '' and key != 'q':
            url += '+' + key + ':' + value
    url += '&maxResults=' + str(count) + '&startIndex=' + str(start)
    return url

# def download_books(url):
#     response = requests.get(url)
#     book_data = response.json()
#     count_books = book_data['totalItems']
#     x = 40 
#     while x < count_books:
#         api = url + '&startIndex=' + str(x)
#         print(api)
#         response = requests.get(api)
#         data = response.json()
#         book_data.update(data)
#         x += 40
#     return book_data['items'], count_books

def change_books_per_page(request):
    if request.GET.get('bpp'):
        request.session['books_per_page'] = request.GET.get('bpp')
    return JsonResponse({})