from .models import Report
from django.forms import ModelForm, formset_factory, inlineformset_factory, modelformset_factory
from django import forms

class ReportCreateForm(ModelForm):
    
    class Meta:
       model = Report
       fields =['user', 'modulo','assunto', 'descricao', 'anexo']
    
