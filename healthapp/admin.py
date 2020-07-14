from django import forms
from django.contrib import admin

from .models import *


class DiseaseAdminForm(forms.ModelForm):
    class Meta:
        model = Disease
        widgets = {
            'department': forms.CheckboxSelectMultiple,
            'treatments': forms.Textarea(attrs={'cols': 80, 'rows': 20}),
            'remedies': forms.Textarea(attrs={'cols': 80, 'rows': 20}),
        }
        fields = '__all__'


class DiseaseAdmin(admin.ModelAdmin):
    form = DiseaseAdminForm


admin.site.register(User)
admin.site.register(Patient)
admin.site.register(Doctor)
admin.site.register(Department)
admin.site.register(Appointment)
admin.site.register(Disease, DiseaseAdmin)
