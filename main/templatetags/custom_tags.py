from django import template
import random

register = template.Library()

@register.simple_tag
def blurb_text(original, cut):
    if len(original) > cut:
        return original[:cut-2]+"..."
    else:
        return original

@register.simple_tag
def is_writer(user):
    groups = []
    for group in user.groups.all():
        groups.append(group.name)
    return 'Writer' in groups

@register.simple_tag
def is_editor(user):
    groups = []
    for group in user.groups.all():
        groups.append(group.name)
    return 'Editor' in groups

@register.simple_tag
def is_developer(user):
    groups = []
    for group in user.groups.all():
        groups.append(group.name)
    return 'Developer' in groups

@register.simple_tag
def is_chief(user):
    groups = []
    for group in user.groups.all():
        groups.append(group.name)
    return 'Editor In Chief' in groups