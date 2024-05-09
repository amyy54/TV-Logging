from typing import List
from .models import CurrentlyWatching

def create_watching_groups(currently_watching: List[CurrentlyWatching], max_shows_displayed: int = 0) -> []:
    res = {}
    for watching in currently_watching:
        abv = watching.season.show.abbreviation
        if abv in res:
            if max_shows_displayed > 0:
                if len(res[abv]) >= max_shows_displayed:
                    if res[abv][-1] is not None:
                        res[abv].append(None)
                else:
                    res[abv].append(watching)
            else:
                res[abv].append(watching)
        else:
            res[abv] = [watching]
    return list(res.values())
