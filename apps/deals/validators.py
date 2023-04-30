from rest_framework.exceptions import ValidationError


def validate_csv_file(value):
    if value.content_type != 'text/csv':
        raise ValidationError('Разрешены только CSV файлы.')

    if not value.name.endswith('.csv'):
        raise ValidationError(
            detail='Разрешены только CSV файлы.')
