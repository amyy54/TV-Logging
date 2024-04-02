from django import template
from tvlog.models import Show


register = template.Library()

@register.inclusion_tag("showbox.html")
def tvbox(show: Show):
    return {"show": show}

@register.filter(name="showrun")
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

