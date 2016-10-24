from django import template

register = template.Library()


@register.filter(name='format_title')
def format_title(title):
    return title.replace(' ', '-')


@register.filter(name='my_truncateuser')
def truncateuser(user_list, display_num: int)-> list:
    return user_list[:display_num]
