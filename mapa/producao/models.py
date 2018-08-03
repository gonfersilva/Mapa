from django.db import models
import datetime, time
from django.conf import settings
from django.shortcuts import render, get_object_or_404, render_to_response, redirect
from django.db import models
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from datetime import timedelta
from time import gmtime, strftime
from django.db.models import Max
from django.contrib.auth.models import User

class Perfil(models.Model):
    CORE = (('3', '3'),('6', '6'))
    user = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name="Username")
    timestamp = models.DateTimeField(auto_now_add=True)
    nome = models.CharField(verbose_name="Perfil", max_length=200, unique=True, null=True, blank=True )
    retrabalho = models.BooleanField(default=False, verbose_name="Retrabalho")
    num_bobines = models.PositiveIntegerField(verbose_name="Número de bobines")
    largura_bobinagem = models.DecimalField(verbose_name="Largura da bobinagem", max_digits=10, decimal_places=2)
    core = models.CharField(verbose_name="Core", max_length=1, choices=CORE)
    gramagem = models.DecimalField(verbose_name="Gramagem", max_digits=10, decimal_places=2, null=True, blank=True)
    espessura = models.DecimalField(verbose_name="Espessura", max_digits=10, decimal_places=2, null=True, blank=True)
    densidade_mp = models.DecimalField(verbose_name="Densidade da matéria prima", max_digits=10, decimal_places=2, null=True, blank=True)
    velocidade = models.DecimalField(verbose_name="Velocidade", max_digits=10, decimal_places=2, null=True, blank=True)
    producao = models.DecimalField(verbose_name="Produção", max_digits=10, decimal_places=2, null=True, blank=True)

    class Meta:
        verbose_name_plural = "Perfis"
        ordering = ['-timestamp']

    def __str__(self):
        return '%s' % (self.nome)
    
    def get_absolute_url(self):
        return f"{self.id}"

class Largura(models.Model):
    perfil = models.ForeignKey(Perfil, on_delete=models.CASCADE, verbose_name="Largura")
    num_bobine = models.PositiveIntegerField(verbose_name="Bobine nº")
    largura = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    class Meta:
        verbose_name_plural = "Larguras"
        ordering = ['perfil']

    def __str__(self):
        return '%s - Bobine nº: %s, %s mm' % (self.perfil, self.num_bobine, self.largura)

    def get_absolute_url(self):
        return f"/producao/perfil/{self.perfil.id}"

def perfil_larguras(sender, instance, **kwargs):
    for i in range(instance.num_bobines):
        lar = Largura.objects.create(perfil=instance, num_bobine=i+1)
        lar.save()

class Nonwoven(models.Model):

    pass

class Lote(models.Model):
    pass

class Produto(models.Model):
    pass

class Consumo(models.Model):
    pass


class Bobinagem(models.Model):
    STATUSP = (('G', 'G'), ('DM', 'DM12'), ('R', 'R'), ('BA', 'BA'), ('LAB', 'LAB'))
    user = models.ForeignKey(User, on_delete=models.PROTECT,verbose_name="Username")
    perfil = models.ForeignKey(Perfil, on_delete=models.PROTECT,verbose_name="Perfil")
    num_emendas = models.IntegerField(verbose_name="Número de emendas", null=True, blank=True, default=0)
    timestamp = models.DateTimeField(auto_now_add=True)
    nome = models.CharField(verbose_name="Bobinagem", max_length=200, unique=True)
    data = models.DateField(auto_now_add=False, auto_now=False, default=datetime.date.today,verbose_name="Data")
    num_bobinagem = models.PositiveIntegerField(verbose_name="Bobinagem nº")
    comp = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Comprimento")
    diam = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Diametro")
    area = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Área")
    inico = models.TimeField(auto_now_add=False, auto_now=False, verbose_name="Início")
    fim = models.TimeField(auto_now_add=False, auto_now=False, verbose_name="Fim")
    duracao = models.CharField(max_length=200, null=True, blank=True, verbose_name="Duração")
    estado = models.CharField(max_length=3, choices=STATUSP, default='G', verbose_name="Estado")
    obs = models.TextField(max_length=500, null=True, blank=True, verbose_name="Observações", default="") 
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome
       

    @property
    def title(self):
        return self.nome
    
    class Meta:
        verbose_name_plural = "Bobinagens"
        ordering = ['-timestamp']

    def get_absolute_url(self):
        return f"/producao/bobinagem/{self.id}"


    


