from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy, resolve
from django.forms import formset_factory
from django import forms
from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, redirect, reverse, HttpResponse
from django.views.generic import CreateView
from django.views.generic import ListView, DetailView, CreateView, TemplateView, View, FormView, UpdateView
from .forms import PerfilCreateForm, LarguraForm, BobinagemCreateForm, BobineStatus, PaleteCreateForm, RetrabalhoCreateForm, EmendasCreateForm, ClienteCreateForm
from .models import Largura, Perfil, Bobinagem, Bobine, Palete, Emenda, Cliente
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, Http404, HttpResponse
from django.db.models.signals import pre_save, post_save
from django.contrib import messages
from time import gmtime, strftime
import datetime
from .funcs import *


@login_required
def perfil_create(request):
    template_name = 'perfil/perfil_create.html'
    context = {}
 
    return render(request, template_name, context)



class CreatePerfil(LoginRequiredMixin, CreateView):
    template_name = 'perfil/perfil_create.html'
    form_class = PerfilCreateForm
    success_url = '/producao/perfil/{id}/'
     
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class BobinagemCreateView(LoginRequiredMixin, CreateView):
    form_class = BobinagemCreateForm
    template_name = 'producao/bobinagem_create.html'
    success_url = "/producao/bobinagem/"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    
class PerfilListView(LoginRequiredMixin, ListView):
    model = Perfil
    template_name = 'perfil/perfil_home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context
    

@login_required
def perfil_detail(request, pk):
    perfil = Perfil.objects.get(pk=pk)
    largura = Largura.objects.filter(perfil=pk)
    template_name = 'perfil/perfil_detail.html'
    context = {
        'perfil': perfil,
        'largura': largura,
    }
    return render(request, template_name, context)


   
class BobinagemListView(LoginRequiredMixin, ListView):
    model = Bobinagem
    template_name = 'producao/bobinagem_home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context

def bobinagem_list(request):
    bobinagem = Bobinagem.objects.all()
    bobine = Bobine.objects.all()

    template_name = 'producao/bobinagem_home.html'

    context = {
        "bobinagem": bobinagem,
        "bobine": bobine,
    }
    return render (request, template_name, context)

@login_required
def bobinagem_status(request, pk):
    template_name = 'producao/bobine_list.html'
    bobinagem = Bobinagem.objects.get(pk=pk)
    bobine = Bobine.objects.filter(bobinagem=pk)
    emenda = Emenda.objects.filter(bobinagem=pk)

    context = {
        "bobinagem": bobinagem,
        "bobine": bobine,
        "emenda":emenda
    }

    return render(request, template_name, context) 

class LarguraUpdate(LoginRequiredMixin, UpdateView):
    model = Largura
    fields = ['largura']
    template_name = 'perfil/largura_update.html'

class BobineUpdate(LoginRequiredMixin, UpdateView):
    model = Bobine
    fields = [ 'estado', 'con', 'descen', 'presa', 'diam_insuf', 'furos', 'esp', 'troca_nw', 'outros', 'buraco', 'obs']
    template_name = 'producao/bobine_update.html'
    
    def get_success_url(self):
         bobinagem = self.object.bobinagem
         return reverse('producao:bobinestatus', kwargs={'pk': bobinagem.id})

    
     

class BobinagemUpdate(LoginRequiredMixin, UpdateView):
    model = Bobinagem
    fields = ['tiponwsup', 'tiponwinf', 'lotenwsup', 'lotenwinf', 'nwsup', 'nwinf', 'comp', 'comp_par', 'diam', 'inico', 'fim']
    template_name = 'producao/bobinagem_update.html'
    
    
class PaleteListView(LoginRequiredMixin, ListView):
    model = Palete
    template_name = 'palete/palete_home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context


class PaleteCreateView(LoginRequiredMixin, CreateView):
    form_class = PaleteCreateForm
    template_name = "palete/palete_create.html"
    success_url = "/producao/palete/{id}"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)



