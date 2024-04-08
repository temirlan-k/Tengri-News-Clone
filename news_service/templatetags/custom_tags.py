from django import template

register = template.Library()


@register.filter(name="is_video")
def is_video(media_src):
    return media_src.endswith(".mp4")
