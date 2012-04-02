from django.template import Library

register = Library()
@register.filter
def hash(h, key):
    if type(h) != dict:
        return None
    return h.get(key, None)
