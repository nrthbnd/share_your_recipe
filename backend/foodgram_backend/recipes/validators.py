from django.core.validators import RegexValidator

# Валидация цвета тега:
HEX_REGEX = r'^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$'
HEX_VALIDATOR = RegexValidator(
    regex=HEX_REGEX,
    message='Значение не соответствует коду цвета в формате HEX.'
)
