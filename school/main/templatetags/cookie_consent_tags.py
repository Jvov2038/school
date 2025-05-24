from django import template

register = template.Library()

@register.inclusion_tag('cookie_consent/banner.html', takes_context=True)
def cookie_banner(context):
    return {'messages': context.get('messages', [])}
