from rest_framework import serializers
from .models import *

# ─────────────────────────────────────────────
#  SEGURIDAD
# ─────────────────────────────────────────────

class RolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rol
        fields = "__all__"


class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    rol_detalle = RolSerializer(source='rol', read_only=True)

    class Meta:
        model = CustomUser
        fields = (
            "id", "username", "password", "first_name", "last_name", 
            "email", "rol", "rol_detalle", "activo"
        )
        extra_kwargs = {
            'email': {'required': True},
            'username': {'required': False},
        }

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = CustomUser(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance


class PersonaSerializer(serializers.ModelSerializer):
    usuario = CustomUserSerializer()

    class Meta:
        model = Persona
        fields = ["id", "nombre", "apellido_paterno", "apellido_materno", "dni",
                 "fecha_nacimiento", "genero", "nacionalidad", "telefono", 
                 "usuario", "activo"]

    def create(self, validated_data):
        user_data = validated_data.pop("usuario")
        user = CustomUserSerializer().create(user_data)
        persona = Persona.objects.create(usuario=user, **validated_data)
        return persona

    def update(self, instance, validated_data):
        user_data = validated_data.pop("usuario", None)
        if user_data:
            user_serializer = CustomUserSerializer()
            user_serializer.update(instance.usuario, user_data)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class LogProcesosSerializer(serializers.ModelSerializer):
    usuario_detalle = CustomUserSerializer(source='usuario', read_only=True)

    class Meta:
        model = LogProcesos
        fields = ["id", "fecha", "accion", "usuario", "usuario_detalle"]


# ─────────────────────────────────────────────
#  Estructura académica
# ─────────────────────────────────────────────

class UniversidadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Universidad
        fields = "__all__"


class FacultadSerializer(serializers.ModelSerializer):
    universidad = serializers.PrimaryKeyRelatedField(queryset=Universidad.objects.all())
    universidad_detalle = UniversidadSerializer(source='universidad', read_only=True)

    class Meta:
        model = Facultad
        fields = ['id', 'nombre', 'descripcion', 'activo', 'universidad', 'universidad_detalle']


class DepartamentoSerializer(serializers.ModelSerializer):
    facultad = serializers.PrimaryKeyRelatedField(queryset=Facultad.objects.all())
    facultad_detalle = FacultadSerializer(source='facultad', read_only=True)

    class Meta:
        model = Departamento
        fields = ['id', 'nombre', 'activo', 'facultad', 'facultad_detalle']
        

class CarreraSerializer(serializers.ModelSerializer):
    departamento = serializers.PrimaryKeyRelatedField(queryset=Departamento.objects.all())
    departamento_detalle = DepartamentoSerializer(source='departamento', read_only=True)

    class Meta:
        model = Carrera
        fields = ['id', 'nombre', 'activo', 'departamento', 'departamento_detalle']


# ─────────────────────────────────────────────
#  Planes de estudio y periodos
# ─────────────────────────────────────────────

class PlanCurricularSerializer(serializers.ModelSerializer):
    carrera = serializers.PrimaryKeyRelatedField(queryset=Carrera.objects.all())
    carrera_detalle = CarreraSerializer(source='carrera', read_only=True)

    class Meta:
        model = PlanCurricular
        fields = ['id', 'tag', 'activo', 'fecha_culminacion', 'carrera', 'carrera_detalle']


class SemestreAcademicoSerializer(serializers.ModelSerializer):
    class Meta:
        model = SemestreAcademico
        fields = "__all__"


class SemestrePlanSerializer(serializers.ModelSerializer):
    plan = serializers.PrimaryKeyRelatedField(queryset=PlanCurricular.objects.all())
    plan_detalle = PlanCurricularSerializer(source='plan', read_only=True)
    semestre_academico = serializers.PrimaryKeyRelatedField(queryset=SemestreAcademico.objects.all())
    semestre_academico_detalle = SemestreAcademicoSerializer(source='semestre_academico', read_only=True)

    class Meta:
        model = SemestrePlan
        fields = ['id', 'nombre', 'detalles', 'activo', 'plan', 'plan_detalle',
                 'semestre_academico', 'semestre_academico_detalle']


# ─────────────────────────────────────────────
#  Cursos y prerrequisitos
# ─────────────────────────────────────────────

class AreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Area
        fields = "__all__"


class TipoCursoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoCurso
        fields = "__all__"


class CursoSerializer(serializers.ModelSerializer):
    area = serializers.PrimaryKeyRelatedField(queryset=Area.objects.all())
    area_detalle = AreaSerializer(source='area', read_only=True)
    
    tipo_curso = serializers.PrimaryKeyRelatedField(queryset=TipoCurso.objects.all())
    tipo_curso_detalle = TipoCursoSerializer(source='tipo_curso', read_only=True)
    
    semestre = serializers.PrimaryKeyRelatedField(queryset=SemestrePlan.objects.all())
    semestre_detalle = SemestrePlanSerializer(source='semestre', read_only=True)
    
    prerrequisitos = serializers.PrimaryKeyRelatedField(
        queryset=Curso.objects.all(), many=True, write_only=True
    )
    prerrequisitos_detalle = serializers.StringRelatedField(
        many=True, source='prerrequisitos', read_only=True
    )

    class Meta:
        model = Curso
        fields = ['id', 'nombre', 'codigo', 'descripcion', 'horas_teoria',
                  'horas_practica', 'horas_laboratorio', 'horas_teopra',
                  'creditos', 'horas_totales', 'activo', 
                  'area', 'area_detalle', 'tipo_curso', 'tipo_curso_detalle',
                  'semestre', 'semestre_detalle',
                  'prerrequisitos', 'prerrequisitos_detalle']


# ─────────────────────────────────────────────
#  Profesores y carga académica
# ─────────────────────────────────────────────

class ProfesionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profesion
        fields = "__all__"


class ProfesorSerializer(serializers.ModelSerializer):
    persona = PersonaSerializer()
    profesion_detalle = ProfesionSerializer(source='profesion', read_only=True)

    class Meta:
        model = Profesor
        fields = ["id", "persona", "profesion", "profesion_detalle", "activo"]

    def create(self, validated_data):
        persona_data = validated_data.pop("persona")
        persona = PersonaSerializer().create(persona_data)
        profesor = Profesor.objects.create(persona=persona, **validated_data)
        return profesor

    def update(self, instance, validated_data):
        persona_data = validated_data.pop("persona", None)
        if persona_data:
            persona_serializer = PersonaSerializer()
            persona_serializer.update(instance.persona, persona_data)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class CargaCursoSerializer(serializers.ModelSerializer):
    profesor = serializers.PrimaryKeyRelatedField(queryset=Profesor.objects.all())
    profesor_detalle = ProfesorSerializer(source='profesor', read_only=True)
    curso = serializers.PrimaryKeyRelatedField(queryset=Curso.objects.all())
    curso_detalle = CursoSerializer(source='curso', read_only=True)

    class Meta:
        model = CargaCurso
        fields = ["id", "profesor", "profesor_detalle", "curso", "curso_detalle", 
                 "detalles", "activo"]


class GrupoSerializer(serializers.ModelSerializer):
    curso = serializers.PrimaryKeyRelatedField(queryset=Curso.objects.all())
    curso_detalle = CursoSerializer(source='curso', read_only=True)

    class Meta:
        model = Grupo
        fields = ["id", "nombre", "codigo", "curso", "curso_detalle", "activo"]


# ─────────────────────────────────────────────
#  Estudiantes
# ─────────────────────────────────────────────

class EstudianteSerializer(serializers.ModelSerializer):
    persona = PersonaSerializer()

    class Meta:
        model = Estudiante
        fields = ["id", "persona", "fecha_creacion", "activo"]

    def create(self, validated_data):
        persona_data = validated_data.pop("persona")
        persona = PersonaSerializer().create(persona_data)
        estudiante = Estudiante.objects.create(persona=persona, **validated_data)
        return estudiante

    def update(self, instance, validated_data):
        persona_data = validated_data.pop("persona", None)
        if persona_data:
            persona_serializer = PersonaSerializer()
            persona_serializer.update(instance.persona, persona_data)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


# ─────────────────────────────────────────────
#  Modelos complementarios para el sílabo
# ─────────────────────────────────────────────

class PeriodoLectivoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PeriodoLectivo
        fields = "__all__"


class MetodologiaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Metodologia
        fields = "__all__"


class BibliografiaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bibliografia
        fields = "__all__"


class SemanaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Semana
        fields = "__all__"


class ContenidoEspecificoSerializer(serializers.ModelSerializer):
    semana = serializers.PrimaryKeyRelatedField(queryset=Semana.objects.all())
    semana_detalle = SemanaSerializer(source='semana', read_only=True)

    class Meta:
        model = ContenidoEspecifico
        fields = ["id", "contenido", "activo", "semana", "semana_detalle"]


class UnidadSerializer(serializers.ModelSerializer):
    metodologia = serializers.CharField()  # Como es TextField en el modelo
    silabo = serializers.PrimaryKeyRelatedField(queryset=Silabo.objects.all())
    silabo_detalle = serializers.StringRelatedField(source='silabo', read_only=True)

    class Meta:
        model = Unidad
        fields = ["id", "numero", "inicio", "final", "descripcion", "metodologia", 
                 "activo", "silabo", "silabo_detalle"]


class ActividadSerializer(serializers.ModelSerializer):
    silabo = serializers.PrimaryKeyRelatedField(queryset=Silabo.objects.all())
    silabo_detalle = serializers.StringRelatedField(source='silabo', read_only=True)

    class Meta:
        model = Actividad
        fields = ["id", "nombre", "descripcion", "activo", "silabo", "silabo_detalle"]


class CriterioEvaluacionSerializer(serializers.ModelSerializer):
    silabo = serializers.PrimaryKeyRelatedField(queryset=Silabo.objects.all())
    silabo_detalle = serializers.StringRelatedField(source='silabo', read_only=True)

    class Meta:
        model = CriterioEvaluacion
        fields = ["id", "nombre", "peso", "fecha_inicio", "fecha_fin", 
                 "descripcion", "activo", "silabo", "silabo_detalle"]


# ─────────────────────────────────────────────
#  Silabos
# ─────────────────────────────────────────────

class SilaboSerializer(serializers.ModelSerializer):
    periodo_lectivo = serializers.PrimaryKeyRelatedField(queryset=PeriodoLectivo.objects.all())
    periodo_lectivo_detalle = PeriodoLectivoSerializer(source='periodo_lectivo', read_only=True)

    profesor = serializers.PrimaryKeyRelatedField(queryset=Profesor.objects.all())
    profesor_detalle = ProfesorSerializer(source='profesor', read_only=True)

    facultad = serializers.PrimaryKeyRelatedField(queryset=Facultad.objects.all())
    facultad_detalle = FacultadSerializer(source='facultad', read_only=True)

    carrera = serializers.PrimaryKeyRelatedField(queryset=Carrera.objects.all())
    carrera_detalle = CarreraSerializer(source='carrera', read_only=True)

    curso = serializers.PrimaryKeyRelatedField(queryset=Curso.objects.all())
    curso_detalle = CursoSerializer(source='curso', read_only=True)

    # Campos de solo lectura para las relaciones inversas

    class Meta:
        model = Silabo
        fields = [
            "id", "nombre", "competencia_curso", "competencia_perfil_egreso", 
            "competencia_profesional", "sumilla", "fecha_creacion", 
            "fecha_modificacion", "activo",
            "periodo_lectivo", "periodo_lectivo_detalle",
            "profesor", "profesor_detalle",
            "facultad", "facultad_detalle",
            "carrera", "carrera_detalle",
            "curso", "curso_detalle"
        ]
        read_only_fields = ["fecha_creacion", "fecha_modificacion"]