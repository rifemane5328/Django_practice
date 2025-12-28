from django import template


register = template.Library()

@register.filter
def stars(rating):
    full = int(round(rating))
    return '⭐️' * full
