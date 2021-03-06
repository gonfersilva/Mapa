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
from decimal import *


class Perfil(models.Model):
    CORE = (('3', '3'),('6', '6'))
    user = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name="Username")
    timestamp = models.DateTimeField(auto_now_add=True)
    nome = models.CharField(verbose_name="Perfil", max_length=200, unique=True, null=True, blank=True )
    produto = models.CharField(verbose_name="Produto", max_length=200, null=True, blank=True )
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
    STATUSP = (('G', 'G'), ('DM', 'DM12'), ('R', 'R'), ('BA', 'BA'), ('LAB', 'LAB'), ('IND', 'IND'))
    TIPONW = (('Suominen 25 gsm','Suominen 25 gsm'), ('Sandler SPUNLACE 100%PP','Sandler SPUNLACE 100%PP'), ('BCN 70%PP/30%PE','BCN 70%PP/30%PE'), ('Sandler','Sandler'), ('PEGAS BICO 17gsm','PEGAS BICO 17gsm'), ('Suominen','Suominen'), ('BCN','BCN'), ('ORMA','ORMA'), ('PEGAS 22','PEGAS 22'), ('SAWASOFT','SAWASOFT'), ('SAWABOND','SAWABOND'), ('Teksis','Teksis'), ('Union','Union'),('Radici','Radici'))
    user = models.ForeignKey(User, on_delete=models.PROTECT,verbose_name="Username")
    perfil = models.ForeignKey(Perfil, on_delete=models.PROTECT,verbose_name="Perfil")
    num_emendas = models.IntegerField(verbose_name="Número de emendas", null=True, blank=True, default=0)
    timestamp = models.DateTimeField(auto_now_add=True)
    nome = models.CharField(verbose_name="Bobinagem", max_length=200, unique=True)
    data = models.DateField(auto_now_add=False, auto_now=False, default=datetime.date.today,verbose_name="Data")
    num_bobinagem = models.PositiveIntegerField(verbose_name="Bobinagem nº")
    comp = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Comprimento Final", default=0)
    tiponwsup = models.CharField(max_length=40, choices=TIPONW, default='', verbose_name="Tipo Nonwoven Superior", null=True, blank=True)
    tiponwinf = models.CharField(max_length=40, choices=TIPONW, default='', verbose_name="Tipo Nonwoven Inferior", null=True, blank=True)
    estado = models.CharField(max_length=3, choices=STATUSP, default='LAB', verbose_name="Estado")
    lotenwsup = models.CharField(verbose_name="Lote Nonwoven Superior", max_length=200, unique=False, null=True, blank=True,)
    lotenwinf = models.CharField(verbose_name="Lote Nonwoven Inferior", max_length=200, unique=False, null=True, blank=True,)
    nwsup = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Consumo Nonwoven Superior", null=True, blank=True)
    nwinf = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Consumo Nonwoven Inferior", null=True, blank=True)
    comp_par = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Comprimento Emenda", null=True, blank=True, default=0)
    comp_cli = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Comprimento Cliente", default=0)
    desper = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Desperdício", default=0)
    diam = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Diametro", null=True, blank=True)
    area = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Área")
    inico = models.TimeField(auto_now_add=False, auto_now=False, verbose_name="Início", null=True, blank=True)
    fim = models.TimeField(auto_now_add=False, auto_now=False, verbose_name="Fim", null=True, blank=True)
    duracao = models.CharField(max_length=200, null=True, blank=True, verbose_name="Duração")
    obs = models.TextField(max_length=500, null=True, blank=True, verbose_name="Observações", default="") 
    area_g = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Área Good", default=0)
    area_dm = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Área DM", default=0)
    area_r = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Área R", default=0)
    area_ind = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Área Ind", default=0)
    area_ba = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Área BA", default=0)
    

    def __str__(self):
        return self.nome
       

    @property
    def title(self):
        return self.nome
    
    class Meta:
        verbose_name_plural = "Bobinagens"
        ordering = ['-data', '-fim', '-nome']

    def get_absolute_url(self):
        return f"/producao/bobinagem/{self.id}"

