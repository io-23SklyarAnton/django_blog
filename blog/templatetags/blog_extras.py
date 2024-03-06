from django import template
from django.template.defaultfilters import stringfilter
from autocorrect import Speller

register = template.Library()


@register.filter(is_safe=True)
@stringfilter
def autocorrect(value):
    spell = Speller()
    return spell(value)