@login_required
def add_bobine_palete(request, pk):
    template_name='palete/add_bobine_palete.html'
    palete = Palete.objects.get(pk=pk)
    bobinagem = Bobinagem.objects.filter(diam=palete.diametro)
    bobine = Bobine.objects.all().order_by('posicao_palete')
    
    
    context = {"palete": palete, 
               "bobine": bobine,
               "bobinagem": bobinagem,
                }
    return render(request, template_name, context)


@login_required
def palete_change(request, operation, pk_bobine, pk_palete):
    
    palete = Palete.objects.get(pk=pk_palete)
    bobine = Bobine.objects.get(pk=pk_bobine)
    
    if operation == 'add':
        Bobine.add_bobine(palete.pk, bobine.pk)
    elif operation == 'remove':
        Bobine.remove_bobine(palete.pk, bobine.pk)
                 
    
    return redirect('producao:addbobinepalete', pk=palete.pk)

# class BobinagemRetrabalhoListView(LoginRequiredMixin, ListView):
    
#     queryset = Bobinagem.objects.all()
#     template_name = 'retrabalho/retrabalho_home.html'
    
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['now'] = timezone.now()
#         return context

class RetrabalhoCreateView(LoginRequiredMixin, CreateView):
     form_class = RetrabalhoCreateForm
     template_name = 'retrabalho/retrabalho_create.html'
     success_url = "/producao/retrabalho/filter/{id}"
    
     def form_valid(self, form):
         form.instance.user = self.request.user
         return super().form_valid(form)

class ClienteCreateView(LoginRequiredMixin, CreateView):
     form_class = ClienteCreateForm
     template_name = 'cliente/cliente_create.html'
     success_url = "/producao/clientes/"
    
     

    
# @login_required
# def bobinagem_emendas(request, pk):
#     template_name = 'retrabalho/retrabalho_emendas.html'
#     bobinagem = Bobinagem.objects.get(pk=pk)
#     emenda = Emenda.objects.filter(bobinagem=pk)

        
#     context = {
#         "bobinagem": bobinagem,
#         "emenda": emenda
#     }

#     return render(request, template_name, context) 

# @login_required
# def create_emenda(request, pk):
#     template_name = 'retrabalho/emenda_create.html'
#     form = EmendasCreateForm()
#     bobinagem = Bobinagem.objects.get(pk=pk)
    
#     if request.method == "POST":
#         form = EmendasCreateForm(request.POST)
        
#         if form.is_valid():
#             Emenda.objects.create(**form.cleaned_data, bobinagem=bobinagem)
#             return  redirect('producao:retrabalho_emendas', pk=bobinagem.pk)
#         else:
#             print(form.error)

    
#     context = {
#         'form': form,
#         'bobinagem': bobinagem,
#     }
#     return render(request, template_name, context)


