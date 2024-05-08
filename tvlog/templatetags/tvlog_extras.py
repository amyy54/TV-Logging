from django import template
from django.conf import settings
from tvlog.models import Show, CurrentlyWatching, Season
from datetime import date, datetime

register = template.Library()

@register.simple_tag
def inDebug():
    return settings.DEBUG

@register.inclusion_tag("showbox.html")
def tvbox(show: Show):
    return {"show": show}

@register.inclusion_tag("showbox_shortprogress.html")
def tvboxshortprogress(watching: []):
    return {"watching": watching}

@register.inclusion_tag("rating.html")
def rating(rating):
    return {"rating": rating}

@register.filter
def showrun(show: Show):
    startYear = show.startdate.year
    if show.enddate is None:
        return f"{startYear}-"
    else:
        endYear = show.enddate.year
        if startYear == endYear:
            return startYear
        else:
            return f"{startYear}-{endYear}"

@register.filter
def seasonprogress(watching: CurrentlyWatching):
    if watching.episode >= watching.season.episodes:
        return 100
    else:
        return round((watching.episode / watching.season.episodes) * 100)

@register.filter
def seasonmd(season: Season):
    return season.startdate.strftime("%b. %Y")

@register.filter
def watchingdate(watching: CurrentlyWatching):
    now = date.today()
    watchdate = watching.date
    if now.year == watchdate.year:
        return watchdate.strftime("%B %-d")
    else:
        return watchdate.strftime("%b. %Y")

@register.filter
def joindate(date: datetime):
    return date.strftime("%b. %Y")

@register.filter
def ratingoutof5(rating):
    res = rating / 2
    if int(res) == res:
        return int(res)
    else:
        return res
