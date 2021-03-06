import datetime
from django.forms import widgets, MultiValueField, fields, ValidationError

from pint import UnitRegistry
from .options import Units

ureg = UnitRegistry()


class HeightWidget(widgets.MultiWidget):
    def __init__(self, attrs=None):
        _widgets = (
            widgets.Select(choices=Units.choices(), attrs={'class': 'hn-measurement unit-select height'}),
            widgets.NumberInput(attrs={'customary': True, 'class': 'hn-measurement height', 'min': 0, 'max': 7}),
            widgets.NumberInput(attrs={'customary': True, 'class': 'hn-measurement height', 'min': 0, 'max': 11}),
            widgets.NumberInput(
                attrs={'metric': True, 'class': 'hn-measurement height', 'value': 20, 'min': 20, 'max': 280})
        )

        super(HeightWidget, self).__init__(_widgets, attrs)

    def decompress(self, value):
        if value:
            height = value * ureg.centimeters
            return [Units.label(Units.CUSTOMARY), int(height.to(ureg.feet).magnitude),
                    int(height.to(ureg.inches).magnitude % 12)]
        return [Units.label(Units.CUSTOMARY), 0, 0]

    def format_output(self, rendered_widgets):
        metric_div = '<div class="customary"><span>%s\'</span><span>%s"</span></div>' % \
                     (rendered_widgets[1], rendered_widgets[2])
        customary_div = '<div class="metric">%scm</div>' % rendered_widgets[3]

        value = '%s<div class="hn-measurement wrapper">%s</div>' % \
                (rendered_widgets[0], ''.join([metric_div, customary_div]))
        return value

    def value_from_datadict(self, data, files, name):
        return [data['height_0'], data['height_1'], data['height_2'], data['height_3']]


class WeightWidget(widgets.MultiWidget):
    def __init__(self, attrs=None):
        _widgets = (
            widgets.Select(choices=Units.choices(), attrs={'class': 'hn-measurement unit-select weight'}),
            widgets.NumberInput(attrs={'customary': True, 'class': 'hn-measurement weight', 'value': 80, 'min': 1})
        )

        self.name = ''
        super(WeightWidget, self).__init__(_widgets, attrs)

    def decompress(self, value):
        if value:
            w = value * ureg.milligrams
            return [Units.label(Units.CUSTOMARY), int(w.to(ureg.lb))]
        return [Units.label(Units.CUSTOMARY), 0]

    def format_output(self, rendered_widgets):
        value = '%s<div class="hn-measurement wrapper">%s<span id="weight-label">lbs</span></div>' % \
                (rendered_widgets[0], ''.join(rendered_widgets[1:]))
        return value


class DateTimeMultiWidget(widgets.MultiWidget):
    def __init__(self, attrs=None):
        _widgets = (
            widgets.DateInput(format='%m/%d/%Y', attrs={'datepicker': True}),
            widgets.TimeInput(attrs={'timepicker': True}),
        )

        super(DateTimeMultiWidget, self).__init__(_widgets, attrs)

    def roundTime(self, dt=None, roundTo=60):
        """Round a datetime object to any time laps in seconds
        dt : datetime.datetime object, default now.
        roundTo : Closest number of seconds to round to, default 1 minute.
        Author: Thierry Husson 2012 - Use it as you want but don't blame me.
        """
        if dt is None:
            dt = datetime.datetime.now()
        seconds = (dt - dt.min).seconds
        # // is a floor division, not a comment on following line:
        rounding = (seconds+roundTo/2) // roundTo * roundTo
        return dt + datetime.timedelta(0,rounding-seconds,-dt.microsecond)

    def decompress(self, value):
        if not value:
            time = datetime.datetime.now()
            time = self.roundTime(time, roundTo=1800)
            return [time.date(), time.time()]
        else:
            if isinstance(value, datetime.datetime):
                return [value.date(), value.time()]
            else:
                time = datetime.datetime.strptime(value, "%m/%d/%Y|%I:%M %p")
                time = self.roundTime(time, roundTo=1800)
                return [time.date(), time.time()]

    def format_output(self, rendered_widgets):
        return ''.join(rendered_widgets)


class HeightField(MultiValueField):
    widget = HeightWidget()

    def __init__(self, *args, **kwargs):
        _fields = (
            fields.ChoiceField(choices=Units.choices(), initial=Units.label(Units.CUSTOMARY)),
            fields.IntegerField(min_value=0, max_value=8, initial=1, required=True),
            fields.IntegerField(min_value=0, max_value=11, initial=1, required=True),
            fields.IntegerField(min_value=1, max_value=280, initial=100, required=False)
        )
        super(HeightField, self).__init__(_fields, *args, **kwargs)

    def compress(self, data_list):
        data_list = [int(x) for x in data_list]
        
        units = data_list[0]
        if units == Units.CUSTOMARY:
            feet = data_list[1] * ureg.feet
            inches = data_list[2] * ureg.inches
            return int((feet + inches).to(ureg.centimeters).magnitude)
        elif units == Units.METRIC:
            return int(data_list[3])
        else:
            return 0
    
    def clean(self, value):
        for i, item in enumerate(value):
            if item in self.empty_values:
                value[i] = '1'
        return super(HeightField, self).clean(value)


class WeightField(MultiValueField):
    widget = WeightWidget()

    def __init__(self, *args, **kwargs):
        _fields = (
            fields.ChoiceField(choices=Units.choices()),
            fields.IntegerField(min_value=1),
        )
        super(WeightField, self).__init__(_fields, *args, **kwargs)

    def compress(self, data_list):
        data_list = [int(x) for x in data_list]

        units = data_list[0]

        if units == Units.CUSTOMARY:
            pounds = data_list[1] * ureg.lb
            return int(pounds.to(ureg.milligrams).magnitude)
        elif units == Units.METRIC:
            kilos = data_list[1] * ureg.kilograms
            return int(kilos.to(ureg.milligrams).magnitude)
        else:
            return 0

    def clean(self, value):
        return super(WeightField, self).clean(value)


class DateTimeMultiField(MultiValueField):
    widget = DateTimeMultiWidget()

    def __init__(self, *args, **kwargs):
        _fields = (
            fields.DateField(required=True),
            fields.TimeField(required=True)
        )
        super(DateTimeMultiField, self).__init__(_fields, *args, **kwargs)

    def compress(self, data_list):
        print(data_list)
        return datetime.datetime.strptime(data_list[0] + '|' + data_list[1], "%m/%d/%Y|%I:%M %p")

    def clean(self, value):
        # return self.compress(value)
        return self.compress(value)