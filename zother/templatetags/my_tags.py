from django.template import Library
from django.template.defaultfilters import stringfilter, linebreaksbr
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe
import re
from django.utils.text import normalize_newlines


register = Library()

@stringfilter
def code_style(value, autoescape=True):
    if autoescape:
        esc = conditional_escape
    else:
        esc = lambda x: x
    value = normalize_newlines(esc(value))
    value = value.replace(' ', '&nbsp;')
    value = value.replace('\n', '<br />')
    return mark_safe(value)

code_style.needs_autoescape = True
register.filter(code_style)

@stringfilter
def spacify(value, autoescape=None):
    if autoescape:
        esc = conditional_escape
    else:
        esc = lambda x: x
    return mark_safe(re.sub('\s', '&'+'nbsp;', esc(value)))
spacify.needs_autoescape = True
register.filter(spacify)