from django import forms
from .models import Book,BookRating


class BookAddForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ('title', 'author', 'category', 'cover', 'pdf')

class BookRatingForm(forms.ModelForm):
    class Meta:
        model = BookRating
        fields = ['rating']
        widgets = {
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 5}),
        }