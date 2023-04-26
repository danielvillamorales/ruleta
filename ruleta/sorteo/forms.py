from django.forms import ModelForm
from sorteo.models import Ruleta


class RuletaForm(ModelForm):
    class Meta:
        model = Ruleta
        fields = ('cedula', 'nombre', 'telefono', 'fecha_nacimiento', 'correo', 'terminos')