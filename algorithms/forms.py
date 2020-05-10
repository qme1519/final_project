from django import forms

# define choices user has
CHOICES = [
('csv', 'Load csv file'),
('own', 'Input your own array (syntax: comma sepparated values, e.g. 1, 2, 3, 4, 5)'),
('random', 'Generate random array (syntax: start, end, number of entries, e.g. -5, 5, 7)')
]

# define form that user will complete
class Form(forms.Form):
    # user input depending on choice
    description = forms.CharField(
        required=False,
        max_length=60,
        widget=forms.TextInput(
            attrs={
            "class": "form-control",
            "placeholder": "Your array/length of random array"
            }
        ),
    )
    # radio buttons for choices
    choice = forms.MultipleChoiceField(
            required=True,
            widget=forms.RadioSelect(attrs = {
            'onclick' : "ShowHideForms();",
            }
            ),
            choices=CHOICES,
        )
    # file upload
    file = forms.FileField(required=False)
    # for search only: target element
    target = forms.CharField(
        required=True,
        max_length=60,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Target element"}
        ),
    )
