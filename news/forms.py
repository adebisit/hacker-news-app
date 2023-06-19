from django import forms


class NewsFilterForm(forms.Form):
    keyword = forms.CharField(max_length=255, required=False, initial='')
    category = forms.ChoiceField(
        choices=[
            ('all', 'All'),
            ('story', "Story"),
            ('job', "Job"),
            ('askhn', "Ask HN"),
            ('showhn', "Show HN"),
        ],
        required=False,
        initial='all'
    )