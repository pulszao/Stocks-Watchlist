from django import template

register = template.Library()

@register.filter
def multiply(value, arg):
    return value * arg

@register.filter
def rentability(actual, avarage):
    return ((actual-avarage)/avarage) * 100
