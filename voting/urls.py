from django.urls import path
from . import views

# app_name: Necesario para que el {% url 'voting:vote_submit' %} funcione
app_name = 'voting' 

urlpatterns = [
    # Rutas Principales
    path('', views.index_view, name='index'), # Añadido por si no existía
    path('guia/', views.guide_view, name='guide'),
    path('generate-keys/', views.key_generation_view, name='generate_keys'),
    path('vote/', views.vote_submission_view, name='vote_submit'), 
    path('success/', views.success_page, name='success_page'), 
    
    # Rutas de Resultados y Auditoría
    path('results/', views.results_dashboard_view, name='results_dashboard'), # Tablero Público (Gráficos)
    path('auditoria/', views.audit_view, name='audit_view'), # <-- NUEVA URL para Auditoría Detallada
    path('verify/', views.verification_page, name='verification_page'),
    path('creditos/', views.credits_view, name='credits'),
    
    path('login/', views.login_view, name='login'), # Correcto: usa views.login_view
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    
    path('verificar-llave/', views.check_key_status, name='check_key'),
]