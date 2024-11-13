from django import forms


class SelectPramForm(forms.Form):
    count_recipe = forms.IntegerField(min_value=0)


class CategoryForm(forms.Form):
    title = forms.CharField(max_length=100)
    description = forms.TimeField()
