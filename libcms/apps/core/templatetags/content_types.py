from django.template import Library


types = {
    'doc': 'word',
    'docx': 'word',
    'pdf': 'pdf',
    'xls': 'excel',
    'xlsx': 'excel',
    'jpg': 'image',
    'jpeg': 'image',
    'png': 'image',
    'gif': 'image',
    'ppt': 'powerpoint',
    'pptx': 'powerpoint',
    'wmv': 'video',
    'mp4': 'video',
    'avi': 'video',
}

register = Library()
@register.filter
def content_type(path):
    if not path:
        return u''
    corrected_path = path.lower().strip().split(u'.')
    return types.get(corrected_path[-1], u'any')