@login_required
def picagem(request, pk):
    palete = Palete.objects.get(pk=pk)
    bob = request.POST.get('q')
    try:
        bobine = Bobine.objects.get(nome=bob)
    except:
        messages.error(request, 'A bobine selecionada não existe.')
        return redirect('producao:addbobinepalete', pk=palete.pk)
    if bobine:
        if bobine.palete:
            if bobine.palete == palete:
                messages.error(request, 'A bobine já faz parte desta palete.')
                # erro = 4
                # return redirect('producao:addbobinepaleteerro', pk=palete.pk, e=erro)
                return redirect('producao:addbobinepalete', pk=palete.pk)
            else:
                messages.error(request, 'A bobine já faz parte de outra palate.')
                # erro = 5
                # return redirect('producao:addbobinepaleteerro', pk=palete.pk, e=erro)
                return redirect('producao:addbobinepalete', pk=palete.pk)
        else:
            if bobine.estado == 'G' or bobine.estado == 'LAB':
                if palete.num_bobines_act == palete.num_bobines:
                    messages.error(request, 'A palete já se encontra completa.')
                    #  erro = 3
                    #  return redirect('producao:addbobinepaleteerro', pk=palete.pk, e=erro)
                    return redirect('producao:addbobinepalete', pk=palete.pk)
                else:
                     if (bobine.bobinagem.diam == palete.diametro or palete.cliente.limsup >= bobine.bobinagem.diam >= palete.cliente.liminf) and bobine.bobinagem.perfil.core == palete.core_bobines and bobine.largura.largura == palete.largura_bobines:
                         Bobine.add_bobine(palete.pk, bobine.pk)
                         return redirect('producao:addbobinepalete', pk=palete.pk)
                     else:
                         messages.error(request, 'A bobine selecionada está fora de especificações.')
                        #  erro = 1
                        #  return redirect('producao:addbobinepaleteerro', pk=palete.pk, e=erro)
                         return redirect('producao:addbobinepalete', pk=palete.pk)
            elif bobine.estado == 'DM' and bobine.largura.largura == palete.largura_bobines and palete.estado == 'DM':
                  Bobine.add_bobine(palete.pk, bobine.pk)
                  return redirect('producao:addbobinepalete', pk=palete.pk) 
            else:
                messages.error(request, 'A bobine selecionada está fora de especificações.')
                return redirect('producao:addbobinepalete', pk=palete.pk)
            
    else:
        messages.error(request, 'A bobine selecionada não existe.')
        #  erro = 2
        #  return redirect('producao:addbobinepaleteerro', pk=palete.pk, e=erro)  
        return redirect('producao:addbobinepalete', pk=palete.pk)        
            

    
   
@login_required
def add_bobine_palete_erro(request, pk, e):
    template_name='palete/add_bobine_erro.html'
    palete = Palete.objects.get(pk=pk)
    
    erro = e
    
    context = {"palete":palete, "erro":erro}
    
    return render(request, template_name, context)

    
@login_required
def perfil_delete(request, pk):
    obj = get_object_or_404(Perfil, pk=pk)
    bobinagem = Bobinagem.objects.filter(perfil=pk)
    if request.method == "POST":
        obj.delete()
        return redirect('producao:perfil')
            
    context = {
        "object": obj,
    }
    return render(request, "perfil/perfil_delete.html", context)

@login_required
def bobinagem_delete(request, pk):
    obj = get_object_or_404(Bobinagem, pk=pk)
    bobine = Bobine.objects.filter(bobinagem=obj)
    
    
    if request.method == "POST":
        try:
            emenda = Emenda.objects.filter(bobinagem=obj)
        except:
            obj.delete()
            if obj.perfil.retrabalho == False:
                return redirect('producao:bobinagens')
            else:
                return redirect('producao:retrabalho_home')

        if emenda:
            for e in emenda:
                e.bobine.comp_actual += e.metros
                e.delete()
            obj.delete()
            if obj.perfil.retrabalho == False:
                return redirect('producao:bobinagens')
            else:
                return redirect('producao:retrabalho_home')
            
    context = {
        "object": obj,
        "bobine": bobine
    }
    return render(request, "producao/bobinagem_delete.html", context)


@login_required
def palete_delete(request, pk):
    obj = get_object_or_404(Palete, pk=pk)
    bobine = Bobine.objects.filter(palete=obj)
    if request.method == "POST":
        obj.delete()
        return redirect('producao:paletes')
            
    context = {
        "object": obj,
        "bobine": bobine
    }
    return render(request, "palete/palete_delete.html", context)
    
