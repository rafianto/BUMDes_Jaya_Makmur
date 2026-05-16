from django.db import models

class Sapi(models.Model):
    JENIS_KELAMIN = (('Jantan', 'Jantan'), ('Betina', 'Betina'))
    STATUS = (('Hidup/Sehat', 'Hidup/Sehat'), ('Sakit', 'Sakit'), ('Dijual', 'Dijual'), ('Mati', 'Mati'))
    RUMPUN = (
        ('Limousin', 'Limousin'),
        ('Simmental', 'Simmental'),
        ('Brahman', 'Brahman'),
        ('Ongole', 'Ongole'),
        ('Bali', 'Bali'),
        ('Madura', 'Madura'),
        ('Holstein', 'Holstein (Frisian)'),
        ('POH', 'Peranakan Ongole Hilang'),
        ('PO', 'PO'),
        ('Lainnya', 'Lainnya'),
    )
    
    id_sapi = models.CharField(max_length=20, unique=True, verbose_name="ID Sapi")
    nama_sapi = models.CharField(max_length=100)
    rumpun = models.CharField(max_length=20, choices=RUMPUN, default='Lainnya', verbose_name="Rumpun/Breed")
    jenis_kelamin = models.CharField(max_length=10, choices=JENIS_KELAMIN)
    tanggal_lahir = models.DateField()
    berat_badan = models.DecimalField(max_digits=8, decimal_places=2, help_text="Dalam Kilogram")
    tinggi_sapi = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True, help_text="Tinggi gumba/pundak dalam cm", verbose_name="Tinggi (cm)")
    status = models.CharField(max_length=15, choices=STATUS, default='Hidup/Sehat')
    foto = models.ImageField(upload_to='images/', blank=True, null=True)
    keterangan = models.TextField(blank=True, null=True)
    tanggal_masuk = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ['-tanggal_masuk']

    def __str__(self):
        return f"{self.id_sapi} - {self.nama_sapi}"


class Dokter(models.Model):
    nama = models.CharField(max_length=100, verbose_name="Nama Dokter Hewan")
    no_telepon = models.CharField(max_length=15)
    alamat = models.TextField(blank=True, null=True)
    spesialisasi = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.nama


class Pemeliharaan(models.Model):
    sapi = models.ForeignKey(Sapi, on_delete=models.CASCADE, related_name='riwayat_pakan')
    tanggal = models.DateField()
    jenis_pakan = models.CharField(max_length=100)
    jumlah_pakan = models.DecimalField(max_digits=8, decimal_places=2)
    biaya_pakan = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Biaya (Rp)")
    keterangan = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Pakan {self.sapi.nama_sapi} - {self.tanggal}"


class Supervisi(models.Model):
    sapi = models.ForeignKey(Sapi, on_delete=models.CASCADE, related_name='riwayat_medis')
    dokter = models.ForeignKey(Dokter, on_delete=models.CASCADE, related_name='riwayat_medis')
    tanggal = models.DateField()
    diagnosa = models.TextField()
    tindakan = models.TextField(blank=True, null=True)
    resep_obat = models.TextField(blank=True, null=True)
    berat_sapi_saat_ini = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    update_tinggi_sapi = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True)
    
    # TAMBAHKAN FIELD INI:
    bukti_kuitansi = models.ImageField(upload_to='images/kuitansi/', blank=True, null=True, verbose_name="Bukti Kuitansi/Tindakan")
    
    biaya_konsultasi = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    update_status_sapi = models.CharField(max_length=15, choices=Sapi.STATUS, default='Hidup/Sehat')



class Pengeluaran(models.Model):
    KATEGORI = (('Pakan', 'Pakan'), ('Obat & Vaksin', 'Obat & Vaksin'), ('Gaji', 'Gaji'), ('Operasional', 'Operasional'), ('Lainnya', 'Lainnya'))
    
    tanggal = models.DateField()
    kategori = models.CharField(max_length=20, choices=KATEGORI)
    deskripsi = models.CharField(max_length=255)
    jumlah = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Jumlah (Rp)")
    bukti_pembayaran = models.ImageField(upload_to='images/', blank=True, null=True)

    def __str__(self):
        return f"{self.kategori}: {self.deskripsi}"


class Panen(models.Model):
    JENIS = (('Susu', 'Susu'), ('Pupuk Kandang', 'Pupuk Kandang'), ('Anak Sapi', 'Anak Sapi'), ('Penjualan Sapi Dewasa', 'Penjualan Sapi Dewasa'))
    
    sapi = models.ForeignKey(Sapi, on_delete=models.SET_NULL, null=True, blank=True, related_name='riwayat_panen')
    tanggal = models.DateField()
    jenis_produksi = models.CharField(max_length=25, choices=JENIS)
    jumlah = models.DecimalField(max_digits=12, decimal_places=2)
    satuan = models.CharField(max_length=10, default='Liter')
    harga_jual = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Harga Jual per Satuan (Rp)")
    
    @property
    def total_pendapatan(self):
        return self.jumlah * self.harga_jual

    def __str__(self):
        return f"{self.jenis_produksi} - {self.tanggal}"