class Palete(models.Model):
    CORE = (('3', '3'),('6', '6'))
    STATUSP = (('G', 'G'), ('DM', 'T'), ('R', 'R'))
    user            = models.ForeignKey(User, on_delete=models.PROTECT,verbose_name="Username")
    timestamp       = models.DateTimeField(auto_now_add=True)
    data_pal        = models.DateField(auto_now=False, auto_now_add=False, default=datetime.date.today)
    nome            = models.CharField(max_length=200, unique=True, null=True, blank=True, verbose_name="Palete")
    num             = models.IntegerField(unique=True, null=True, blank=True, verbose_name="Palete nº")
    estado          = models.CharField(max_length=2, choices=STATUSP, default='G', verbose_name="Estado")
    area            = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Área palete")
    comp_total      = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Comprimento palete")
    lote            = models.CharField(max_length=200, unique=True, null=True, blank=True, verbose_name="Nº Lote")
    num_bobines     = models.IntegerField(verbose_name="Bobines total")
    num_bobines_act = models.IntegerField(default=0) 
    largura_bobines = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Largura das bobines")
    diametro        = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="Diâmetro das bobines")
    core_bobines    = models.CharField(max_length=1, choices=CORE, verbose_name="Core das bobines")
    peso_bruto      = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Peso bruto")
    peso_palete     = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Peso palete")
    peso_liquido    = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Peso liqudo")
    
    def __str__(self):
        return self.nome

    class Meta:
        verbose_name_plural = "Paletes"
        ordering = ['-timestamp']  

    

class Bobine(models.Model):
    STATUSP = (('G', 'G'), ('DM', 'DM12'), ('R', 'R'), ('BA', 'BA'),('LAB', 'LAB'))
    bobinagem = models.ForeignKey(Bobinagem, on_delete=models.CASCADE, verbose_name="Bobinagem")
    largura =  models.ForeignKey(Largura, on_delete=models.PROTECT,  null=True, blank=True, verbose_name="Largura")
    comp_actual = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Comprimento actual", default="")
    nome = models.CharField(verbose_name="Bobine", max_length=200, null=True, blank=True, default="")
    palete = models.ForeignKey(Palete, on_delete=models.SET_NULL, null=True, blank=True)   
    posicao_palete = models.PositiveIntegerField(verbose_name="Posição", default=0)
    estado = models.CharField(max_length=3, choices=STATUSP, default='G', verbose_name="Estado")
    area = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Área bobine")
    con = models.BooleanField(default=False,verbose_name="Cónica")
    descen = models.BooleanField(default=False,verbose_name="Descentrada")
    presa = models.BooleanField(default=False,verbose_name="Presa")
    estrela = models.BooleanField(default=False,verbose_name="Estrela")
    furos = models.BooleanField(default=False,verbose_name="Furos")
    esp = models.BooleanField(default=False,verbose_name="Espessura")
    troca_nw = models.BooleanField(default=False,verbose_name="Troca NW")
    outros = models.BooleanField(default=False,verbose_name="Outros")
    obs = models.TextField(max_length=500, null=True, blank=True, verbose_name="Observações", default="" )

    def __str__(self):
        if self.largura.num_bobine < 10:
            return '%s-0%s' % (self.bobinagem, self.largura.num_bobine)
        else:
            return '%s-%s' % (self.bobinagem, self.largura.num_bobine)
    
    class Meta:
        verbose_name_plural = "Bobines"
    
    def get_absolute_url(self):
        return f"/producao/bobinagem/{self.bobinagem.id}"

    @classmethod
    def add_bobine(cls, palete, bobine):
        bobine = Bobine.objects.get(pk=bobine)
        palete = Palete.objects.get(pk=palete)
        if palete.num_bobines_act < palete.num_bobines:
            bobine.posicao_palete = palete.num_bobines_act + 1
            bobine.palete = palete
            palete.num_bobines_act += 1
            palete.area = bobine.largura
            bobine.save()
            palete.save()
        else:
            return redirect('/producao/palete/') 
        
    @classmethod
    def remove_bobine(cls, palete, bobine):
        bobine = Bobine.objects.get(pk=bobine)
        palete = Palete.objects.get(pk=palete)
        bobine.palete = None
        palete.num_bobines_act -= 1
        bobine_filter = Bobine.objects.filter(palete=palete)
        bobine.save()
        palete.save()
        

class Emenda(models.Model):
    bobinagem = models.ForeignKey(Bobinagem, on_delete=models.PROTECT, verbose_name="Bobinagem", null=True, blank=True,)
    bobine = models.ForeignKey(Bobine, on_delete=models.PROTECT, verbose_name="Bobine", null=True, blank=True,)
    num_emenda = models.IntegerField(verbose_name="Emenda nº", default=0)
    emenda = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Emenda metros", null=True, blank=True, default=0)
    metros = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Metros gastos", null=True, blank=True, default=0)

    def __str__(self):
        return 'Emenda nº %s da bobinagem %s' % (self.num_emenda, self.bobinagem)

    def get_absolute_url(self):
        return f"/producao/retrabalho/{self.bobinagem.id}"

class Aging(models.Model):
    pass
    
            



