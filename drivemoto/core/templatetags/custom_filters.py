from django import template

register = template.Library()

@register.filter
def startswith(value, arg):
    """Check if a string starts with the given prefix."""
    return value.startswith(arg)
