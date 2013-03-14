from django import forms


class SearchEntry(forms.Form):
    street_address = forms.CharField(max_length=50)
    city_zip = forms.CharField(max_length=30)
    search_distance = forms.CharField(max_length=3)
