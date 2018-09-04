from django.conf.urls import url, include
from . import views
from .views import RetrabalhoCreateView, palete_retrabalho, palete_create_retrabalho, picagem, add_bobine_palete_erro, palete_delete, bobinagem_delete, perfil_delete, create_emenda, bobinagem_emendas, CreatePerfil, PerfilListView, perfil_detail, LarguraUpdate, BobinagemListView, BobinagemCreateView, bobinagem_status, add_bobine_palete, BobineUpdate, palete_change, PaleteListView, PaleteCreateView, BobinagemRetrabalhoListView, status_bobinagem

app_name="producao" 

urlpatterns = [
    
    url(r'^perfil/$', PerfilListView.as_view(), name='perfil'),
    url(r'^perfil/(?P<pk>\d+)/', perfil_detail, name='perfil_details'),
    url(r'^perfil/delete/(?P<pk>\d+)/', perfil_delete, name='perfil_delete'),
    url(r'^perfil/update/(?P<pk>\d+)/', LarguraUpdate.as_view(), name='perfil_update_largura'),
    url(r'^perfil/create/$', CreatePerfil.as_view(), name='perfil_create'),
    url(r'^bobinagem/$', BobinagemListView.as_view(), name='bobinagens'),
    url(r'^bobinagem/create/$', BobinagemCreateView.as_view(), name='bobinagem_create'),
    url(r'^bobinagem/(?P<pk>\d+)/', bobinagem_status, name='bobinestatus'),
    url(r'^bobinagem/delete/(?P<pk>\d+)/', bobinagem_delete, name='bobinagem_delete'),
    url(r'^bobinagem/(?P<operation>.+)/(?P<pk>\d+)/', status_bobinagem, name='bobinagem_status'),
    url(r'^bobine/(?P<pk>\d+)/', BobineUpdate.as_view(), name='bobineupdate'),
    url(r'^palete/$', PaleteListView.as_view(), name='paletes'),
    url(r'^palete/retrabalho/$', palete_retrabalho, name='paletes_retrabalho'),
    url(r'^palete/create/$', PaleteCreateView.as_view(), name='palete_create'),
    url(r'^palete/createretrabalho/$', palete_create_retrabalho, name='palete_create_retrabalho'),
    url(r'^palete/(?P<pk>\d+)/$', add_bobine_palete, name='addbobinepalete'),
    url(r'^palete/delete/(?P<pk>\d+)/$', palete_delete, name='palete_delete'),
    url(r'^palete/(?P<pk>\d+)/(?P<e>\d+)/$', add_bobine_palete_erro, name='addbobinepaleteerro'),
    url(r'^palete/(?P<pk>\d+)/picagem/$', picagem, name='picagem'),
    url(r'^palete/(?P<operation>.+)/(?P<pk_bobine>\d+)/(?P<pk_palete>\d+)/$', palete_change, name='paletebobine'),
    url(r'^retrabalho/$', BobinagemRetrabalhoListView.as_view(), name='retrabalho'),
    url(r'^retrabalho/create/$', RetrabalhoCreateView.as_view(), name='retrabalho_create'),
    url(r'^retrabalho/(?P<pk>\d+)/$', bobinagem_emendas, name='retrabalho_emendas'),
    url(r'^retrabalho/(?P<pk>\d+)/emenda/$', create_emenda, name='emenda'),
]