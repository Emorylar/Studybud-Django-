from django.forms import ModelForm
from .models import Room

class RoomForm(ModelForm):
    class Meta:
        model=Room           #to specify the model /class to be used
        fields='__all__'
        exclude=['host','participants']