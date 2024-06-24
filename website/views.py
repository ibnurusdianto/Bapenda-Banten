from datetime import datetime, timedelta
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.views.decorators.csrf import csrf_protect

from .forms import CustomUserCreationForm, SubUnitForm, RespondenForm, UnsurPelayananForm, KuesionerForm, LayananForm
from .models import SubUnit, Responden, UnsurPelayanan, Kuesioner, CustomUser, Layanan

User = get_user_model()

def home(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome {username}!')
            if user.is_superuser:
                return redirect('admin_dashboard')
            else:
                return redirect('user_biasa')
        else:
            messages.error(request, 'Incorrect username or password.')
        return redirect('home')

    if request.user.is_authenticated:
        last_activity = request.session.get('last_activity')
        timeout = settings.SESSION_COOKIE_AGE
        if last_activity:
            last_activity_time = datetime.strptime(last_activity, "%Y-%m-%d %H:%M:%S")
            last_activity_time = timezone.make_aware(last_activity_time, timezone.get_current_timezone())
            elapsed_time = (timezone.now() - last_activity_time).seconds
            if elapsed_time > timeout:
                logout(request)
                messages.info(request, 'Anda telah logout otomatis karena tidak ada aktivitas.')
        request.session['last_activity'] = timezone.now().strftime("%Y-%m-%d %H:%M:%S")

    return render(request, 'home.html')

def user_biasa(request):
    return render(request, 'user/index.html')

def register_user(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            try:
                validate_password(form.cleaned_data['password2'])
            except ValidationError as e:
                form.add_error('password2', e)
            if User.objects.filter(email=form.cleaned_data['email']).exists():
                form.add_error('email', 'Email sudah terdaftar.')
            if form.is_valid():
                user = form.save()
                login(request, user)
                messages.success(request, "Pendaftaran berhasil!")
                if user.is_superuser:
                    return redirect('admin_dashboard')
                else:
                    return redirect('user_biasa')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

def keep_alive(request):
    if request.method == 'POST' and request.user.is_authenticated:
        request.session['last_activity'] = timezone.now().strftime("%Y-%m-%d %H:%M:%S")
    return HttpResponse()

def logout_user(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('home')

# Views untuk dashboard admin
def respondent_admin(request):
    respondents = Responden.objects.all()

    id_sub_unit = request.POST.get('id_sub_unit')
    no_pol = request.POST.get('no_pol')
    no_phone = request.POST.get('no_phone')

    if id_sub_unit:
        respondents = respondents.filter(uptd__id=id_sub_unit)
    if no_pol:
        respondents = respondents.filter(nopol_kendaraan__icontains=no_pol)
    if no_phone:
        respondents = respondents.filter(no_telepon__icontains=no_phone)

    subunits = SubUnit.objects.all()
    return render(request, 'admin-dashboard/responden.html', {'respondents': respondents, 'subunits': subunits})

def edit_responden(request, id):
    responden = get_object_or_404(Responden, id=id)
    if request.method == 'POST':
        form = RespondenForm(request.POST, instance=responden)
        if form.is_valid():
            form.save()
            return redirect('respondent')
    else:
        form = RespondenForm(instance=responden)
    return render(request, 'admin-dashboard/edit_responden.html', {'form': form})

def hapus_responden(request, id):
    responden = get_object_or_404(Responden, id=id)
    if request.method == 'POST':
        subunit = responden.uptd
        responden.delete()
        # Check if there are no more respondents linked to the subunit
        if not Responden.objects.filter(uptd=subunit).exists():
            subunit.delete()
        return redirect('respondent')
    return render(request, 'admin-dashboard/responden.html', {'responden': responden})

def admin_dashboard(request):
    # Logika untuk menentukan user aktif
    active_users = User.objects.all()
    user_aktif = []
    for user in active_users:
        last_login = user.last_login
        if last_login and (timezone.now() - last_login) < timedelta(minutes=5):
            user.is_online = True
        else:
            user.is_online = False
        user_aktif.append(user)

    # Logika untuk menentukan top profiles
    top_profiles = User.objects.all().order_by('-login_count')[:10]

    return render(request, 'admin-dashboard/index.html', {
        'user_aktif': user_aktif,
        'top_profiles': top_profiles,
    })

def admin_updt(request):
    if request.method == 'POST':
        subunit_form = SubUnitForm(request.POST)
        if subunit_form.is_valid():
            subunit = subunit_form.save()
            Responden.objects.create(
                uptd=subunit,
                nama=subunit.nama_sub_unit,
                jenis_kelamin='Tidak Diketahui',
                email=subunit.email,
                no_telepon=subunit.telepon_fax,
                nopol_kendaraan='Tidak Diketahui',
                jenis_layanan=subunit.jenis_layanan
            )
            if subunit.potensi_ikm:
                UnsurPelayanan.objects.create(nama_unsur=subunit.potensi_ikm)
            return redirect('admin_updt')
    else:
        subunit_form = SubUnitForm()

    subunits = SubUnit.objects.all()
    layanan_list = Layanan.objects.all()
    return render(request, 'admin-dashboard/uptd.html', {'subunits': subunits, 'subunit_form': subunit_form, 'layanan_list': layanan_list})


def delete_uptd(request, subunit_id):
    subunit = get_object_or_404(SubUnit, id=subunit_id)
    subunit.delete()
    return redirect('admin_updt')

@csrf_protect
def edit_uptd(request, subunit_id):
    subunit = get_object_or_404(SubUnit, id=subunit_id)
    if request.method == 'POST':
        form = SubUnitForm(request.POST, instance=subunit)
        if form.is_valid():
            form.save()
            return redirect('admin_updt')
    else:
        form = SubUnitForm(instance=subunit)
    layanan_list = Layanan.objects.all()
    return render(request, 'admin-dashboard/edit_uptd.html', {'form': form, 'subunit': subunit, 'layanan_list': layanan_list})

def tambah_updt(request):
    if request.method == 'POST':
        form = SubUnitForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_updt')
    else:
        form = SubUnitForm()
    return render(request, 'admin-dashboard/tambah_uptd.html', {'form': form})

def survey_unsur_IKM(request):
    daftar_unsur = UnsurPelayanan.objects.all()
    return render(request, 'admin-dashboard/unsurikm.html', {'daftar_unsur': daftar_unsur})

def tambah_unsur_IKM(request):
    if request.method == 'POST':
        form = UnsurPelayananForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('survey_unsur_IKM')
    else:
        form = UnsurPelayananForm()
    return render(request, 'admin-dashboard/unsur/tambah.html', {'form': form})

def edit_unsur(request, id):
    unsur = get_object_or_404(UnsurPelayanan, id=id)
    if request.method == 'POST':
        form = UnsurPelayananForm(request.POST, instance=unsur)
        if form.is_valid():
            form.save()
            return redirect('survey_unsur_IKM')
    else:
        form = UnsurPelayananForm(instance=unsur)
    return render(request, 'admin-dashboard/unsur/edit_unsur.html', {'form': form})

def hapus_unsur(request, id):
    unsur = get_object_or_404(UnsurPelayanan, id=id)
    if request.method == 'POST':
        unsur.delete()
        return redirect('survey_unsur_IKM')
    return render(request, 'admin-dashboard/unsurikm.html', {'unsur': unsur})

def kusioner(request):
    daftar_pertanyaan = Kuesioner.objects.all()
    layanan_list = Layanan.objects.all()
    return render(request, 'admin-dashboard/kuesioner.html', {'daftar_pertanyaan': daftar_pertanyaan, 'layanan_list': layanan_list})

def tambah_kuesioner(request):
    if request.method == 'POST':
        form = KuesionerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('kusioner')
    else:
        form = KuesionerForm()
    layanan_list = Layanan.objects.all()
    return render(request, 'admin-dashboard/kuesioner/tambah.html', {'form': form, 'layanan_list': layanan_list})

def edit_kuesioner(request, id):
    kuesioner = get_object_or_404(Kuesioner, id=id)
    if request.method == 'POST':
        form = KuesionerForm(request.POST, instance=kuesioner)
        if form.is_valid():
            form.save()
            return redirect('kusioner')
    else:
        form = KuesionerForm(instance=kuesioner)
    layanan_list = Layanan.objects.all()
    return render(request, 'admin-dashboard/kuesioner/edit.html', {'form': form, 'layanan_list': layanan_list})

def delete_kuesioner(request, id):
    kuesioner = get_object_or_404(Kuesioner, id=id)
    if request.method == 'POST':
        kuesioner.delete()
        return redirect('kusioner')
    return render(request, 'admin-dashboard/kuesioner/delete.html', {'kuesioner': kuesioner})

def hasil_survey(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    if start_date and end_date:
        hasil_surveys = Responden.objects.filter(tanggal_survey__range=[start_date, end_date])
    else:
        hasil_surveys = Responden.objects.all()
    return render(request, 'admin-dashboard/hasilsurvey.html', {'hasil_surveys': hasil_surveys})

def isi_kusioner(request):
    if request.method == 'POST':
        jenis_layanan_id = request.POST.get('jenis_layanan')
        layanan = Layanan.objects.get(id=jenis_layanan_id)
        responden = Responden.objects.create(
            nama=request.POST.get('nama'),
            jenis_kelamin=request.POST.get('jenis_kelamin'),
            email=request.POST.get('email'),
            no_telepon=request.POST.get('no_telepon'),
            nopol_kendaraan=request.POST.get('nopol_kendaraan'),
            jenis_layanan=layanan.nama_layanan,
        )
        for key, value in request.POST.items():
            if key.startswith('rating_'):
                question_id = key.split('_')[1]
                pertanyaan = Kuesioner.objects.get(id=question_id)
                JawabanKuesioner.objects.create(
                    responden=responden,
                    pertanyaan=pertanyaan,
                    jawaban=value
                )
        return redirect('hasil_survey')
    else:
        daftar_pertanyaan = Kuesioner.objects.all()
        jenis_layanan = Layanan.objects.all()
        return render(request, 'user/kuesioner.html', {'daftar_pertanyaan': daftar_pertanyaan, 'jenis_layanan': jenis_layanan})

def layanan_list(request):
    layanan = Layanan.objects.all()
    return render(request, 'admin-dashboard/layanan.html', {'layanan': layanan})

def layanan_create(request):
    if request.method == 'POST':
        form = LayananForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('layanan_list')
    else:
        form = LayananForm()
    return render(request, 'admin-dashboard/layanan_form.html', {'form': form})

def layanan_update(request, pk):
    layanan = get_object_or_404(Layanan, pk=pk)
    if request.method == 'POST':
        form = LayananForm(request.POST, instance=layanan)
        if form.is_valid():
            form.save()
            return redirect('layanan_list')
    else:
        form = LayananForm(instance=layanan)
    return render(request, 'admin-dashboard/layanan_form.html', {'form': form})

def layanan_delete(request, pk):
    layanan = get_object_or_404(Layanan, pk=pk)
    if request.method == 'POST':
        layanan.delete()
        return redirect('layanan_list')
    return render(request, 'admin-dashboard/layanan_confirm_delete.html', {'layanan': layanan})