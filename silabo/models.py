from django.db import models
from django.contrib.auth.models import AbstractUser

# ─────────────────────────────────────────────
#  SEGURIDAD Y USUARIOS
# ─────────────────────────────────────────────

class Rol(models.Model):
    nombre = models.CharField(max_length=200)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)

    rol = models.ForeignKey(Rol, on_delete=models.SET_NULL, null=True, related_name="usuarios")
    activo = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'  # <-- ESTA LÍNEA ES CLAVE
    REQUIRED_FIELDS = ['username']  # Solo si aún quieres que username exista

    def __str__(self):
        return self.email


class Persona(models.Model):
    nombre = models.CharField(max_length=200)
    apellido_paterno = models.CharField(max_length=200)
    apellido_materno = models.CharField(max_length=200)
    dni = models.CharField(max_length=8)
    fecha_nacimiento = models.DateField()
    genero = models.CharField(max_length=1, choices=[("M", "Masculino"), ("F", "Femenino")])
    nacionalidad = models.CharField(max_length=50)
    telefono = models.CharField(max_length=20, blank=True)
    usuario = models.OneToOneField(CustomUser, on_delete=models.SET_NULL, null=True, related_name="persona")
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.apellido_paterno} {self.apellido_materno}, {self.nombre}"


class LogProcesos(models.Model):
    fecha = models.DateField()
    accion = models.TextField()
    usuario = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name="logs")

    def __str__(self):
        return f"{self.fecha} - {self.accion[:50]}"


# ─────────────────────────────────────────────
#  PROFESIONES Y PROFESORES
# ─────────────────────────────────────────────

