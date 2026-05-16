from django import forms
from django.utils import timezone
from .models import Sapi, Dokter, Pemeliharaan, Supervisi, Pengeluaran, Panen

class DateInput(forms.DateInput):
    input_type = 'date'

class BootstrapMixin:
    """Secara otomatis memberi class Bootstrap 5 yang benar ke setiap field"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            widget = field.widget
            if isinstance(widget, forms.Select):
                widget.attrs.update({'class': 'form-select'})
            elif isinstance(widget, forms.CheckboxInput):
                widget.attrs.update({'class': 'form-check-input'})
            else:
                widget.attrs.update({'class': 'form-control'})

class SapiForm(BootstrapMixin, forms.ModelForm):
     class Meta:
        model = Sapi
        fields = ['id_sapi', 'nama_sapi', 'rumpun', 'jenis_kelamin', 'tanggal_lahir', 'berat_badan', 'tinggi_sapi', 'status', 'foto', 'keterangan']
        widgets = {
            'tanggal_lahir': DateInput(), 
            'keterangan': forms.Textarea(attrs={'rows': 3})
        }
        
class DokterForm(BootstrapMixin, forms.ModelForm):
    class Meta:
        model = Dokter
        fields = '__all__'
        widgets = {'alamat': forms.Textarea(attrs={'rows': 2})}

class PemeliharaanForm(BootstrapMixin, forms.ModelForm):
    class Meta:
        model = Pemeliharaan
        fields = ['sapi', 'tanggal', 'jenis_pakan', 'jumlah_pakan', 'biaya_pakan', 'keterangan']
        widgets = {'tanggal': DateInput(), 'keterangan': forms.Textarea(attrs={'rows': 2})}
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Hanya tampilkan sapi yang hidup
        self.fields['sapi'].queryset = Sapi.objects.filter(status__in=['Hidup/Sehat', 'Sakit'])
        self.fields['sapi'].empty_label = "-- Pilih Sapi --"

class SupervisiForm(BootstrapMixin, forms.ModelForm):
    class Meta:
        model = Supervisi
        # TAMBAHKAN 'bukti_kuitansi' DI PALING AKHIR
        fields = ['sapi', 'dokter', 'tanggal', 'diagnosa', 'tindakan', 'resep_obat', 'berat_sapi_saat_ini', 'update_tinggi_sapi', 'bukti_kuitansi', 'biaya_konsultasi', 'update_status_sapi']
        widgets = {
            'tanggal': DateInput(), 'diagnosa': forms.Textarea(attrs={'rows': 3}),
            'tindakan': forms.Textarea(attrs={'rows': 2}), 'resep_obat': forms.Textarea(attrs={'rows': 2}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['sapi'].queryset = Sapi.objects.filter(status__in=['Hidup/Sehat', 'Sakit'])
        self.fields['sapi'].empty_label = "-- Pilih Sapi --"
        self.fields['dokter'].empty_label = "-- Pilih Dokter --"
        self.fields['tanggal'].initial = timezone.now().date()

class PengeluaranForm(BootstrapMixin, forms.ModelForm):
    class Meta:
        model = Pengeluaran
        fields = ['tanggal', 'kategori', 'deskripsi', 'jumlah', 'bukti_pembayaran']
        widgets = {'tanggal': DateInput()}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['tanggal'].initial = timezone.now().date()

class PanenForm(BootstrapMixin, forms.ModelForm):
    class Meta:
        model = Panen
        fields = ['sapi', 'tanggal', 'jenis_produksi', 'jumlah', 'satuan', 'harga_jual']
        widgets = {'tanggal': DateInput()}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['sapi'].queryset = Sapi.objects.filter(status='Hidup/Sehat')
        self.fields['sapi'].empty_label = "-- Pilih Sapi (Opsional) --"
        self.fields['tanggal'].initial = timezone.now().date()

    # ANOMALI FIX: Validasi agar tidak bisa jual sapi tanpa memilih sapi
    def clean(self):
        cleaned_data = super().clean()
        jenis = cleaned_data.get('jenis_produksi')
        sapi = cleaned_data.get('sapi')
        if jenis in ['Penjualan Sapi Dewasa', 'Anak Sapi'] and not sapi:
            raise forms.ValidationError({"sapi": "Jenis produksi ini wajib memilih sapi terkait."})
        return cleaned_data

class LaporanForm(forms.Form):
    tanggal_mulai = forms.DateField(widget=DateInput())
    tanggal_selesai = forms.DateField(widget=DateInput())