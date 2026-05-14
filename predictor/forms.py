"""
Forms for the lung cancer prediction input.
"""
from django import forms

# Choices for Yes/No fields (1=No, 2=Yes in dataset)
YES_NO_CHOICES = [
    ('1', 'No'),
    ('2', 'Yes'),
]

GENDER_CHOICES = [
    ('M', 'Male'),
    ('F', 'Female'),
]


class PredictionForm(forms.Form):
    """Form for collecting patient data for lung cancer prediction."""
    
    # Personal Information
    GENDER = forms.ChoiceField(
        choices=GENDER_CHOICES,
        label='Gender',
        widget=forms.Select(attrs={
            'class': 'form-select',
            'id': 'input-gender'
        })
    )
    
    AGE = forms.IntegerField(
        label='Age',
        min_value=1,
        max_value=120,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter age',
            'id': 'input-age'
        })
    )
    
    # Lifestyle Factors
    SMOKING = forms.ChoiceField(
        choices=YES_NO_CHOICES,
        label='Smoking',
        widget=forms.Select(attrs={
            'class': 'form-select',
            'id': 'input-smoking'
        })
    )
    
    YELLOW_FINGERS = forms.ChoiceField(
        choices=YES_NO_CHOICES,
        label='Yellow Fingers',
        widget=forms.Select(attrs={
            'class': 'form-select',
            'id': 'input-yellow-fingers'
        })
    )
    
    ANXIETY = forms.ChoiceField(
        choices=YES_NO_CHOICES,
        label='Anxiety',
        widget=forms.Select(attrs={
            'class': 'form-select',
            'id': 'input-anxiety'
        })
    )
    
    PEER_PRESSURE = forms.ChoiceField(
        choices=YES_NO_CHOICES,
        label='Peer Pressure',
        widget=forms.Select(attrs={
            'class': 'form-select',
            'id': 'input-peer-pressure'
        })
    )
    
    CHRONIC_DISEASE = forms.ChoiceField(
        choices=YES_NO_CHOICES,
        label='Chronic Disease',
        widget=forms.Select(attrs={
            'class': 'form-select',
            'id': 'input-chronic-disease'
        })
    )
    
    # Symptoms
    FATIGUE = forms.ChoiceField(
        choices=YES_NO_CHOICES,
        label='Fatigue',
        widget=forms.Select(attrs={
            'class': 'form-select',
            'id': 'input-fatigue'
        })
    )
    
    ALLERGY = forms.ChoiceField(
        choices=YES_NO_CHOICES,
        label='Allergy',
        widget=forms.Select(attrs={
            'class': 'form-select',
            'id': 'input-allergy'
        })
    )
    
    WHEEZING = forms.ChoiceField(
        choices=YES_NO_CHOICES,
        label='Wheezing',
        widget=forms.Select(attrs={
            'class': 'form-select',
            'id': 'input-wheezing'
        })
    )
    
    ALCOHOL_CONSUMING = forms.ChoiceField(
        choices=YES_NO_CHOICES,
        label='Alcohol Consuming',
        widget=forms.Select(attrs={
            'class': 'form-select',
            'id': 'input-alcohol'
        })
    )
    
    COUGHING = forms.ChoiceField(
        choices=YES_NO_CHOICES,
        label='Coughing',
        widget=forms.Select(attrs={
            'class': 'form-select',
            'id': 'input-coughing'
        })
    )
    
    SHORTNESS_OF_BREATH = forms.ChoiceField(
        choices=YES_NO_CHOICES,
        label='Shortness of Breath',
        widget=forms.Select(attrs={
            'class': 'form-select',
            'id': 'input-shortness-breath'
        })
    )
    
    SWALLOWING_DIFFICULTY = forms.ChoiceField(
        choices=YES_NO_CHOICES,
        label='Swallowing Difficulty',
        widget=forms.Select(attrs={
            'class': 'form-select',
            'id': 'input-swallowing'
        })
    )
    
    CHEST_PAIN = forms.ChoiceField(
        choices=YES_NO_CHOICES,
        label='Chest Pain',
        widget=forms.Select(attrs={
            'class': 'form-select',
            'id': 'input-chest-pain'
        })
    )
