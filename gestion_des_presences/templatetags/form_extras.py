from django import template
register = template.Library()

@register.filter(name="add_class")
def add_class(field, css):
    # conserve les attrs existants et ajoute/merge les classes CSS
    attrs = field.field.widget.attrs.copy()
    existing = attrs.get("class", "")
    attrs["class"] = (existing + " " + css).strip()
    return field.as_widget(attrs=attrs)

@register.filter(name="add_attr")
def add_attr(field, arg):
    # usage: {{ field|add_attr:"placeholder:Votre email" }}
    key, _, val = arg.partition(":")
    attrs = field.field.widget.attrs.copy()
    attrs[key] = val
    return field.as_widget(attrs=attrs)
