from django import template

register = template.Library()


def cut_number(number):
    if 999 < number < 100_000_0:
        return str(number//1000) + 'k'
    elif number > 1000000:
        return str(number//100000) + 'm'


register.filter('cut_number', cut_number)
