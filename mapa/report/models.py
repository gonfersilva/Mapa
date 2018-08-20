from django.db import models
from django.contrib.auth.models import User

class Report(models.Model):
    MODULO = (('Produção','Produção'), ('Planeamento','Planeamento'), ('Outro', 'Outro')) 
    STATUS = (('Aberto','Aberto'), ('Em análise','Em análise'), ('Fechado', 'Fechado')) 
    user = models.ForeignKey(User, on_delete=models.PROTECT,verbose_name="Username")
    timestamp = models.DateTimeField(auto_now_add=True)
    assunto = models.CharField(verbose_name="Assunto", max_length=30, unique=False)
    descricao = models.TextField(max_length=500, verbose_name="Descrição")
    modulo =  models.CharField(max_length=20, choices=MODULO, default='', verbose_name="Módulo")
    estado =  models.CharField(max_length=20, choices=STATUS, default='Aberto', verbose_name="Estado")
    anexo = models.FileField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Reports"
        ordering = ['-timestamp']

    def __str__(self):
        return '%s - %s (%s)' % (self.assunto, self.user, self.estado)

    def get_absolute_url(self):
        return f"{self.id}"