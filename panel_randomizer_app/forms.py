from django import forms
from panel_randomizer_app.models import Participant 

class ParicipantForm(forms.ModelForm):  
    class Meta:  
        model = Participant  
        fields = "__all__" # fields = ('title', 'text',)
