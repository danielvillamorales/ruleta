from django.db import models
from django.db.models import Max
from datetime import date

class DiasFecha(models.Model):
    fecha = models.DateField(null=False)

    def __str__(self):
        return f'{self.fecha}'

# Create your models here.
class Ruleta(models.Model):
    cedula = models.CharField(max_length=100)
    nombre = models.CharField(max_length=100, null=False)
    fecha_nacimiento = models.DateField(null=False)
    correo = models.EmailField()
    telefono = models.CharField(max_length=100, null=False)
    fecha = models.DateField(auto_now_add=True)
    porcentaje = models.CharField(max_length=4, null=True)
    consecutivo = models.IntegerField()
    terminos = models.BooleanField(default=True)

    class Meta:
        unique_together = ('cedula', 'fecha')

    def __str__(self):
        return f'{self.cedula} - {self.nombre} - {self.fecha_nacimiento} - {self.correo} - {self.fecha} - {self.porcentaje} - {self.consecutivo}'
    
    def get_next_consecutivo(self):
        # Obtener el último registro agregado a la tabla Ruleta
        try:
            last_record = Ruleta.objects.latest('id')
            last_fecha = DiasFecha.objects.filter(fecha=date.today())
            # Reiniciar el consecutivo si es mayor que 20 o si no hay registros en la tabla Ruleta
            if last_record.consecutivo >= 80 if len(last_fecha) > 0 else 50:
                return 1
            else:
                return last_record.consecutivo + 1
        except:
            return 1