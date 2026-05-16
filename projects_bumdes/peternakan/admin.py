from django.contrib import admin
from .models import Sapi, Dokter, Pemeliharaan, Supervisi, Pengeluaran, Panen

@admin.register(Sapi)
class SapiAdmin(admin.ModelAdmin):
    list_display = ('id_sapi', 'nama_sapi', 'jenis_kelamin', 'status')
    search_fields = ('id_sapi', 'nama_sapi')

@admin.register(Dokter)
class DokterAdmin(admin.ModelAdmin):
    list_display = ('nama', 'no_telepon')

@admin.register(Pemeliharaan)
class PemeliharaanAdmin(admin.ModelAdmin):
    list_display = ('sapi', 'tanggal', 'jenis_pakan', 'biaya_pakan')

@admin.register(Supervisi)
class SupervisiAdmin(admin.ModelAdmin):
    list_display = ('sapi', 'dokter', 'tanggal', 'update_status_sapi')

@admin.register(Pengeluaran)
class PengeluaranAdmin(admin.ModelAdmin):
    list_display = ('tanggal', 'kategori', 'deskripsi', 'jumlah')

@admin.register(Panen)
class PanenAdmin(admin.ModelAdmin):
    list_display = ('tanggal', 'jenis_produksi', 'jumlah', 'satuan', 'total_pendapatan_display')
    def total_pendapatan_display(self, obj):
        return f"Rp {obj.total_pendapatan:,.0f}"