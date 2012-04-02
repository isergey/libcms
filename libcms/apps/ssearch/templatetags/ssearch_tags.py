import datetime
from django.template import Library

register = Library()

@register.filter
def date_from_isostring(isostring):
    try:
        return datetime.datetime.strptime(isostring, "%Y-%m-%dT%H:%M:%SZ")
    except ValueError:
        return None


facet_titles = {

}
def facet_title(code):
