from django import template


register = template.Library()


@register.filter('startswith')
def startswith(text, starts):
    if isinstance(text, str):
        return starts in text
    return False
