from django.urls import path
from . import views
from .views import layanan_list, layanan_create, layanan_update, layanan_delete

urlpatterns = [
    # Authentication and home page
    path('', views.home, name='home'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),

    # Respondent
    path('respondent/', views.respondent_admin, name='respondent'),
    path('respondent/edit/<int:id>/', views.edit_responden, name='edit_responden'),
    path('respondent/delete/<int:id>/', views.hapus_responden, name='hapus_responden'),

    # Admin Dashboard
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),

    # UPTD Admin Section
    path('admin_dashboard/updt/', views.admin_updt, name='admin_updt'),
    path('admin_dashboard/updt/tambah/', views.tambah_updt, name='tambah_updt'),
    path('admin_dashboard/updt/delete/<int:subunit_id>/', views.delete_uptd, name='delete_uptd'),
    path('admin_dashboard/updt/edit/<int:subunit_id>/', views.edit_uptd, name='edit_uptd'),

    # Other Admin Sections
    path('admin_dashboard/survey_unsur_IKM/', views.survey_unsur_IKM, name='survey_unsur_IKM'),
    path('admin_dashboard/survey_unsur_IKM/delete/<int:id>/', views.hapus_unsur, name='hapus_unsur'),
    path('admin_dashboard/kusioner/', views.kusioner, name='kusioner'),
    path('admin_dashboard/hasil_survey/', views.hasil_survey, name='hasil_survey'),
    path('keep-alive/', views.keep_alive, name='keep_alive'),

    # Adding IKM elements and questionnaires
    path('admin_dashboard/tambah_unsur_IKM/', views.tambah_unsur_IKM, name='tambah_unsur_IKM'),
    path('admin_dashboard/survey_unsur_IKM/edit/<int:id>/', views.edit_unsur, name='edit_unsur'),
    path('admin_dashboard/tambah_kuesioner/', views.tambah_kuesioner, name='tambah_kuesioner'),
    path('admin_dashboard/edit_kuesioner/<int:id>/', views.edit_kuesioner, name='edit_kuesioner'),
    path('admin_dashboard/delete_kuesioner/<int:id>/', views.delete_kuesioner, name='delete_kuesioner'),

    # User Section
    path('user/', views.user_biasa, name='user_biasa'),
    path('user/isi_kusioner/', views.isi_kusioner, name='isi_kusioner'),
    # path('user/submit_survey/', views.submit_survey, name='submit_survey'),

    # Layanan Section
    path('layanan/', layanan_list, name='layanan_list'),
    path('layanan/create/', layanan_create, name='layanan_create'),
    path('layanan/update/<int:pk>/', layanan_update, name='layanan_update'),
    path('layanan/delete/<int:pk>/', layanan_delete, name='layanan_delete'),
]