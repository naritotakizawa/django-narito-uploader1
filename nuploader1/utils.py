from django.http import Http404
from .models import Composite


def make_clean_path_list(request_path):
    return [path for path in request_path.split('/') if path]


def get_sql_kwargs(request_path):
    cleaned_path_list = make_clean_path_list(request_path)
    i = 0
    kwargs = {}
    for path in cleaned_path_list[::-1]:
        arg_name = 'parent__' * i + 'name'
        kwargs[arg_name] = path
        i += 1
    arg_name = 'parent__' * i + 'isnull'
    kwargs[arg_name] = True
    return kwargs


def get_composite(request_path):
    try:
        sql_kwargs = get_sql_kwargs(request_path)
        composite = Composite.objects.get(**sql_kwargs)
    except Composite.DoesNotExist:
        raise Http404
    else:
        return composite
