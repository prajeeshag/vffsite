from django.forms import DateInput


class DatePickerInput(DateInput):
    template_name = 'mySmartFields/datepicker.html'

    def __init__(self, startOffset=None, endOffset=None):
        self.startOffset = startOffset
        self.endOffset = endOffset
        super().__init__()

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context['widget']['startYear'] = self.startOffset
        context['widget']['endYear'] = self.endOffset
        return context
