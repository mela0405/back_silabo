from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from .models import *
from .serializers import *


# ─────────────────────────────────────────────
#  SEGURIDAD
# ─────────────────────────────────────────────

class RolViewSet(viewsets.ModelViewSet):
    """
    CRUD completo para roles del sistema
    """
    queryset = Rol.objects.all()
    serializer_class = RolSerializer


class CustomUserViewSet(viewsets.ModelViewSet):
    """
    CRUD completo para usuarios del sistema
    """
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

    @action(detail=True, methods=['post'])
    def cambiar_password(self, request, pk=None):
        """
        Endpoint personalizado para cambiar contraseña
        """
        user = self.get_object()
        password = request.data.get('password')
        
        if password:
            user.set_password(password)
            user.save()
            return Response({'message': 'Contraseña actualizada correctamente'})
        else:
            return Response(
                {'error': 'Password es requerido'}, 
                status=status.HTTP_400_BAD_REQUEST
            )


class PersonaViewSet(viewsets.ModelViewSet):
    """
    CRUD completo para personas
    """
    queryset = Persona.objects.all()
    serializer_class = PersonaSerializer

    @action(detail=False, methods=['get'])
    def buscar_por_dni(self, request):
        """
        Buscar persona por DNI
        """
        dni = request.query_params.get('dni')
        if dni:
            persona = get_object_or_404(Persona, dni=dni)
            serializer = self.get_serializer(persona)
            return Response(serializer.data)
        else:
            return Response(
                {'error': 'DNI es requerido'}, 
                status=status.HTTP_400_BAD_REQUEST
            )


class LogProcesosViewSet(viewsets.ModelViewSet):
    """
    CRUD completo para logs del sistema
    """
    queryset = LogProcesos.objects.all().order_by('-fecha')
    serializer_class = LogProcesosSerializer


# ─────────────────────────────────────────────
#  Estructura académica
# ─────────────────────────────────────────────

class UniversidadViewSet(viewsets.ModelViewSet):
    """
    CRUD completo para universidades
    """
    queryset = Universidad.objects.all()
    serializer_class = UniversidadSerializer

    @action(detail=True, methods=['get'])
    def facultades(self, request, pk=None):
        """
        Obtener todas las facultades de una universidad
        """
        universidad = self.get_object()
        facultades = universidad.facultades.filter(activo=True)
        serializer = FacultadSerializer(facultades, many=True)
        return Response(serializer.data)


class FacultadViewSet(viewsets.ModelViewSet):
    """
    CRUD completo para facultades
    """
    queryset = Facultad.objects.all()
    serializer_class = FacultadSerializer

    @action(detail=True, methods=['get'])
    def departamentos(self, request, pk=None):
        """
        Obtener todos los departamentos de una facultad
        """
        facultad = self.get_object()
        departamentos = facultad.departamentos.filter(activo=True)
        serializer = DepartamentoSerializer(departamentos, many=True)
        return Response(serializer.data)


class DepartamentoViewSet(viewsets.ModelViewSet):
    """
    CRUD completo para departamentos
    """
    queryset = Departamento.objects.all()
    serializer_class = DepartamentoSerializer

    @action(detail=True, methods=['get'])
    def carreras(self, request, pk=None):
        """
        Obtener todas las carreras de un departamento
        """
        departamento = self.get_object()
        carreras = departamento.carreras.filter(activo=True)
        serializer = CarreraSerializer(carreras, many=True)
        return Response(serializer.data)


class CarreraViewSet(viewsets.ModelViewSet):
    """
    CRUD completo para carreras
    """
    queryset = Carrera.objects.all()
    serializer_class = CarreraSerializer

    @action(detail=True, methods=['get'])
    def planes_curriculares(self, request, pk=None):
        """
        Obtener todos los planes curriculares de una carrera
        """
        carrera = self.get_object()
        planes = carrera.planes.filter(activo=True)
        serializer = PlanCurricularSerializer(planes, many=True)
        return Response(serializer.data)


# ─────────────────────────────────────────────
#  Planes de estudio y periodos
# ─────────────────────────────────────────────