def bobinagem_nome(sender, instance, **kwargs):
    if not instance.nome:
        data = instance.data
        data = data.strftime('%Y%m%d')
        if instance.perfil.retrabalho == True and instance.num_emendas > 0:
            if instance.num_bobinagem < 10:
                instance.nome = '3%s-0%s' % (data, instance.num_bobinagem)

            else:
                instance.nome = '3%s-%s' % (data, instance.num_bobinagem)
        elif instance.perfil.retrabalho == True and instance.num_emendas == 0:
            if instance.num_bobinagem < 10:
                instance.nome = '4%s-0%s' % (data, instance.num_bobinagem)
            else:
                instance.nome = '4%s-%s' % (data, instance.num_bobinagem)
        else:
            if instance.num_bobinagem < 10:
                instance.nome = '%s-0%s' % (data, instance.num_bobinagem)
            else:
                instance.nome = '%s-%s' % (data, instance.num_bobinagem)
            
                 
        

def create_bobine(sender, instance, **kwargs):
    num = 1
    for i in range(instance.perfil.num_bobines):
        lar = Largura.objects.get(perfil=instance.perfil, num_bobine=num)
        
        bob = Bobine.objects.create(bobinagem=instance, largura=lar)
        if num < 10:
            bob.nome = '%s-0%s' % (instance.nome, num)
        else:
            bob.nome = '%s-%s' % (instance.nome, num)
        if bob.bobinagem.estado == 'R':
            bob.estado = 'R'
        elif bob.bobinagem.estado == 'DM':
            bob.estado = 'DM'
        elif bob.bobinagem.estado == 'G':
            bob.estado = 'G'
        elif bob.bobinagem.estado == 'BA':
            bob.estado = 'BA'
        else:
            bob.estado = 'LAB'
        bob.save() 
        num += 1



def tempo_duracao(sender, instance, **kwargs):
    if not instance.duracao:
        fim = instance.fim
        fim = fim.strftime('%H:%M')
        inico = instance.inico
        inico = inico.strftime('%H:%M')
        (hf, mf) = fim.split(':')
        (hi, mi) = inico.split(':')
        if hf < hi: 
            result = (int(hf) * 3600 + int(mf) * 60) - (int(hi) * 3600 + int(mi) * 60) + 86400
        else:
            result = (int(hf) * 3600 + int(mf) * 60) - (int(hi) * 3600 + int(mi) * 60) 
        
        result_str = strftime("%H:%M", gmtime(result))
        instance.duracao = result_str

def palete_nome(sender, instance, **kwargs):
    if not instance.nome:
        ano = instance.data_pal
        ano = ano.strftime('%Y')
        pal = Palete.objects.latest('num')
        pal = pal.num
        instance.num = pal + 1
        if pal + 1 < 10:    
            instance.nome = 'P000%s-%s' % (pal + 1, ano)  
        elif pal + 1 < 100:
            instance.nome = 'P00%s-%s' % (pal + 1, ano)
        elif pal + 1 < 1000:
            instance.nome = 'P0%s-%s' % (pal + 1, ano)
        else: 
            instance.nome = 'P%s-%s' % (pal + 1, ano)


def area_bobinagem(sender, instance, **kwargs):
    largura = instance.perfil.largura_bobinagem / 1000
    instance.area = instance.comp * largura

def area_bobine(sender, instance, **kwargs):
    largura = instance.largura.largura / 1000
    instance.area = largura * instance.comp_actual
    
def area_palete(sender, instance, **kwargs):
    bobine = Bobine.objects.filter(palete=instance.pk)
    area = 0
    comp = 0
    for b in bobine:
        area = area + b.area 
        comp = comp + b.bobinagem.comp
        
    instance.area = area
    instance.comp_total = comp

def comp_bobine(sender, instance, **kwargs):
    if instance.comp_actual == "":
        instance.comp_actual = instance.bobinagem.comp 
    else: 
        pass     
    
def emenda(sender, instance, **kwrags):
    bobinagem = Bobinagem.objects.get(pk=instance.bobinagem.pk)
    num = instance.num_emenda
    x = instance.metros
    if bobinagem.num_emendas == 0:
        instance.num_emenda = 0
        instance.emenda = 0
    elif bobinagem.num_emendas > 0:
        if num == 1:
            instance.emenda = instance.metros
        elif num == 2:
            emenda = Emenda.objects.get(bobinagem=bobinagem, num_emenda=1)
            instance.emenda = x + emenda.emenda
        
   

post_save.connect(perfil_larguras, sender=Perfil)
pre_save.connect(bobinagem_nome, sender=Bobinagem)
post_save.connect(create_bobine, sender=Bobinagem)
pre_save.connect(tempo_duracao, sender=Bobinagem)
pre_save.connect(palete_nome, sender=Palete)
pre_save.connect(area_bobinagem, sender=Bobinagem)
pre_save.connect(comp_bobine, sender=Bobine)
pre_save.connect(area_bobine, sender=Bobine)
pre_save.connect(area_palete, sender=Palete)
pre_save.connect(emenda, sender=Emenda)




