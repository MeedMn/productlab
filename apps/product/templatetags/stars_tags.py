from django import template
from django.utils.safestring import mark_safe
import math

register = template.Library()

@register.simple_tag
def stars_tag(product):
    full_stars = int(product.rating)
    half_stars = round(product.rating - full_stars, 1) >= 0.5
    empty_stars = 5 - full_stars - half_stars
    stars_html = ''
    for i in range(full_stars):
        stars_html += '<i class="fa fa-star"></i>'
    if half_stars:
        stars_html += '<i class="fa fa-star-half-o"></i>'
    for i in range(empty_stars):
        stars_html += '<i class="fa fa-star-o"></i>'
    return mark_safe(stars_html)
