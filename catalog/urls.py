from django.urls import path
from .views import *


urlpatterns = [
    # Book
    path('', BookList.as_view(), name='book-list'),
    path('book-add/', BookCreate.as_view(), name='book-create'),
    path('book-edit/<int:pk>/', BookUpdate.as_view(), name='book-update'),
    path('book-remove/<int:pk>/', BookDelete.as_view(), name='book-delete'),
    # Author
    path('author-list/', AuthorList.as_view(), name='author-list'),
    path('author-add/', AuthorCreate.as_view(), name='author-create'),
    path('author-edit/<int:pk>/', AuthorUpdate.as_view(), name='author-update'),
    path('author-remove/<int:pk>/', AuthorDelete.as_view(), name='author-delete'),
    # Google Api Views
    path('google-books-search/', google_search, name='google-search'),
    path('google-books-search/change-books-per-page/', change_books_per_page),
]