class Cliente(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    cod = models.PositiveIntegerField(verbose_name="Código de cliente", unique=True)
    nome = models.CharField(max_length=200, unique=True, null=True, blank=True, verbose_name="Nome")
    limsup = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Limite Superior")
    liminf = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Limite Inferior")

    class Meta:
        verbose_name_plural = "Clientes"
        ordering = ['-timestamp', '-nome']

    def __str__(self):
        return self.nome

class PerfilPalete(models.Model):
    pass


class Palete(models.Model):
    CORE = (('3', '3'),('6', '6'))
    STATUSP = (('G', 'G'), ('DM', 'DM'))
    user            = models.ForeignKey(User, on_delete=models.PROTECT,verbose_name="Username")
    cliente         = models.ForeignKey(Cliente, on_delete=models.PROTECT,verbose_name="Cliente", null=True, blank=True)
    timestamp       = models.DateTimeField(auto_now_add=True)
    data_pal        = models.DateField(auto_now=False, auto_now_add=False, default=datetime.date.today)
    nome            = models.CharField(max_length=200, unique=True, null=True, blank=True, verbose_name="Palete")
    num             = models.IntegerField(unique=False, null=True, blank=True, verbose_name="Palete nº")
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
        ordering = ['-nome']  

class Bobine(models.Model):
    STATUSP = (('G', 'G'), ('DM', 'DM12'), ('R', 'R'), ('BA', 'BA'),('LAB', 'LAB'), ('IND', 'IND'), ('HOLD', 'HOLD'))
    bobinagem = models.ForeignKey(Bobinagem, on_delete=models.CASCADE, verbose_name="Bobinagem")
    largura =  models.ForeignKey(Largura, on_delete=models.PROTECT,  null=True, blank=True, verbose_name="Largura")
    comp_actual = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Comprimento actual", default="")
    nome = models.CharField(verbose_name="Bobine", max_length=200, null=True, blank=True, default="")
    palete = models.ForeignKey(Palete, on_delete=models.SET_NULL, null=True, blank=True)   
    posicao_palete = models.PositiveIntegerField(verbose_name="Posição", default=0)
    estado = models.CharField(max_length=4, choices=STATUSP, default='G', verbose_name="Estado")
    area = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Área bobine")
    con = models.BooleanField(default=False,verbose_name="Cónica")
    descen = models.BooleanField(default=False,verbose_name="Descentrada")
    presa = models.BooleanField(default=False,verbose_name="Presa")
    diam_insuf = models.BooleanField(default=False,verbose_name="Diâmetro insuficiente")
    furos = models.BooleanField(default=False,verbose_name="Furos")
    esp = models.BooleanField(default=False,verbose_name="Gramagem")
    troca_nw = models.BooleanField(default=False,verbose_name="Troca NW")
    outros = models.BooleanField(default=False,verbose_name="Outros")
    buraco = models.BooleanField(default=False,verbose_name="Buracos")    
    obs = models.TextField(max_length=500, null=True, blank=True, verbose_name="Observações", default="" )

    def __str__(self):
        if self.largura.num_bobine < 10:
            return '%s-0%s' % (self.bobinagem, self.largura.num_bobine)
        else:
            return '%s-%s' % (self.bobinagem, self.largura.num_bobine)
    
    class Meta:
        verbose_name_plural = "Bobines"
         
    def get_absolute_url(self):
        return f"/producao/bobine/details/{self.id}"

    @classmethod
    def add_bobine(cls, palete, bobine):
        bobine = Bobine.objects.get(pk=bobine)
        palete = Palete.objects.get(pk=palete)
        if palete.estado == 'DM':
            bobine.posicao_palete = palete.num_bobines_act + 1
            bobine.palete = palete
            palete.num_bobines_act += 1
            palete.area = bobine.largura
            bobine.save()
            palete.save()
        elif palete.num_bobines_act < palete.num_bobines:
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
    bobinagem = models.ForeignKey(Bobinagem, on_delete=models.CASCADE, verbose_name="Bobinagem", null=True, blank=True)
    bobine = models.ForeignKey(Bobine, on_delete=models.PROTECT, verbose_name="Bobine")
    num_emenda = models.IntegerField(verbose_name="Bobine nº",  null=True, blank=True, default=0)
    emenda = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Emenda metros", null=True, blank=True, default=0)
    metros = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Metros gastos", blank=True, default=0)

    def __str__(self):
        return 'Emenda nº %s da bobinagem %s' % (self.num_emenda, self.bobinagem)

    # def get_absolute_url(self):
    #     return f"/producao/retrabalho/{self.bobinagem.id}"

class Aging(models.Model):
    pass
    

def bobinagem_nome(sender, instance, **kwargs):
    if not instance.nome:
        data = instance.data
        data = data.strftime('%Y%m%d')
        map(int, data)
        if instance.perfil.retrabalho == True and instance.num_emendas > 0:
            if instance.num_bobinagem < 10:
                # instance.nome = '3%s-0%s' % (data, instance.num_bobinagem)
                instance.nome = '3%s-0%s' % (data[1:], instance.num_bobinagem)

            else:
                instance.nome = '3%s-0%s' % (data[1:], instance.num_bobinagem)
        elif instance.perfil.retrabalho == True and instance.num_emendas == 0:
            if instance.num_bobinagem < 10:
                instance.nome = '4%s-0%s' % (data[1:], instance.num_bobinagem)
            else:
                instance.nome = '4%s-%s' % (data[1:], instance.num_bobinagem)
        else:
            if instance.num_bobinagem < 10:
                instance.nome = '%s-0%s' % (data, instance.num_bobinagem)
            else:
                instance.nome = '%s-%s' % (data, instance.num_bobinagem)
            
                 
        

def create_bobine(sender, instance, **kwargs):
    num = 1
    for i in range(instance.perfil.num_bobines):
        lar = Largura.objects.get(perfil=instance.perfil, num_bobine=num)
        bob = Bobine.objects.filter(bobinagem=instance, largura=lar)
        if not bob:
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
            elif bob.bobinagem.estado == 'IND':
                bob.estado = 'IND'
            else:
                bob.estado = 'LAB'
            bob.save() 
        num += 1
    
    





def tempo_duracao(sender, instance, **kwargs):
    if instance.inico or instance.fim:
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
        # pal = Palete.objects.latest('num')
        # pal = pal.num
        # instance.num = pal + 1
        if instance.estado == 'DM':
            palete = Palete.objects.filter(estado='DM')
            num = 0
            for p in palete:
                if p.num > num:
                     num = p.num

            instance.num = num + 1
            if num + 1 < 10:
                instance.nome = 'DM000%s-%s' % (num + 1, ano)
            elif num + 1 < 100:
                instance.nome = 'DM00%s-%s' % (num + 1, ano)
            elif num + 1 < 1000:
                instance.nome = 'DM0%s-%s' % (num + 1, ano)
            else:
                instance.nome = 'DM%s-%s' % (num + 1, ano)

        elif instance.estado == 'G':
             palete = Palete.objects.filter(estado='G')
             num = 0
             for p in palete:
                if p.num > num:
                     num = p.num
             instance.num = num + 1   
             if num + 1 < 10:    
                instance.nome = 'P000%s-%s' % (num + 1, ano)  
             elif num + 1 < 100:
                instance.nome = 'P00%s-%s' % (num + 1, ano)
             elif num + 1 < 1000:
                instance.nome = 'P0%s-%s' % (num + 1, ano)
             else: 
                instance.nome = 'P%s-%s' % (num + 1, ano)
                
             


def area_bobinagem(sender, instance, **kwargs):
    largura = instance.perfil.largura_bobinagem / 1000
    instance.area = instance.comp_cli * largura
    
def area_bobine(sender, instance, **kwargs):
    largura = instance.largura.largura / 1000
    instance.area = largura * instance.comp_actual
    
def area_palete(sender, instance, **kwargs):
    bobine = Bobine.objects.filter(palete=instance.pk)
    area = 0
    comp = 0
    for b in bobine:
        if b.palete:
            area = area + b.area 
            comp = comp + b.bobinagem.comp
        
    instance.area = area
    instance.comp_total = comp

def comp_bobine(sender, instance, **kwargs):
    if instance.comp_actual == "":
        instance.comp_actual = instance.bobinagem.comp 
    else: 
        pass     
    
# def emenda(sender, instance, **kwrags):
#     bobinagem = Bobinagem.objects.get(pk=instance.bobinagem.pk)
#     num = instance.num_emenda
#     x = instance.metros
#     if bobinagem.num_emendas == 0:
#         instance.num_emenda = 0
#         instance.emenda = 0
#     elif bobinagem.num_emendas > 0:
#         if num == 1:
#             instance.emenda = instance.metros
#         elif num == 2:
#             emenda = Emenda.objects.get(bobinagem=bobinagem, num_emenda=1)
#             instance.emenda = x + emenda.emenda
        
   
def desperdicio(sender, instance, **kwargs):
    if instance.comp_par > 0:
        desp = instance.comp - instance.comp_par
        x = instance.comp_par * Decimal('0.05')
        if desp <= x:
            instance.comp_cli = instance.comp
        else:        
            instance.comp_cli = instance.comp_par * Decimal('1.05')
            instance.desper = (instance.comp - instance.comp_cli) / 1000 * instance.perfil.largura_bobinagem
    elif instance.comp_par == 0:
        instance.comp_cli = instance.comp
        instance.desper = 0
   
      

def comp_area_bobine_retrabalho(sender, instance, **kwargs):
    bobine = Bobine.objects.filter(bobinagem=instance)
    for b in bobine:
        b.comp_actual = instance.comp
        b.area = b.comp_actual * b.largura.largura
        b.save()

    
# def bobine_nome(pk):
#     bobinagem = Bobinagem.objects.get(pk=pk)
#     bobine = Bobine.objects.filter(bobinagem=bobinagem)
#     for b in bobine:
#         if b.largura.num_bobine < 10:
#             b.nome = '%s-0%s' % (bobinagem.nome, b.largura.num_bobine)
#         else:
#             b.nome = '%s-%s' % (bobinagem.nome, b.largura.num_bobine)
#         b.save()

# def area_status(sender, instance, **kwargs):
#     bobine = Bobine.objects.filter(bobinagem=instance)
#     area_g = 0
#     area_dm = 0
#     area_r = 0
#     area_ind = 0
#     area_ba = 0
#     for b in bobine:
#         if b.estado == 'G':
#             area_g += b.area
#         elif b.estado == 'DM':
#             area_dm += b.area
#         elif b.estado == 'R':
#             area_r += b.area
#         elif b.estado == 'IND':
#             area_ind += b.area
#         elif b.estado == 'BA':
#             area_ba += b.area
#         else: 
#             instance.area_g = area_g
#             instance.area_dm= area_dm
#             instance.area_r = area_r
#             instance.area_ind = area_ind
#             instance.area_ba = area_ba
#             instance.save()
            

#     instance.area_g = area_g
#     instance.area_dm= area_dm
#     instance.area_r = area_r
#     instance.area_ind = area_ind
#     instance.area_ba = area_ba
#     instance.save()


# def area_good(pk):
#     bobinagem = Bobinagem.objects.get(pk=pk)
#     bobine_g = Bobine.objects.filter(bobinagem=bobinagem, estado='G')
#     area_g = 0
#     for b_g in bobine_g:
#         area_g = b_g.area
    
#     bobinagem.area_g = area_g
#     bobinagem.save()

def update_areas(sender, instance, **kwargs):
    post_save.disconnect(update_areas, sender=sender)
    bobine = Bobine.objects.get(pk=instance.pk)
    bobinagem = Bobinagem.objects.get(pk=bobine.bobinagem.pk)
    bobines = Bobine.objects.filter(bobinagem=bobinagem)
    area_g = 0
    area_dm = 0
    area_r = 0
    area_ind = 0
    area_ba = 0
    
    for b in bobines:
         estado = b.estado

         if estado == 'G':
             area_g += b.area
        
         elif estado == 'R':
            area_r += b.area
        
         elif estado == 'DM':
             area_dm += b.area

         elif estado == 'IND':
             area_ind += b.area

         elif estado == 'BA':
             area_ba += b.area
    
    bobinagem.area_g = area_g
    bobinagem.area_r = area_r
    bobinagem.area_dm = area_dm
    bobinagem.area_ind = area_ind
    bobinagem.area_ba = area_ba
    bobinagem.save()

    post_save.connect(update_areas, sender=sender)



post_save.connect(perfil_larguras, sender=Perfil)
pre_save.connect(bobinagem_nome, sender=Bobinagem)
pre_save.connect(desperdicio, sender=Bobinagem)
post_save.connect(create_bobine, sender=Bobinagem)
post_save.connect(comp_area_bobine_retrabalho, sender=Bobinagem)
# post_save.connect(area_status, sender=Bobinagem)
pre_save.connect(tempo_duracao, sender=Bobinagem)
pre_save.connect(palete_nome, sender=Palete)
pre_save.connect(area_bobinagem, sender=Bobinagem)
pre_save.connect(comp_bobine, sender=Bobine)
pre_save.connect(area_bobine, sender=Bobine)
pre_save.connect(area_palete, sender=Palete)
post_save.connect(update_areas, sender=Bobine)





