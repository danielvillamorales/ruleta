from django.shortcuts import render, redirect, get_object_or_404
from sorteo.models import Ruleta
from sorteo.forms import RuletaForm
from django.urls import reverse
from datetime import date
from django.contrib import messages

valor_premio = {1:'30%',
                2:'15%',
                3:'40%',
                4:'15%',
                5:'35%',
                6:'20%',
                7:'15%',
                8:'20%',
                9:'25%',
                10:'20%',
                11:'15%',
                12:'20%',
                13:'15%',
                14:'15%',
                15:'25%',
                16:'35%',
                17:'30%',
                18:'40%',
                19:'15%',
                20:'20%',
                21:'15%',
                22:'30%',
                23:'20%',
                24:'45%',
                25:'50%',}

# Create your views here.
def ruleta(request, pk):
    print(pk)
    cliente = get_object_or_404(Ruleta, pk=pk)
    print(cliente)
    return render(request, 'ruleta.html', {'cliente' : cliente})


def registro(request):
    if request.method == 'POST':
        form = RuletaForm(request.POST)
        if form.is_valid():
            try:
                cliente_obj = Ruleta.objects.get(cedula=form.cleaned_data['cedula'], fecha=date.today())
                if cliente_obj:
                    messages.error(request, 'Ya se ha registrado un usuario con esa cédula el dia de hoy')
                    return redirect('registro')
            except:
                cliente = form.save(commit=False)
                cliente.consecutivo = cliente.get_next_consecutivo()
                cliente.porcentaje = valor_premio[cliente.consecutivo]
                print(cliente)
                cliente.save()
                return redirect('ruleta', cliente.id)
    return render(request , 'registro.html')


def consultar_ganador(request):
    if request.method == 'POST':
        cedula = request.POST.get('cedula')
        try:
            cliente_obj = Ruleta.objects.get(cedula=cedula, fecha=date.today())
            if cliente_obj:
                return render(request, 'consultac.html', {'cliente' : cliente_obj})
        except:
            messages.error(request, 'No se ha encontrado un ganador con esa cédula el dia de hoy')
            return redirect('consultar_ganador')

    return render(request, 'consultac.html')