class Profesion(models.Model):
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField(blank=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre


class Profesor(models.Model):
    persona = models.OneToOneField(Persona, on_delete=models.CASCADE, related_name="profesor")
    profesion = models.ForeignKey(Profesion, on_delete=models.SET_NULL, null=True, blank=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return str(self.persona)


# ─────────────────────────────────────────────
#  ESTUDIANTES
# ─────────────────────────────────────────────

class Estudiante(models.Model):
    persona = models.OneToOneField(Persona, on_delete=models.CASCADE, related_name="estudiante")
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return str(self.persona)


# ─────────────────────────────────────────────
#  ESTRUCTURA ACADÉMICA
# ─────────────────────────────────────────────

class Universidad(models.Model):
    nombre = models.CharField(max_length=200)
    direccion = models.CharField(max_length=100, blank=True)
    acronimo = models.CharField(max_length=50, blank=True)
    descripcion = models.TextField(blank=True)
    url = models.URLField(blank=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre


class Facultad(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True)
    universidad = models.ForeignKey(Universidad, on_delete=models.SET_NULL, null=True, related_name="facultades")
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre


class Departamento(models.Model):
    nombre = models.CharField(max_length=200)
    facultad = models.ForeignKey(Facultad, on_delete=models.SET_NULL, null=True, related_name="departamentos")
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre


class Carrera(models.Model):
    nombre = models.CharField(max_length=200)
    departamento = models.ForeignKey(Departamento, on_delete=models.SET_NULL, null=True, related_name="carreras")
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre


# ─────────────────────────────────────────────
#  PLANES DE ESTUDIO Y PERIODOS
# ─────────────────────────────────────────────

class PlanCurricular(models.Model):
    tag = models.CharField(max_length=255)
    carrera = models.ForeignKey(Carrera, on_delete=models.SET_NULL, null=True, related_name="planes")
    fecha_culminacion = models.DateField(null=True, blank=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.carrera} - {self.tag}"


class SemestreAcademico(models.Model):
    nombre = models.CharField(max_length=255)
    anio_academico = models.PositiveSmallIntegerField()
    periodo = models.CharField(max_length=100)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    semanas = models.PositiveSmallIntegerField()
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return f"{self.nombre} ({self.periodo})"


class SemestrePlan(models.Model):
    nombre = models.CharField(max_length=50)
    detalles = models.CharField(max_length=200)
    plan = models.ForeignKey(PlanCurricular, on_delete=models.SET_NULL, null=True, related_name="semestres")
    semestre_academico = models.ForeignKey(SemestreAcademico, on_delete=models.SET_NULL, null=True, related_name="semestres")
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.plan} - {self.nombre}"


class PeriodoLectivo(models.Model):
    periodo = models.CharField(max_length=40)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.periodo


# ─────────────────────────────────────────────
#  CURSOS Y PRERREQUISITOS
# ─────────────────────────────────────────────

class Area(models.Model):
    codigo = models.CharField(max_length=10, unique=True)
    nombre = models.CharField(max_length=100)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre


class TipoCurso(models.Model):
    nombre = models.CharField(max_length=300)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre


class Curso(models.Model):
    codigo = models.CharField(max_length=100, unique=True)
    nombre = models.CharField(max_length=300)
    descripcion = models.TextField(blank=True)
    horas_teoria = models.PositiveSmallIntegerField()
    horas_practica = models.PositiveSmallIntegerField()
    horas_laboratorio = models.PositiveSmallIntegerField()
    horas_teopra = models.PositiveSmallIntegerField(default=0)
    creditos = models.PositiveSmallIntegerField()
    tipo_curso = models.ForeignKey(TipoCurso, on_delete=models.SET_NULL, null=True, related_name="cursos")
    area = models.ForeignKey(Area, on_delete=models.SET_NULL, null=True, related_name="cursos")
    semestre = models.ForeignKey(SemestrePlan, on_delete=models.SET_NULL, null=True, related_name="cursos")
    prerrequisitos = models.ManyToManyField("self", symmetrical=False, blank=True, related_name="requeridos_por")
    activo = models.BooleanField(default=True)

    @property
    def horas_totales(self):
        return self.horas_teoria + self.horas_practica + self.horas_laboratorio + self.horas_teopra

    def __str__(self):
        return f"{self.codigo} - {self.nombre}"


# ─────────────────────────────────────────────
#  CARGA ACADÉMICA Y GRUPOS
# ─────────────────────────────────────────────

class CargaCurso(models.Model):
    profesor = models.ForeignKey(Profesor, on_delete=models.SET_NULL, null=True, related_name="cargas")
    curso = models.ForeignKey(Curso, on_delete=models.SET_NULL, null=True, related_name="cargas")
    detalles = models.CharField(max_length=100, blank=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.curso} - {self.profesor}"


class Grupo(models.Model):
    nombre = models.CharField(max_length=30)
    codigo = models.PositiveIntegerField()
    curso = models.ForeignKey(Curso, on_delete=models.SET_NULL, null=True, related_name="grupos")
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nombre} ({self.curso})"


# ─────────────────────────────────────────────
#  METODOLOGÍA
# ─────────────────────────────────────────────

class Metodologia(models.Model):
    tipo = models.CharField(max_length=60)
    descripcion = models.TextField()
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.tipo


# ─────────────────────────────────────────────
#  SÍLABOS (DEBE IR ANTES DE LOS MODELOS QUE LO REFERENCIAN)
# ─────────────────────────────────────────────

class Silabo(models.Model):
    nombre = models.CharField(max_length=250, null=True)
    periodo_lectivo = models.ForeignKey(PeriodoLectivo, on_delete=models.CASCADE, related_name="silabos")
    competencia_curso = models.TextField(null=True)
    competencia_perfil_egreso = models.TextField(null=True)
    competencia_profesional = models.TextField(null=True)
    sumilla = models.TextField(null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    profesor = models.ForeignKey(Profesor, on_delete=models.CASCADE, related_name="silabos")
    facultad = models.ForeignKey(Facultad, on_delete=models.CASCADE, related_name="silabos")
    carrera = models.ForeignKey(Carrera, on_delete=models.CASCADE, related_name="silabos")
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name="silabos")
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f"Silabo {self.periodo_lectivo} - {self.curso}"


# ─────────────────────────────────────────────
#  UNIDADES Y CONTENIDO ACADÉMICO
# ─────────────────────────────────────────────

class Unidad(models.Model):
    numero = models.PositiveSmallIntegerField(null=True)
    inicio = models.DateField()
    final = models.DateField()
    descripcion = models.TextField()
    metodologia = models.TextField()
    silabo = models.ForeignKey(Silabo, on_delete=models.SET_NULL, null=True, related_name="unidades")
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.descripcion[:50]


class Bibliografia(models.Model):
    autor = models.CharField(max_length=120)
    libro = models.CharField(max_length=160)
    fecha = models.DateField()
    link = models.URLField(blank=True)
    nombre = models.CharField(max_length=160, blank=True)
    unidad = models.ForeignKey(Unidad, on_delete=models.SET_NULL, null=True, related_name="bibliografias")
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.libro


class Semana(models.Model):
    numero = models.PositiveSmallIntegerField()
    unidad = models.ForeignKey(Unidad, on_delete=models.SET_NULL, null=True, related_name="semanas")
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f"Semana {self.numero}"


class ContenidoEspecifico(models.Model):
    contenido = models.TextField()
    semana = models.ForeignKey(Semana, on_delete=models.SET_NULL, null=True, related_name="contenidos")
    activo = models.BooleanField(default=True)
    
    def __str__(self):
        return f"Contenido especifico {self.contenido[:50]}"


# ─────────────────────────────────────────────
#  ACTIVIDADES Y EVALUACIÓN
# ─────────────────────────────────────────────

class Actividad(models.Model):
    nombre = models.CharField(max_length=120)
    descripcion = models.TextField()
    silabo = models.ForeignKey(Silabo, on_delete=models.SET_NULL, null=True, related_name="actividades")
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre


class CriterioEvaluacion(models.Model):
    nombre = models.CharField(max_length=120)
    peso = models.FloatField()
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    descripcion = models.TextField()
    silabo = models.ForeignKey(Silabo, on_delete=models.SET_NULL, null=True, related_name="criterios_evaluacion")
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre