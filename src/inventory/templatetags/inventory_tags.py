from django import template
from inventory.models import Material


register = template.Library()


@register.simple_tag
def get_all_materials():
    return Material.objects.all()


@register.inclusion_tag('inventory/materials_list.html')
def get_materials():
    materials = Material.objects.all()
    return {"materials": materials}