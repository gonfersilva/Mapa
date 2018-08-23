from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy, resolve
from django.forms import formset_factory
from django import forms
from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, redirect, reverse, HttpResponse
from django.views.generic import CreateView
from django.views.generic import ListView, DetailView, CreateView, TemplateView, View, FormView, UpdateView
from .forms import PerfilCreateForm, LarguraForm, BobinagemCreateForm, BobineStatus, PaleteCreateForm, EmendasCreateForm, RetrabalhoCreateForm
from .models import Largura, Perfil, Bobinagem, Bobine, Palete, Emenda
from django.utils import timezone
from django.contrib.auth.decorators import login_required

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
    fields = [ 'estado', 'con', 'descen', 'presa', 'estrela', 'furos', 'esp', 'troca_nw', 'outros', 'obs']
    template_name = 'producao/bobine_update.html'
    
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

class BobinagemRetrabalhoListView(LoginRequiredMixin, ListView):
    
    queryset = Bobinagem.objects.all()
    template_name = 'retrabalho/retrabalho_home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context

class RetrabalhoCreateView(LoginRequiredMixin, CreateView):
    form_class = RetrabalhoCreateForm
    template_name = 'retrabalho/retrabalho_create.html'
    success_url = "/producao/retrabalho/{id}"
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

  

    
@login_required
def bobinagem_emendas(request, pk):
    template_name = 'retrabalho/retrabalho_emendas.html'
    bobinagem = Bobinagem.objects.get(pk=pk)
    emenda = Emenda.objects.filter(bobinagem=pk)

        
    context = {
        "bobinagem": bobinagem,
        "emenda": emenda
    }

    return render(request, template_name, context) 

@login_required
def create_emenda(request, pk):
    template_name = 'retrabalho/emenda_create.html'
    form = EmendasCreateForm()
    bobinagem = Bobinagem.objects.get(pk=pk)
    
    if request.method == "POST":
        form = EmendasCreateForm(request.POST)
        
        if form.is_valid():
            Emenda.objects.create(**form.cleaned_data, bobinagem=bobinagem)
            return  redirect('producao:retrabalho_emendas', pk=bobinagem.pk)
        else:
            print(form.error)

    
    context = {
        'form': form,
        'bobinagem': bobinagem,
    }
    return render(request, template_name, context)


@login_required
def picagem(request, pk):
    palete = Palete.objects.get(pk=pk)
    bob = request.POST.get('q')
    bob_filter = Bobine.objects.filter(nome=bob)
    if bob_filter.exists():
        bobine = Bobine.objects.get(nome=bob)
        if bobine.palete:
            if bobine.palete == palete:
                erro = 4
                return redirect('producao:addbobinepaleteerro', pk=palete.pk, e=erro)
            else:
                erro = 5
                return redirect('producao:addbobinepaleteerro', pk=palete.pk, e=erro)
        else:    
            if palete.num_bobines_act == palete.num_bobines:
                erro = 3
                return redirect('producao:addbobinepaleteerro', pk=palete.pk, e=erro) 
            else:
                if bobine.estado == palete.estado or bobine.estado == 'LAB' and bobine.bobinagem.diam == palete.diametro and bobine.bobinagem.perfil.core == palete.core_bobines and bobine.largura.largura == palete.largura_bobines:
                    Bobine.add_bobine(palete.pk, bobine.pk)
                    return redirect('producao:addbobinepalete', pk=palete.pk)
                else:
                    erro = 1
                    return redirect('producao:addbobinepaleteerro', pk=palete.pk, e=erro)
    else:   
        erro = 2
        return redirect('producao:addbobinepaleteerro', pk=palete.pk, e=erro)

    
    
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
        obj.delete()
        return redirect('producao:bobinagens')
            
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
            
    return redirect('producao:bobinagens')