from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()

# ─────────────────────────────────────────────
#  SEGURIDAD
# ─────────────────────────────────────────────
router.register(r'roles', RolViewSet)
router.register(r'usuarios', CustomUserViewSet)
router.register(r'personas', PersonaViewSet)
router.register(r'logs', LogProcesosViewSet)

# ─────────────────────────────────────────────
#  Estructura académica
# ─────────────────────────────────────────────
router.register(r'universidades', UniversidadViewSet)
router.register(r'facultades', FacultadViewSet)
router.register(r'departamentos', DepartamentoViewSet)
router.register(r'carreras', CarreraViewSet)

# ─────────────────────────────────────────────
#  Planes de estudio y periodos
# ─────────────────────────────────────────────
router.register(r'planes', PlanCurricularViewSet)
router.register(r'semestres-academicos', SemestreAcademicoViewSet)
router.register(r'semestres-plan', SemestrePlanViewSet)

# ─────────────────────────────────────────────
#  Cursos y prerrequisitos
# ─────────────────────────────────────────────
router.register(r'areas', AreaViewSet)
router.register(r'tipos-curso', TipoCursoViewSet)
router.register(r'cursos', CursoViewSet)

# ─────────────────────────────────────────────
#  Profesores y carga académica
# ─────────────────────────────────────────────
router.register(r'profesiones', ProfesionViewSet)
router.register(r'profesores', ProfesorViewSet)
router.register(r'cargas', CargaCursoViewSet)
router.register(r'grupos', GrupoViewSet)

# ─────────────────────────────────────────────
#  Estudiantes
# ─────────────────────────────────────────────
router.register(r'estudiantes', EstudianteViewSet)

# ─────────────────────────────────────────────
#  Modelos complementarios para el sílabo
# ─────────────────────────────────────────────
router.register(r'periodos-lectivos', PeriodoLectivoViewSet)
router.register(r'metodologias', MetodologiaViewSet)
router.register(r'bibliografias', BibliografiaViewSet)
router.register(r'semanas', SemanaViewSet)
router.register(r'contenidos-especificos', ContenidoEspecificoViewSet)
router.register(r'unidades', UnidadViewSet)
router.register(r'actividades', ActividadViewSet)
router.register(r'criterios', CriterioEvaluacionViewSet)

# ─────────────────────────────────────────────
#  Silabos
# ─────────────────────────────────────────────
router.register(r'silabos', SilaboViewSet)

urlpatterns = router.urls