class PlanCurricularViewSet(viewsets.ModelViewSet):
    """
    CRUD completo para planes curriculares
    """
    queryset = PlanCurricular.objects.all()
    serializer_class = PlanCurricularSerializer

    @action(detail=True, methods=['get'])
    def semestres(self, request, pk=None):
        """
        Obtener todos los semestres de un plan curricular
        """
        plan = self.get_object()
        semestres = plan.semestres.filter(activo=True)
        serializer = SemestrePlanSerializer(semestres, many=True)
        return Response(serializer.data)


class SemestreAcademicoViewSet(viewsets.ModelViewSet):
    """
    CRUD completo para semestres académicos
    """
    queryset = SemestreAcademico.objects.all()
    serializer_class = SemestreAcademicoSerializer


class SemestrePlanViewSet(viewsets.ModelViewSet):
    """
    CRUD completo para semestres de plan
    """
    queryset = SemestrePlan.objects.all()
    serializer_class = SemestrePlanSerializer

    @action(detail=True, methods=['get'])
    def cursos(self, request, pk=None):
        """
        Obtener todos los cursos de un semestre
        """
        semestre = self.get_object()
        cursos = semestre.cursos.filter(activo=True)
        serializer = CursoSerializer(cursos, many=True)
        return Response(serializer.data)


# ─────────────────────────────────────────────
#  Cursos y prerrequisitos
# ─────────────────────────────────────────────

class AreaViewSet(viewsets.ModelViewSet):
    """
    CRUD completo para áreas
    """
    queryset = Area.objects.all()
    serializer_class = AreaSerializer

    @action(detail=True, methods=['get'])
    def cursos(self, request, pk=None):
        """
        Obtener todos los cursos de un área
        """
        area = self.get_object()
        cursos = area.cursos.filter(activo=True)
        serializer = CursoSerializer(cursos, many=True)
        return Response(serializer.data)


class TipoCursoViewSet(viewsets.ModelViewSet):
    """
    CRUD completo para tipos de curso
    """
    queryset = TipoCurso.objects.all()
    serializer_class = TipoCursoSerializer


