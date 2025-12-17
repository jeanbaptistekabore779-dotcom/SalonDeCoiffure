# coiffure/templatetags/form_tags.py

from django import template
# Importez la classe du champ lié pour la vérification
from django.forms.boundfield import BoundField 

register = template.Library()

@register.filter
def add_class(field, css_class):
    # Vérifie si 'field' est bien un champ de formulaire
    if isinstance(field, BoundField):
        # Le code initial (si c'est un BoundField)
        return field.as_widget(attrs={"class": css_class})
    else:
        # Renvoie la valeur sans modification si ce n'est pas un champ (évite l'erreur)
        return field