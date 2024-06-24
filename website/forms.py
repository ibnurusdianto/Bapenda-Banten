from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Kuesioner, Layanan, JawabanKuesioner, SubUnit, Responden, UnsurPelayanan

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        label="",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
    )
    first_name = forms.CharField(
        label="",
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
    )
    last_name = forms.CharField(
        label="",
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
    )

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in self.fields:
            self.fields[field_name].widget.attrs.update({'class': 'form-control'})
        self.fields['username'].widget.attrs['placeholder'] = 'User Name'
        self.fields['username'].help_text = (
            '<span class="form-text text-muted"><small>'
            'Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'
            '</small></span>'
        )

class SubUnitForm(forms.ModelForm):
    class Meta:
        model = SubUnit
        fields = [
            'nama_sub_unit', 'pertanyaan', 'telepon_fax', 'koordinator',
            'jumlah_mesin', 'potensi_ikm', 'email', 'jenis_layanan'
        ]

class RespondenForm(forms.ModelForm):
    class Meta:
        model = Responden
        fields = [
            'uptd', 'nama', 'jenis_kelamin', 'email', 'no_telepon',
            'nopol_kendaraan', 'jenis_layanan'
        ]

class UnsurPelayananForm(forms.ModelForm):
    class Meta:
        model = UnsurPelayanan
        fields = ['nama_unsur']

class KuesionerForm(forms.ModelForm):
    layanan = forms.ModelChoiceField(queryset=Layanan.objects.all(), required=True)
    class Meta:
        model = Kuesioner
        fields = ['isi_pertanyaan', 'opsi_a', 'opsi_b', 'opsi_c', 'opsi_d', 'layanan']

class JawabanKuesionerForm(forms.ModelForm):
    class Meta:
        model = JawabanKuesioner
        fields = ['responden', 'pertanyaan', 'jawaban']

class LayananForm(forms.ModelForm):
    class Meta:
        model = Layanan
        fields = ['nama_layanan']