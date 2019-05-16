from django import forms
from recipes.models import Recipe


class NewRecipesForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['title', 'image', 'description', 'difficulty', 'ingredients']

    def __init__(self, *args, **kwargs):
        super(NewRecipesForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs['class'] = 'form-control'
        self.fields['description'].widget.attrs['class'] = 'form-control'
        self.fields['difficulty'].widget.attrs['class'] = 'form-control'
        self.fields['ingredients'].widget.attrs['class'] = 'form-control'