@login_required
def status_bobinagem(request, operation, pk):
    bobinagem = Bobinagem.objects.get(pk=pk)
    if operation == 'ap':
        bobinagem.estado = 'G'
        bobinagem.save()
        num = 1
        for i in range(bobinagem.perfil.num_bobines):
            largura = Largura.objects.get(perfil=bobinagem.perfil, num_bobine=num)
            bobine = Bobine.objects.get(bobinagem=bobinagem, largura=largura)
            if bobine.estado == 'LAB':
                bobine.estado = 'G'
                bobine.save()
            num += 1
        areas(pk)
    elif operation == 'rej':
        bobinagem.estado = 'R'
        bobinagem.save()
        num = 1
        for i in range(bobinagem.perfil.num_bobines):
            largura = Largura.objects.get(perfil=bobinagem.perfil, num_bobine=num)
            bobine = Bobine.objects.get(bobinagem=bobinagem, largura=largura)
            if bobine.estado == 'LAB':
                bobine.estado = 'R'
                bobine.save()
            num += 1
        areas(pk)
    elif operation == 'dm':
        bobinagem.estado = 'DM'
        bobinagem.save()
        num = 1
        for i in range(bobinagem.perfil.num_bobines):
            largura = Largura.objects.get(perfil=bobinagem.perfil, num_bobine=num)
            bobine = Bobine.objects.get(bobinagem=bobinagem, largura=largura)
            if bobine.estado == 'LAB':
                bobine.estado = 'DM'
                bobine.save()
            num += 1
        areas(pk)

       
            
    return redirect('producao:bobinagens')


@login_required
def palete_retrabalho(request):
    palete = Palete.objects.filter(estado='DM')
    template_name = 'palete/palete_retrabalho.html'
    context = {
        "palete":palete
    }
    return render(request, template_name, context)

@login_required
def palete_create_retrabalho(request):
    palete = Palete.objects.create(estado="DM", num_bobines=0, largura_bobines=0, diametro=0, core_bobines='3', user=request.user)   
    palete.save()
    return redirect('producao:addbobinepalete', pk=palete.pk)

@login_required
def retrabalho_home(request):
    palete = Palete.objects.filter(estado='DM')
    bobine = Bobine.objects.all()
    bobinagem = Bobinagem.objects.all()
    template_name = 'retrabalho/retrabalho_home.html'

    context = {
        "palete": palete,
        "bobine": bobine,
        "bobinagem": bobinagem,
    }
    return render(request, template_name, context)

@login_required
def retrabalho_filter(request, pk):
    # palete = Palete.objects.filter(estado="DM")
    # bobine = Bobine.objects.all()
    bobinagem = Bobinagem.objects.get(pk=pk)
    # q_largura = request.GET.get("l")
    # if q_largura:
    #     palete = palete.filter(largura_bobines__gte=q_largura)
    # bobinagem = Bobinagem.objects.get(pk=pk)
    form = EmendasCreateForm
    
    if request.method == "POST":
        form = EmendasCreateForm(request.POST)
               
        if form.is_valid():
            bobine_ori = int(form['bobine'].value())
            comp_bobine_ori = int(form['metros'].value())
            bobine = Bobine.objects.get(pk=bobine_ori)
            if comp_bobine_ori > bobine.comp_actual:
                messages.error(request, 'A bobine selecionada não tem comprimento suficiente para efectuar esta operação.')
                # redirect('producao:retrabalho_filter', pk=bobinagem.pk)
            else:
                emenda = Emenda.objects.create(**form.cleaned_data, bobinagem=bobinagem)
                bobine.comp_actual = bobine.comp_actual - emenda.metros 
                bobine.save()
                emenda.num_emenda = bobinagem.num_emendas + 1
                emenda.save()
                emenda_num = emenda.num_emenda
                print(emenda_num)
                if emenda_num == 0:
                    emenda.emenda = 0
                    emenda.save()
                elif emenda_num > 0:
                    if emenda_num == 1:
                        emenda.emenda = emenda.metros
                        emenda.save()
                    elif emenda_num == 2:
                        emenda_ul_bob = Emenda.objects.get(bobinagem=bobinagem, num_emenda=1)
                        emenda.emenda = emenda_ul_bob.emenda + emenda.metros 
                        emenda.save()
                    elif emenda_num == 3:
                        emenda_ul_bob = Emenda.objects.get(bobinagem=bobinagem, num_emenda=2)
                        emenda.emenda = emenda_ul_bob.emenda + emenda.metros 
                        emenda.save()
                bobinagem.num_emendas += 1 
                bobinagem.save()
                data = bobinagem.data
                data = data.strftime('%Y%m%d')
                map(int, data)
                if bobinagem.perfil.retrabalho == True and bobinagem.num_emendas > 1:
                    if bobinagem.num_bobinagem < 10:
                        # instance.nome = '3%s-0%s' % (data, instance.num_bobinagem)
                        bobinagem.nome = '3%s-0%s' % (data[1:], bobinagem.num_bobinagem)
                        bobinagem_pk = bobinagem.pk
                        bobine_nome(bobinagem_pk)
                    else:
                        bobinagem.nome = '3%s-0%s' % (data[1:], bobinagem.num_bobinagem)
                elif bobinagem.perfil.retrabalho == True and bobinagem.num_emendas == 0:
                    if bobinagem.num_bobinagem < 10:
                        bobinagem.nome = '4%s-0%s' % (data[1:], bobinagem.num_bobinagem)
                    else:
                        bobinagem.nome = '4%s-%s' % (data[1:], bobinagem.num_bobinagem)
                


                comp_parcial = int(form['metros'].value())
                bobinagem.comp = bobinagem.comp + comp_parcial
                bobinagem.save()

        return redirect('producao:retrabalho_filter', pk=bobinagem.pk)
         

    palete = Palete.objects.filter(estado="DM")
    bobine = Bobine.objects.all()
    emenda = Emenda.objects.filter(bobinagem=pk)

    q_largura = request.GET.get("l")
    

    if q_largura:
        palete = palete.filter(largura_bobines__gte=q_largura)
        
    template_name = 'retrabalho/retrabalho_inicio.html'
    context = {
        
        "palete": palete,
        "bobine": bobine,
        "form": form,
        "bobinagem": bobinagem,
        "emenda": emenda
        
    }

    return render(request, template_name, context)



