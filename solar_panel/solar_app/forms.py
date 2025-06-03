from django import forms
from .models import Category



class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['pimg', 'price', 'wattage', 'voltage', 'warrenty', 'title', 'description1', 'solar_panel', 'solar_heater', 'inverter', 'solar_cooker', 'luminous', 'loom', 'hi_mo', 'discount_10', 'discount_20', 'discount_30', 'first_name', 'last_name', 'email', 'phone', 'description']
      
