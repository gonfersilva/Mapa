from .models import Perfil, Largura, Bobinagem, Bobine, Palete, Emenda
from django.forms import ModelForm, formset_factory, inlineformset_factory, modelformset_factory
from django import forms

class PerfilCreateForm(ModelForm):
    
    class Meta:
       model = Perfil
       fields =['nome', 'produto', 'num_bobines', 'largura_bobinagem', 'core', 'retrabalho']
    #    fields =['nome', 'num_bobines', 'retrabalho', 'largura_bobinagem', 'core', 'gramagem', 'espessura', 'densidade_mp', 'velocidade', 'producao']


class LarguraForm(ModelForm):

    class Meta:
       model = Largura
       fields =[ 'largura' ]


class BobinagemCreateForm(ModelForm):
    
    class Meta:
       model = Bobinagem
       fields =['data', 'num_bobinagem', 'perfil', 'comp', 'comp_par', 'diam', 'inico', 'fim', 'estado', 'obs']

    def __init__(self, *args, **kwargs):
        super(BobinagemCreateForm, self).__init__(*args, **kwargs)
        self.fields['perfil'].queryset = Perfil.objects.filter(retrabalho=False)


class RetrabalhoCreateForm(ModelForm):
    
    class Meta:
       model = Bobinagem
       fields =['data', 'num_bobinagem', 'perfil', 'num_emendas', 'comp', 'diam', 'inico', 'fim', 'estado', 'obs']

    def __init__(self, *args, **kwargs):
        super(RetrabalhoCreateForm, self).__init__(*args, **kwargs)
        self.fields['perfil'].queryset = Perfil.objects.filter(retrabalho=True)


       
class PaleteCreateForm(ModelForm):
    
    class Meta:
       model = Palete
       fields =['estado', 'num_bobines', 'largura_bobines', 'diametro', 'core_bobines']

    



class BobineStatus(ModelForm):
   
    class Meta:
        model = Bobine
        fields = [ 'largura', 'estado', 'con', 'descen', 'presa', 'estrela', 'furos', 'esp', 'troca_nw', 'outros', 'obs'] 



class EmendasCreateForm(ModelForm):
    
    class Meta:
       model = Emenda
       fields = [ 'bobine', 'metros', 'num_emenda'] 

    def __init__(self, *args, **kwargs):
        super(EmendasCreateForm, self).__init__(*args, **kwargs)
        self.fields['bobine'].queryset = Bobine.objects.filter(estado='DM')

class Picagem(forms.Form):
    nome = forms.CharField(max_length=50)
    
