from django.template import Library

register = Library()
@register.filter
def hash(h, key):
    if type(h) == dict:
        return h.get(key, None)
    elif type(h) == list or type(h) == tuple:
        try:
            return h[int(key)]
        except Exception:
            return 0
    else:
        return None
