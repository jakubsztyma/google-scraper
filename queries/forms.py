from django import forms


class QueryForm(forms.Form):
    phrase = forms.CharField(label='Query', max_length=1000)
