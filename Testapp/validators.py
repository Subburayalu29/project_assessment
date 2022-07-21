from django.core.exceptions import ValidationError


def validate_file_size(value):
    file_size = value.size

    if file_size > 4194304:
        raise ValidationError("You cannot upload file more than 4Mb")
    else:
        return value