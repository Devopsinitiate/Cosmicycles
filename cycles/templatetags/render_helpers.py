from django import template
from django.utils.safestring import mark_safe
from django.template.defaultfilters import escape
import json

register = template.Library()

@register.simple_tag
def render_recommendations(recommendations_str):
    if not recommendations_str:
        return ""

    if isinstance(recommendations_str, dict):
        recommendations = recommendations_str
    else:
        try:
            recommendations = json.loads(recommendations_str)
        except json.JSONDecodeError:
            lines = ''.join(
                '<li>{}</li>'.format(escape(rec.strip()))
                for rec in recommendations_str.split(';') if rec.strip()
            )
            return mark_safe('<ul class="list-disc pl-5 space-y-1">{}</ul>'.format(lines))

    parts = []
    for category, recs in recommendations.items():
        parts.append('<h6 class="font-semibold text-sm mt-2">{}</h6>'.format(escape(category.capitalize())))
        if isinstance(recs, list):
            items = ''.join('<li>{}</li>'.format(escape(r)) for r in recs)
        else:
            items = '<li>{}</li>'.format(escape(recs))
        parts.append('<ul class="list-disc pl-5 space-y-1">{}</ul>'.format(items))

    return mark_safe(''.join(parts))
