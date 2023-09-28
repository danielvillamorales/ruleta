from django.shortcuts import render, redirect, get_object_or_404
from sorteo.models import Ruleta , DiasFecha
from sorteo.forms import RuletaForm
from django.http import HttpResponse
from django.db.models import Q
from django.urls import reverse
from datetime import date
from django.contrib import messages
from io import BytesIO
import xlwt

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
                24:'15%',
                25:'20%',
                26:'15%',
                27:'20%',
                28:'25%',
                29:'30%',
                30:'25%',
                31:'35%',
                32:'30%',
                33:'15%',
                34:'20%',
                35:'25%',
                36:'30%',
                37:'15%',
                38:'20%',
                39:'25%',
                40:'40%',
                41:'15%',
                42:'20%',
                43:'25%',
                44:'30%',
                45:'15%',
                46:'20%',
                47:'25%',
                48:'30%',                
                49:'45%',
                50:'50%',}

valor_premio2 = {1:'40%',
                2:'30%',
                3:'30%',
                4:'30%',
                5:'35%',
                6:'30%',
                7:'35%',
                8:'30%',
                9:'35%',
                10:'30%',
                11:'30%',
                12:'30%',
                13:'30%',
                14:'35%',
                15:'30%',
                16:'30%',
                17:'30%',
                18:'35%',
                19:'40%',
                20:'30%',
                21:'30%',
                22:'35%',
                23:'30%',
                24:'30%',
                25:'35%',
                26:'30%',
                27:'30%',
                28:'35%',
                29:'30%',
                30:'30%',
                31:'30%',
                32:'35%',
                33:'30%',
                34:'30%',
                35:'30%',
                36:'30%',
                37:'35%',
                38:'30%',
                39:'30%',
                40:'30%',
                41:'35%',
                42:'30%',
                43:'30%',
                44:'35%',
                45:'30%',
                46:'30%',
                47:'40%',
                48:'30%',                
                49:'30%',
                50:'35%',
                51:'35%',
                52:'35%',
                53:'40%',
                54:'30%',
                55:'30%',
                56:'30%',
                57:'30%',
                58:'30%',
                59:'35%',
                60:'30%',
                61:'35%',
                62:'30%',
                63:'35%',
                64:'30%',
                65:'30%',
                66:'30%',
                67:'30%',
                68:'35%',
                69:'30%',
                70:'30%',
                71:'35%',
                72:'30%',
                73:'30%',
                74:'35%',
                75:'30%',
                76:'30%',
                77:'30%',
                78:'35%',
                79:'45%',
                80:'50%',}

# Create your views here.
def ruleta(request, pk):
    print(pk)
    cliente = get_object_or_404(Ruleta, pk=pk)
    fecha_promo = DiasFecha.objects.filter(fecha=date.today())
    es_promo = 1 if len(fecha_promo) > 0 else 0
    print(cliente)
    return render(request, 'ruleta.html', {'cliente' : cliente, 'es_promo': es_promo})


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
                fecha_promo = DiasFecha.objects.filter(fecha=date.today())
                cliente = form.save(commit=False)
                cliente.consecutivo = cliente.get_next_consecutivo()
                cliente.porcentaje = valor_premio2[cliente.consecutivo] if len(fecha_promo) > 0 else  valor_premio[cliente.consecutivo]
                print(cliente)
                cliente.save()
                return redirect('ruleta', cliente.id)
    return render(request , 'registro.html')


def consultar_ganador(request):
    if request.method == 'POST':
        cedula = request.POST.get('cedula')
        cliente_obj = Ruleta.objects.filter(Q(cedula=cedula) | Q(nombre__icontains=cedula), fecha=date.today())
        if len(cliente_obj)>0:
            return render(request, 'consultac.html', {'clientes' : cliente_obj})
        else:
            messages.error(request, 'No se ha encontrado un ganador con esa cédula el dia de hoy')
            return redirect('consultar_ganador')
    return render(request, 'consultac.html')


def exportar_sorteos(request):
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Sorteos')
    font_style = xlwt.XFStyle()
    columns = ['id','cedula','nombre','fecha_nacimeinto','correo','fecha_digitado','porcetaje','consecutivo','telefono']
    row_num = 0
    [ws.write(row_num, col_num, column, font_style) for col_num, column in enumerate(columns)]
    rows = Ruleta.objects.all().values_list('id','cedula','nombre','fecha_nacimiento','correo','fecha','porcentaje','consecutivo','telefono')
    for row_num, row in enumerate(rows, start=1):
        for col_num, cell in enumerate(row):
            if isinstance(cell, date):
                ws.write(row_num, col_num, cell.strftime('%Y-%m-%d'), font_style)
            else:
                ws.write(row_num, col_num, cell, font_style)
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=Sorteos.xls'
    output = BytesIO()
    wb.save(output)
    output.seek(0)
    response.write(output.getvalue())
    return response