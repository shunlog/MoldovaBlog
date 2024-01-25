from django.core.exceptions import ValidationError


class PasswordLengthValidator:
    def __init__(self, min_length=8, max_length=128):
        self.min_length = min_length
        self.max_length = max_length

    def validate(self, password, user=None):
        if len(password) < self.min_length:
            raise ValidationError(
                f"Password must contain at least {self.min_length} characters.",
                code="password_too_short",
                params={"min_length": self.min_length},
            )
        if len(password) > self.max_length:
            raise ValidationError(
                f"Password must contain at most {self.max_length} characters.",
                code="password_too_long",
                params={"max_length": self.max_length},
            )

    def get_help_text(self):
        return f"Your password must contain between {self.min_length} \
        and {self.max_length} characters."
