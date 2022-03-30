from django import forms 
from .models import Item
from django.forms import ModelForm

class CreateItemForm(ModelForm):
    #this provides the setup of the form that the user can fill out
    class Meta:
        model = Item
        fields = [
            'title', 
            'description', 
            'amount', 
            'image_url', 
            ]


    def __init__(self, *args, **kwargs):
        #called this function because it calls the form that was just created above
       super(CreateItemForm, self).__init__(*args, **kwargs)
       #referenced stackoverflow.com for visible_fields in writing form for ModelForm
       for visible in self.visible_fields():
           visible.field.widget.attrs["class"] = "row form-control"