# Funções de apoio

def bobine_nome(pk):
    bobinagem = Bobinagem.objects.get(pk=pk)
    bobine = Bobine.objects.filter(bobinagem=bobinagem)
    for b in bobine:
        data = bobinagem.data
        data = data.strftime('%Y%m%d')
        map(int, data)
        if bobinagem.num_bobinagem < 10 and b.largura.num_bobine < 10:
            b.nome = '3%s-0%s-0%s' % (data[1:], bobinagem.num_bobinagem, b.largura.num_bobine)
            b.save()
            

def comprimento_bobine_original(pk):
    pass

def finalizar_retrabalho(request, pk):
    bobinagem = get_object_or_404(Bobinagem, pk=pk)
    form = BobinagemCreateForm(request.POST or None, instance=bobinagem)
    if form.is_valid():
        bobinagem = form.save(commit=False)
        bobinagem.save()
        return redirect('producao:retrabalho_home')

    template_name = 'retrabalho/retrabalho_finalizar.html'
    context = {
        "bobinagem": bobinagem,
        "form": form
    }

    return render(request, template_name, context)

class BobinagemRetrabalhoFinalizar(LoginRequiredMixin, UpdateView):
    model = Bobinagem
    fields = ['inico', 'fim', 'diam']
    template_name = 'retrabalho/retrabalho_finalizar.html'


