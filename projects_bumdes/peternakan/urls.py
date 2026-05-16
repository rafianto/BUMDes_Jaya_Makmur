from django.urls import path
from . import views

app_name = 'peternakan'

urlpatterns = [
    # AUTH (LOGIN & LOGOUT) -> HARUS ADA DI PALING ATAS
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Dashboard
    path('', views.DashboardView.as_view(), name='dashboard'),
    
    # Modul Sapi
    path('sapi/', views.SapiListView.as_view(), name='sapi_list'),
    path('sapi/tambah/', views.SapiCreateView.as_view(), name='sapi_tambah'),
    path('sapi/<int:pk>/edit/', views.SapiUpdateView.as_view(), name='sapi_edit'),
    path('sapi/<int:pk>/', views.SapiDetailView.as_view(), name='sapi_detail'),
    path('sapi/<int:pk>/hapus/', views.SapiDeleteView.as_view(), name='sapi_hapus'),
    
    # Modul Dokter
    path('dokter/', views.DokterListView.as_view(), name='dokter_list'),
    path('dokter/tambah/', views.DokterCreateView.as_view(), name='dokter_tambah'),
    path('dokter/<int:pk>/edit/', views.DokterUpdateView.as_view(), name='dokter_edit'),
    path('dokter/<int:pk>/hapus/', views.DokterDeleteView.as_view(), name='dokter_hapus'),
    
    # Modul Pemeliharaan
    path('pemeliharaan/', views.PemeliharaanListView.as_view(), name='pemeliharaan_list'),
    path('pemeliharaan/tambah/', views.PemeliharaanCreateView.as_view(), name='pemeliharaan_tambah'),
    path('pemeliharaan/download-excel/', views.export_pemeliharaan_excel, name='pemeliharaan_export_excel'), # <-- TAMBAHKAN INI
    path('pemeliharaan/<int:pk>/edit/', views.PemeliharaanUpdateView.as_view(), name='pemeliharaan_edit'),
    path('pemeliharaan/<int:pk>/hapus/', views.PemeliharaanDeleteView.as_view(), name='pemeliharaan_hapus'),
    
    # Modul Supervisi
    path('supervisi/', views.SupervisiListView.as_view(), name='supervisi_list'),
    path('supervisi/tambah/', views.SupervisiCreateView.as_view(), name='supervisi_tambah'),
    
    # Modul Pengeluaran
    path('pengeluaran/', views.PengeluaranListView.as_view(), name='pengeluaran_list'),
    path('pengeluaran/tambah/', views.PengeluaranCreateView.as_view(), name='pengeluaran_tambah'),
    path('pengeluaran/<int:pk>/hapus/', views.PengeluaranDeleteView.as_view(), name='pengeluaran_hapus'),
    
    # Modul Panen
    path('panen/', views.PanenListView.as_view(), name='panen_list'),
    path('panen/tambah/', views.PanenCreateView.as_view(), name='panen_tambah'),
    path('panen/<int:pk>/hapus/', views.PanenDeleteView.as_view(), name='panen_hapus'),
    
    # Laporan
    path('laporan/', views.LaporanView.as_view(), name='laporan'),
]