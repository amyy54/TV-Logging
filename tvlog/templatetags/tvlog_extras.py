from django import template
from tvlog.models import Show, CurrentlyWatching


register = template.Library()

@register.inclusion_tag("showbox.html")
def tvbox(show: Show):
    return {"show": show}

@register.inclusion_tag("showbox_shortprogress.html")
def tvboxshortprogress(watching: CurrentlyWatching):
    return {"watching": watching}

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
