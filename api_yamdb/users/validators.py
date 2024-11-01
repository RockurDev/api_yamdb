import re

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_username(username: str) -> None:
    if username == 'me':
        raise ValidationError(
            _("The username 'me' is prohibited."),
            params={'value': username},
        )

    prohibited_symbols = ''.join(re.findall(r'[^\w.@+-]', username))

    if prohibited_symbols:
        raise ValidationError(
            _('Next symbols are prohibited: %(symbols)s'),
            params={'value': username, 'symbols': prohibited_symbols},
        )
