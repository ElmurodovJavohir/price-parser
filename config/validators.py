from django.core import validators
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.core.exceptions import ValidationError
from datetime import date


@deconstructible
class UsernameValidator(validators.RegexValidator):
    regex = r'^[\w.]{5,32}$'
    message = _(
        'Enter a valid username. This value may contain only letters, '
        'numbers, and ./_ characters.'
    )
    flags = 0


@deconstructible
class PhoneNumberValidator(validators.RegexValidator):
    regex = r"^\+[0-9]\d{7,14}$"
    message = _(
        "Phone number must be entered in a valid format.",
    )


def date_of_birth_validate(value: date):
    today = timezone.now().date()
    if value > today:
        raise ValidationError("Date must be greater or equal to today")


username_validators = [UsernameValidator()]  # noqa
phone_number_validators = [PhoneNumberValidator()]  # noqa
date_of_birth_validators = [date_of_birth_validate]
