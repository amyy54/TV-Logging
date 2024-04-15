from django.forms import ModelForm

from datetime import date

from .models import Show, CurrentlyWatching, Season

class NewLogForm(ModelForm):
    class Meta:
        model = CurrentlyWatching
        fields = ["date", "season", "episode", "rating", "rewatch"]

    def __init__(self, *args, **kwargs):
        show = kwargs.pop('show', None)
        super().__init__(*args, **kwargs)
        if show is not None:
            self.fields["season"].queryset = show.season_set.order_by('startdate')

