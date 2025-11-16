from django import template
from inventory.models import Material


register = template.Library()


@register.simple_tag # performs a fucntion
def get_all_materials():
    return Material.objects.all()


@register.inclusion_tag('inventory/materials_list.html') # adds a block of html-file
def show_materials():
    materials = Material.objects.all()
    return {"materials": materials}