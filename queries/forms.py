from django import forms


class QueryForm(forms.Form):
    phrase = forms.CharField(label='Provide your query:', max_length=1000)
