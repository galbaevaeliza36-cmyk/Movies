from django import forms
from films.models import Category

spisok_bad_films = [
    "Eliza", "Kaila"
]
class CreatFilmsForms(forms.Form):
    title = forms.CharField()
    description = forms.CharField()
    episodes = forms.IntegerField()

    def clean(self):
        data= self.cleaned_data
        title = data.get("title")
        if title in spisok_bad_films:
            raise forms.ValidationError("Этот фильм запрешено")
        return data 


    # def clean_title():
    #     title = self.cleaned_data.get("title")
    #     if title in spisok_bad_films:
    #         raise forms.ValidationError("Этот фильм запрешено")
    #     return title   


class SearchForm(forms.Form):
    choice_list = [("1","больше сто"),("2", "меньше сто")]
    search = forms.CharField(required=False, label="Search")
    category_id = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=False,
        label="Category"
    )
    episodes_choice=forms.ChoiceField(choices=choice_list)