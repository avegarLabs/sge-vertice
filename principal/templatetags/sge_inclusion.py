from django import template

register = template.Library()


@register.inclusion_tag('includes/submit_buttons.html', takes_context=True)
def submit_row(context):
    return {
        "pk": context['item'].pk,
        "model_name": context['model_name'],
        "verbose_name": context['verbose_name'],
        "change": context['user'].has_perm(f"{context.request.current_app}.change_{context['model_name']}"),
        "delete": context['user'].has_perm(f"{context.request.current_app}.delete_{context['model_name']}")
    }


@register.inclusion_tag('includes/submit_buttons+suplemento.html', takes_context=True)
def submit_row_extra_buttons(context):
    return {
        "pk": context['item'].pk,
        "model_name": context['model_name'],
        "verbose_name": context['verbose_name'],
        "change": context['user'].has_perm(f"{context.request.current_app}.change_{context['model_name']}"),
        "delete": context['user'].has_perm(f"{context.request.current_app}.delete_{context['model_name']}"),
        "suplemento": context['user'].has_perm(f"{context.request.current_app}.add_suplemento")
    }

@register.inclusion_tag('includes/submit_buttons+trabajadores_capacitacion.html', takes_context=True)
def submit_row_extra_buttons_actividadcapacitaciontrab(context):
    return {
        "pk": context['item'].pk,
        "model_name": context['model_name'],
        "verbose_name": context['verbose_name'],
        "change": context['user'].has_perm(f"{context.request.current_app}.change_{context['model_name']}"),
        "delete": context['user'].has_perm(f"{context.request.current_app}.delete_{context['model_name']}"),
        "actividadcapacitaciontrab": context['user'].has_perm(f"{context.request.current_app}.read_actividadcapacitaciontrabajadores_new")
    }