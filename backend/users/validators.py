import re

from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _


class UppercaseValidator:
    def validate(self, password, user=None):
        if not re.search(r"[A-Z]", password):
            raise ValidationError(
                _("Le mot de passe doit contenir au moins une lettre majuscule."),
                code="password_no_upper",
            )

    def get_help_text(self):
        return _("Votre mot de passe doit contenir au moins une lettre majuscule.")


class LowercaseValidator:
    def validate(self, password, user=None):
        if not re.search(r"[a-z]", password):
            raise ValidationError(
                _("Le mot de passe doit contenir au moins une lettre minuscule."),
                code="password_no_lower",
            )

    def get_help_text(self):
        return _("Votre mot de passe doit contenir au moins une lettre minuscule.")


class DigitValidator:
    def validate(self, password, user=None):
        if not re.search(r"\d", password):
            raise ValidationError(
                _("Le mot de passe doit contenir au moins un chiffre."),
                code="password_no_digit",
            )

    def get_help_text(self):
        return _("Votre mot de passe doit contenir au moins un chiffre.")


class SpecialCharacterValidator:
    def validate(self, password, user=None):
        if not re.search(r"\W", password):
            raise ValidationError(
                _("Le mot de passe doit contenir au moins un caractère spécial."),
                code="password_no_special",
            )

    def get_help_text(self):
        return _("Votre mot de passe doit contenir au moins un caractère spécial.")
