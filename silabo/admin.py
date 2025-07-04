from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from .models import (
    Rol, CustomUser, Persona, LogProcesos,
    Profesion, Profesor, Estudiante,
    Universidad, Facultad, Departamento, Carrera,
    PlanCurricular, SemestreAcademico, SemestrePlan, PeriodoLectivo,
    Area, TipoCurso, Curso,
    CargaCurso, Grupo,
    Metodologia, Silabo,
    Unidad, Bibliografia, Semana, ContenidoEspecifico,
    Actividad, CriterioEvaluacion,
)

# ─────────────────────────────────────────────
#  CustomUser: extiende la vista estándar
# ─────────────────────────────────────────────
@admin.register(CustomUser)
class CustomUserAdmin(BaseUserAdmin):
    ordering = ("email",)
    list_display = ("email", "username", "rol", "is_staff", "is_active")
    list_filter = ("rol", "is_staff", "is_active")
    search_fields = ("email", "username")

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (_("Información personal"), {"fields": ("username", "rol")}),
        (_("Permisos"), {"fields": ("is_active", "is_staff", "is_superuser",
                                    "groups", "user_permissions")}),
        (_("Fechas"), {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "password1", "password2"),
        }),
    )

# ─────────────────────────────────────────────
#  Inlines útiles
# ─────────────────────────────────────────────
class PersonaInline(admin.StackedInline):
    model = Persona
    can_delete = False
    fk_name = "usuario"  # OneToOne → CustomUser

class ProfesorInline(admin.StackedInline):
    model = Profesor
    can_delete = False
    fk_name = "persona"

class EstudianteInline(admin.StackedInline):
    model = Estudiante
    can_delete = False
    fk_name = "persona"

CustomUserAdmin.inlines = [PersonaInline]

# ─────────────────────────────────────────────
#  modelos sencillos
# ─────────────────────────────────────────────
simple_models = [
    Rol, Persona, LogProcesos,
    Profesion, Profesor, Estudiante,
    Universidad, Facultad, Departamento, Carrera,
    PlanCurricular, SemestreAcademico, SemestrePlan, PeriodoLectivo,
    Area, TipoCurso, Curso,
    CargaCurso, Grupo,
    Metodologia, Silabo,
    Unidad, Bibliografia, Semana, ContenidoEspecifico,
    Actividad, CriterioEvaluacion,
]

for model in simple_models:
    admin.site.register(model)
