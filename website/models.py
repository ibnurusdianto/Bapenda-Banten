from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.utils import timezone

class Layanan(models.Model):
    nama_layanan = models.CharField(max_length=255)

    def __str__(self):
        return self.nama_layanan

class SubUnit(models.Model):
    nama_sub_unit = models.CharField(max_length=255)
    pertanyaan = models.TextField()
    telepon_fax = models.CharField(max_length=20)
    koordinator = models.CharField(max_length=100)
    jumlah_mesin = models.PositiveIntegerField()
    potensi_ikm = models.CharField(max_length=255)
    email = models.EmailField()
    jenis_layanan = models.ForeignKey(Layanan, on_delete=models.CASCADE)

    def __str__(self):
        return self.nama_sub_unit

class Responden(models.Model):
    uptd = models.ForeignKey(SubUnit, on_delete=models.CASCADE)
    nama = models.CharField(max_length=255)
    jenis_kelamin = models.CharField(max_length=10)
    email = models.EmailField()
    no_telepon = models.CharField(max_length=20)
    nopol_kendaraan = models.CharField(max_length=20)
    jenis_layanan = models.ForeignKey(Layanan, on_delete=models.CASCADE)
    tanggal_survey = models.DateField(default=timezone.now)

    def __str__(self):
        return self.nama

class UnsurPelayanan(models.Model):
    nama_unsur = models.CharField(max_length=255)

    def __str__(self):
        return self.nama_unsur

class Kuesioner(models.Model):
    isi_pertanyaan = models.TextField()
    opsi_a = models.CharField(max_length=255)
    opsi_b = models.CharField(max_length=255)
    opsi_c = models.CharField(max_length=255)
    opsi_d = models.CharField(max_length=255)
    layanan = models.ForeignKey(Layanan, on_delete=models.CASCADE)

    def __str__(self):
        return self.isi_pertanyaan

class CustomUser(AbstractUser):
    login_count = models.IntegerField(default=0)
    groups = models.ManyToManyField(
        Group,
        related_name='customuser_set',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_query_name='customuser',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='customuser_set',
        blank=True,
        help_text='Specific permissions for this user.',
        related_query_name='customuser',
    )

    def increment_login_count(self):
        self.login_count += 1
        self.save()

class JawabanKuesioner(models.Model):
    responden = models.ForeignKey(Responden, on_delete=models.CASCADE)
    pertanyaan = models.ForeignKey(Kuesioner, on_delete=models.CASCADE)
    jawaban = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.responden.nama} - {self.pertanyaan.isi_pertanyaan}"