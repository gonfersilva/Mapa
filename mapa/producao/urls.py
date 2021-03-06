from django.conf.urls import url, include
from . import views
from .views import bobine_details, relatorio_diario, retrabalho_filter, planeamento_home, bobinagem_list, producao_home, cliente_home, emenda_delete, BobinagemRetrabalhoFinalizar, ClienteCreateView, finalizar_retrabalho, RetrabalhoCreateView, BobinagemUpdate, palete_retrabalho, retrabalho_home, palete_create_retrabalho, picagem, add_bobine_palete_erro, palete_delete, bobinagem_delete, perfil_delete, CreatePerfil, PerfilListView, perfil_detail, LarguraUpdate, BobinagemListView, BobinagemCreateView, bobinagem_status, add_bobine_palete, BobineUpdate, palete_change, PaleteListView, PaleteCreateView, status_bobinagem

app_name="producao" 

urlpatterns = [
    
    url(r'^$', producao_home, name='producao_home'),
    url(r'^planeamento/$', planeamento_home, name='planeamento_home'),
    url(r'^perfil/$', PerfilListView.as_view(), name='perfil'),
    url(r'^perfil/(?P<pk>\d+)/', perfil_detail, name='perfil_details'),
    url(r'^perfil/delete/(?P<pk>\d+)/', perfil_delete, name='perfil_delete'),
    url(r'^perfil/update/(?P<pk>\d+)/', LarguraUpdate.as_view(), name='perfil_update_largura'),
    url(r'^perfil/create/$', CreatePerfil.as_view(), name='perfil_create'),
    url(r'^bobinagem/$', bobinagem_list, name='bobinagens'),
    url(r'^bobinagem/create/$', BobinagemCreateView.as_view(), name='bobinagem_create'),
    url(r'^bobinagem/(?P<pk>\d+)/', bobinagem_status, name='bobinestatus'),
    url(r'^bobinagem/update/(?P<pk>\d+)/', BobinagemUpdate.as_view(), name='bobinagemupdate'),
    url(r'^bobinagem/delete/(?P<pk>\d+)/', bobinagem_delete, name='bobinagem_delete'),
    url(r'^bobinagem/(?P<operation>.+)/(?P<pk>\d+)/', status_bobinagem, name='bobinagem_status'),
    url(r'^bobine/(?P<pk>\d+)/', BobineUpdate.as_view(), name='bobineupdate'),
    url(r'^bobine/details/(?P<pk>\d+)/', bobine_details, name='bobine_details'),
    url(r'^palete/$', PaleteListView.as_view(), name='paletes'),
    url(r'^palete/retrabalho/$', palete_retrabalho, name='paletes_retrabalho'),
    url(r'^palete/create/$', PaleteCreateView.as_view(), name='palete_create'),
    url(r'^palete/createretrabalho/$', palete_create_retrabalho, name='palete_create_retrabalho'),
    url(r'^palete/(?P<pk>\d+)/$', add_bobine_palete, name='addbobinepalete'),
    url(r'^palete/delete/(?P<pk>\d+)/$', palete_delete, name='palete_delete'),
    url(r'^palete/(?P<pk>\d+)/(?P<e>\d+)/$', add_bobine_palete_erro, name='addbobinepaleteerro'),
    url(r'^palete/(?P<pk>\d+)/picagem/$', picagem, name='picagem'),
    url(r'^palete/(?P<operation>.+)/(?P<pk_bobine>\d+)/(?P<pk_palete>\d+)/$', palete_change, name='paletebobine'),
    url(r'^retrabalho/$', retrabalho_home, name='retrabalho_home'),
    url(r'^retrabalho/filter/(?P<pk>\d+)/', retrabalho_filter, name='retrabalho_filter'),
    url(r'^retrabalho/filter/delete/(?P<pk>\d+)/', emenda_delete, name='emenda_delete'),
    url(r'^retrabalho/create/$', RetrabalhoCreateView.as_view(), name='retrabalho_bobinagem'),
    url(r'^retrabalho/filter/finalizar/(?P<pk>\d+)/$', BobinagemRetrabalhoFinalizar.as_view(), name='finalizar_retrabalho'),
    url(r'^clientes/$', cliente_home, name='clientes'),
    url(r'^clientes/create/$', ClienteCreateView.as_view(), name='cliente_create'),
    url(r'^relatorio/linha/$', relatorio_diario, name='relatorio_diario'),
       
    
    
]