class CursoViewSet(viewsets.ModelViewSet):
    """
    CRUD completo para cursos:
    - GET    /cursos/          → lista
    - POST   /cursos/          → crear
    - GET    /cursos/{id}/     → detalle
    - PUT    /cursos/{id}/     → actualizar
    - PATCH  /cursos/{id}/     → actualización parcial
    - DELETE /cursos/{id}/     → eliminar
    """
    queryset = Curso.objects.all()
    serializer_class = CursoSerializer

    @action(detail=True, methods=['get'])
    def prerrequisitos(self, request, pk=None):
        """
        Obtener prerrequisitos de un curso
        """
        curso = self.get_object()
        prerrequisitos = curso.prerrequisitos.all()
        serializer = CursoSerializer(prerrequisitos, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def cursos_dependientes(self, request, pk=None):
        """
        Obtener cursos que tienen este curso como prerrequisito
        """
        curso = self.get_object()
        cursos_dependientes = curso.requeridos_por.all()
        serializer = CursoSerializer(cursos_dependientes, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def grupos(self, request, pk=None):
        """
        Obtener grupos de un curso
        """
        curso = self.get_object()
        grupos = curso.grupos.filter(activo=True)
        serializer = GrupoSerializer(grupos, many=True)
        return Response(serializer.data)


# ─────────────────────────────────────────────
#  Profesores y carga académica
# ─────────────────────────────────────────────

class ProfesionViewSet(viewsets.ModelViewSet):
    """
    CRUD completo para profesiones
    """
    queryset = Profesion.objects.all()
    serializer_class = ProfesionSerializer


class ProfesorViewSet(viewsets.ModelViewSet):
    """
    CRUD completo para profesores
    """
    queryset = Profesor.objects.all()
    serializer_class = ProfesorSerializer

    @action(detail=True, methods=['get'])
    def cargas(self, request, pk=None):
        """
        Obtener carga académica de un profesor
        """
        profesor = self.get_object()
        cargas = profesor.cargas.filter(activo=True)
        serializer = CargaCursoSerializer(cargas, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def silabos(self, request, pk=None):
        """
        Obtener sílabos creados por un profesor
        """
        profesor = self.get_object()
        silabos = profesor.silabos.filter(activo=True)
        serializer = SilaboSerializer(silabos, many=True)
        return Response(serializer.data)


class CargaCursoViewSet(viewsets.ModelViewSet):
    """
    CRUD completo para carga de cursos
    """
    queryset = CargaCurso.objects.all()
    serializer_class = CargaCursoSerializer


class GrupoViewSet(viewsets.ModelViewSet):
    """
    CRUD completo para grupos
    """
    queryset = Grupo.objects.all()
    serializer_class = GrupoSerializer


# ─────────────────────────────────────────────
#  Estudiantes
# ─────────────────────────────────────────────

class EstudianteViewSet(viewsets.ModelViewSet):
    """
    CRUD completo para estudiantes
    """
    queryset = Estudiante.objects.all()
    serializer_class = EstudianteSerializer

    @action(detail=False, methods=['get'])
    def buscar_por_dni(self, request):
        """
        Buscar estudiante por DNI
        """
        dni = request.query_params.get('dni')
        if dni:
            try:
                persona = Persona.objects.get(dni=dni)
                estudiante = persona.estudiante
                serializer = self.get_serializer(estudiante)
                return Response(serializer.data)
            except (Persona.DoesNotExist, Estudiante.DoesNotExist):
                return Response(
                    {'error': 'Estudiante no encontrado'}, 
                    status=status.HTTP_404_NOT_FOUND
                )
        else:
            return Response(
                {'error': 'DNI es requerido'}, 
                status=status.HTTP_400_BAD_REQUEST
            )


# ─────────────────────────────────────────────
#  Modelos complementarios para el sílabo
# ─────────────────────────────────────────────

class PeriodoLectivoViewSet(viewsets.ModelViewSet):
    """
    CRUD completo para periodos lectivos
    """
    queryset = PeriodoLectivo.objects.all()
    serializer_class = PeriodoLectivoSerializer

    @action(detail=True, methods=['get'])
    def silabos(self, request, pk=None):
        """
        Obtener sílabos de un periodo lectivo
        """
        periodo = self.get_object()
        silabos = periodo.silabos.filter(activo=True)
        serializer = SilaboSerializer(silabos, many=True)
        return Response(serializer.data)


class MetodologiaViewSet(viewsets.ModelViewSet):
    """
    CRUD completo para metodologías
    """
    queryset = Metodologia.objects.all()
    serializer_class = MetodologiaSerializer


class BibliografiaViewSet(viewsets.ModelViewSet):
    """
    CRUD completo para bibliografías
    """
    queryset = Bibliografia.objects.all()
    serializer_class = BibliografiaSerializer


class SemanaViewSet(viewsets.ModelViewSet):
    """
    CRUD completo para semanas
    """
    queryset = Semana.objects.all()
    serializer_class = SemanaSerializer

    @action(detail=True, methods=['get'])
    def contenidos(self, request, pk=None):
        """
        Obtener contenidos específicos de una semana
        """
        semana = self.get_object()
        contenidos = semana.contenidos.filter(activo=True)
        serializer = ContenidoEspecificoSerializer(contenidos, many=True)
        return Response(serializer.data)


class ContenidoEspecificoViewSet(viewsets.ModelViewSet):
    """
    CRUD completo para contenidos específicos
    """
    queryset = ContenidoEspecifico.objects.all()
    serializer_class = ContenidoEspecificoSerializer


class UnidadViewSet(viewsets.ModelViewSet):
    """
    CRUD completo para unidades.
    """
    serializer_class = UnidadSerializer
    queryset = Unidad.objects.all().order_by('numero')   # orden base

    # ←–– Filtrado global por query param ––→
    def get_queryset(self):
        qs = super().get_queryset().filter(activo=True)  # sólo activas
        silabo_id = self.request.query_params.get('silabo_id')
        if silabo_id:
            qs = qs.filter(silabo_id=silabo_id)
        return qs

    # ←–– Acciones de detalle ––→
    @action(detail=True, methods=['get'])
    def semanas(self, request, pk=None):
        """
        Obtener semanas activas de una unidad, ordenadas por número.
        """
        unidad = self.get_object()
        semanas = unidad.semanas.filter(activo=True).order_by('numero')
        serializer = SemanaSerializer(semanas, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def bibliografias(self, request, pk=None):
        """
        Obtener bibliografías activas de una unidad.
        """
        unidad = self.get_object()
        bibliografias = unidad.bibliografias.filter(activo=True)
        serializer = BibliografiaSerializer(bibliografias, many=True)
        return Response(serializer.data)


class ActividadViewSet(viewsets.ModelViewSet):
    """
    CRUD completo para actividades
    """
    serializer_class = ActividadSerializer
    queryset = Actividad.objects.all().order_by('id')   # orden opcional

    # ←–– Búsqueda por silabo_id ––→
    def get_queryset(self):
        qs = super().get_queryset().filter(activo=True)     # sólo actividades activas
        silabo_id = self.request.query_params.get('silabo_id')
        if silabo_id:
            qs = qs.filter(silabo_id=silabo_id)
        return qs

    def create(self, request, *args, **kwargs):
        """
        Crear actividad(es) – soporta creación múltiple
        """
        is_many = isinstance(request.data, list)
        serializer = self.get_serializer(data=request.data, many=is_many)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class CriterioEvaluacionViewSet(viewsets.ModelViewSet):
    """
    CRUD completo para criterios de evaluación
    """
    serializer_class = CriterioEvaluacionSerializer
    queryset = CriterioEvaluacion.objects.all().order_by('id')   # orden opcional

    # ←–– Filtro por silabo_id ––→
    def get_queryset(self):
        qs = super().get_queryset().filter(activo=True)          # solo activos
        silabo_id = self.request.query_params.get('silabo_id')
        if silabo_id:
            qs = qs.filter(silabo_id=silabo_id)
        return qs

    def create(self, request, *args, **kwargs):
        """
        Crear criterio(s) de evaluación – soporta creación múltiple
        """
        is_many = isinstance(request.data, list)
        serializer = self.get_serializer(data=request.data, many=is_many)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


# ─────────────────────────────────────────────
#  Silabos
# ─────────────────────────────────────────────

class SilaboViewSet(viewsets.ModelViewSet):
    """
    CRUD completo para sílabos
    """
    queryset = Silabo.objects.all()
    serializer_class = SilaboSerializer

    @action(detail=True, methods=['get'])
    def unidades(self, request, pk=None):
        """
        Obtener unidades de un sílabo
        """
        silabo = self.get_object()
        unidades = silabo.actividades.filter(activo=True)  # Nota: revisar nombre de related_name
        serializer = UnidadSerializer(unidades, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def actividades_completas(self, request, pk=None):
        """
        Obtener actividades completas de un sílabo
        """
        silabo = self.get_object()
        actividades = silabo.actividades.filter(activo=True)
        serializer = ActividadSerializer(actividades, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def criterios_evaluacion_completos(self, request, pk=None):
        """
        Obtener criterios de evaluación completos de un sílabo
        """
        silabo = self.get_object()
        criterios = silabo.actividades.filter(activo=True)  # Nota: revisar nombre de related_name
        serializer = CriterioEvaluacionSerializer(criterios, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def por_profesor(self, request):
        """
        Obtener sílabos por profesor
        """
        profesor_id = request.query_params.get('profesor_id')
        if profesor_id:
            silabos = self.queryset.filter(profesor_id=profesor_id, activo=True)
            serializer = self.get_serializer(silabos, many=True)
            return Response(serializer.data)
        else:
            return Response(
                {'error': 'profesor_id es requerido'}, 
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=False, methods=['get'])
    def por_curso(self, request):
        """
        Obtener sílabos por curso
        """
        curso_id = request.query_params.get('curso_id')
        if curso_id:
            silabos = self.queryset.filter(curso_id=curso_id, activo=True)
            serializer = self.get_serializer(silabos, many=True)
            return Response(serializer.data)
        else:
            return Response(
                {'error': 'curso_id es requerido'}, 
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=False, methods=['get'])
    def por_periodo(self, request):
        """
        Obtener sílabos por periodo lectivo
        """
        periodo_id = request.query_params.get('periodo_id')
        if periodo_id:
            silabos = self.queryset.filter(periodo_lectivo_id=periodo_id, activo=True)
            serializer = self.get_serializer(silabos, many=True)
            return Response(serializer.data)
        else:
            return Response(
                {'error': 'periodo_id es requerido'}, 
                status=status.HTTP_400_BAD_REQUEST
            )