class Error(object):
    def __init__(self, code='', message='', explain=None):
        self._code = code
        self._message = message
        self._explain = explain

    def to_dict(self):
        result = {
            'type': 'error'
        }
        if self._code:
            result['code'] = self._code

        if self._message:
            result['message'] = self._message

        if self._explain:
            result['explain'] = self._explain

        return result


class FormError(object):
    def __init__(self, name, fields=None):
        self._name = name
        self._fields = fields or {}

    def add_field_error(self, name, error):
        field_errors = self._fields.get(name, [])
        field_errors.append(error)
        self._fields[name] = field_errors

    def to_dict(self):
        result = {
            'type': 'form_error',
            'name': self._name,
            'fields': self._fields
        }
        return result

    @staticmethod
    def from_form(name, django_form):
        form_error = FormError(name)
        for field_name, field_errors in django_form.errors.items():
            for field_error in field_errors:
                form_error.add_field_error(field_name,field_error)
        return form_error