@login_required
def emenda_delete(request, pk):
    emenda = get_object_or_404(Emenda, pk=pk)
    bobine = get_object_or_404(Bobine, pk=emenda.bobine.pk)
    bobinagem = get_object_or_404(Bobinagem, pk=emenda.bobinagem.pk)
    bob = Bobine.objects.filter(bobinagem=bobinagem)
    if request.method == "POST":
        bobinagem.num_emendas -= 1
        bobinagem.comp -= emenda.metros
        bobine.comp_actual += emenda.metros 
        data = bobinagem.data
        data = data.strftime('%Y%m%d')
        map(int, data)
        if bobinagem.perfil.retrabalho == True and bobinagem.num_emendas > 1:
            if bobinagem.num_bobinagem < 10:
                # instance.nome = '3%s-0%s' % (data, instance.num_bobinagem)
                bobinagem.nome = '3%s-0%s' % (data[1:], bobinagem.num_bobinagem)
                for b in bob:
                    if b.largura.num_bobine < 10:
                        b.nome = '%s-0%s' % (bobinagem.nome, b.largura.num_bobine)
                        b.save()
                    else:
                        b.nome = '%s-%s' % (bobinagem.nome, b.largura.num_bobine)
                        b.save()
            else:
                bobinagem.nome = '3%s-0%s' % (data[1:], bobinagem.num_bobinagem)
                for b in bob:
                    if b.largura.num_bobine < 10:
                        b.nome = '%s-0%s' % (bobinagem.nome, b.largura.num_bobine)
                        b.save()
                    else:
                        b.nome = '%s-%s' % (bobinagem.nome, b.largura.num_bobine)
                        b.save()
                
        elif bobinagem.perfil.retrabalho == True and (bobinagem.num_emendas == 0 or bobinagem.num_emendas == 1):
            if bobinagem.num_bobinagem < 10:
                bobinagem.nome = '4%s-0%s' % (data[1:], bobinagem.num_bobinagem)
                for b in bob:
                    if b.largura.num_bobine < 10:
                        b.nome = '%s-0%s' % (bobinagem.nome, b.largura.num_bobine)
                        b.save()
                    else:
                        b.nome = '%s-%s' % (bobinagem.nome, b.largura.num_bobine)
                        b.save()
                
            else:
                bobinagem.nome = '4%s-%s' % (data[1:], bobinagem.num_bobinagem)
                for b in bob:
                    if b.largura.num_bobine < 10:
                        b.nome = '%s-0%s' % (bobinagem.nome, b.largura.num_bobine)
                        b.save()
                    else:
                        b.nome = '%s-%s' % (bobinagem.nome, b.largura.num_bobine)
                        b.save()
                
        bobinagem.save()
        # bobinagem_pk = bobinagem.pk
        # bobine_nome(bobinagem_pk)
        bobine.save()
        emenda.delete()
        return redirect('producao:retrabalho_filter', pk=emenda.bobinagem.pk)

    template_name =  'retrabalho/emenda_delete.html'    
    context = {
           "emenda": emenda,
           "bobinagem": bobinagem,
           "bobine":bobine
    }
    return render(request, template_name, context)

def cliente_home(request):
    cliente = Cliente.objects.all()

    template_name = 'cliente/cliente_home.html'
    context = {
        "cliente":cliente
    }
    return render(request, template_name, context)



def producao_home(request):
    template_name = 'producao/producao_home.html'
    context = {}

    return render(request, template_name, context)

def planeamento_home(request):
    template_name = 'producao/planeamento_home.html'
    context = {}

    return render(request, template_name, context)


def bobine_details(request, pk):
     bobine = get_object_or_404(Bobine, pk=pk)
     
     emenda = Emenda.objects.filter(bobinagem=bobine.bobinagem)

     template_name = 'producao/bobine_details.html'
     context = {
         "bobine": bobine,
         "emenda": emenda,
     }
     return render(request, template_name, context)


def relatorio_diario(request):
    inicio_data = request.GET.get("id")
    fim_data = request.GET.get("fd")
    inicio_hora = request.GET.get("fd")
    fim_hora = request.GET.get("fd")
    
    bobinagem = []

    area_g = 0
    area_r = 0
    area_dm = 0
    area_ind = 0
    area_ba = 0

   

    
    
   
    if inicio_data and fim_data:
         bobinagem = Bobinagem.objects.filter(data__range=(inicio_data, fim_data))
         for bob in bobinagem:
             area_g += bob.area_g
             area_r += bob.area_r
             area_dm += bob.area_dm
             area_ind += bob.area_ind
             area_ba += bob.area_ba

    
        

   

    template_name = 'producao/relatorio_diario_linha.html'
    context = {     
        "bobinagem": bobinagem,
        "area_g":area_g,
        "area_dm":area_dm,
        "area_r":area_r,
        "area_ba":area_ba,
        "area_ind":area_ind,
        

        
    }

    return render(request, template_name, context)