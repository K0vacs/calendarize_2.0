from django import template

register = template.Library()

@register.filter
def paginate(value): # Only one argument.
    try:
        """Converts underscores into spaces"""
        value = int(value) + 1
        return list(range(1, value))
    except:
        return [1]

@register.filter
def nextPage (value):
    try:
        return value + 1
    except:
        return 1

@register.filter
def prevPage (value):
    try:
        return value - 1
    except:
        return 1