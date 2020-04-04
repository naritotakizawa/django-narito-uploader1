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


def walk_and_write_zip(composite, zip_file, count, dir_name=''):
    """再帰的にCompositeを走査し、zipファイルに書き込んでいく"""
    dirs = []
    for composite in composite.composite_set.all():
        if composite.is_dir:
            dirs.append(composite)
        else:
            zip_file.writestr(dir_name + composite.name, composite.src.read())
    count -= 1

    if count:
        for composite in dirs:
            walk_and_write_zip(composite, zip_file, count, f'{dir_name}{composite.name}/')
