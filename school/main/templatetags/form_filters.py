from django import template

register = template.Library()

@register.filter(name='add_class')
def add_class(field, css):
    return field.as_widget(attrs={"class": css})

@register.filter
def widget_type(field):
    return field.field.widget.__class__.__name__.lower()
