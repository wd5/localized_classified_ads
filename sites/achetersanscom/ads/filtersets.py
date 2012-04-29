# coding=utf-8
import django_filters
from django.forms import widgets

from geoads.filters import LocationFilter, BooleanForNumberFilter
from geoads.widgets import GooglePolygonWidget, IndifferentNullBooleanSelect, SpecificRangeWidget
from geoads.templatetags.ads_tag import has_value

from utils.bootstrap import BootstrapFieldset

from models import HomeForSaleAd, HABITATION_TYPE_CHOICES
from forms import HomeForSaleAdFilterSetForm



# TODO: improve: inherit form ads.filtersets !
class NicerFilterSet(django_filters.FilterSet):
    def __init__(self, *args, **kwargs):
        super(NicerFilterSet, self).__init__(*args, **kwargs)        
        for name, field in self.filters.iteritems():
            if isinstance(field, django_filters.filters.BooleanFilter):
                field.widget = IndifferentNullBooleanSelect()
            if isinstance(field, django_filters.ChoiceFilter):
                # Add "Any" entry to choice fields.
                field.extra['choices'] = tuple([("", "Tous types"), ] + list(field.extra['choices']))

# TODO: improve: inherit form ads.filtersets !
class HomeForSaleAdFilterSet(NicerFilterSet):
    price = django_filters.OpenRangeNumericFilter(label="Budget (€)", 
                                       widget=SpecificRangeWidget({'size':'6'}))
    surface = django_filters.OpenRangeNumericFilter(label="Surface (m²)", 
                                         widget=SpecificRangeWidget({'size':'6'}))
    nb_of_rooms = django_filters.OpenRangeNumericFilter(label="Nb. de pièces", 
                                         widget=SpecificRangeWidget({'size':'6'}))
    nb_of_bedrooms = django_filters.OpenRangeNumericFilter(label="Nb. de chambres", 
                                         widget=SpecificRangeWidget({'size':'6'}))
    ground_surface = django_filters.OpenRangeNumericFilter(label="(m²)", 
                                         widget=SpecificRangeWidget({'size':'6'}))
    floor = django_filters.OpenRangeNumericFilter(label="Etage", 
                                         widget=SpecificRangeWidget({'size':'6'}))
    habitation_type = django_filters.MultipleChoiceFilter(label="Type d'habitation", 
                                         widget = widgets.CheckboxSelectMultiple(),
                                         choices = HABITATION_TYPE_CHOICES)
    location = LocationFilter(widget=GooglePolygonWidget(), 
                              label="Localisation", required=False)
    balcony = BooleanForNumberFilter(label="Balcon", widget = IndifferentNullBooleanSelect())
    terrace = BooleanForNumberFilter(label="Terrasse", widget = IndifferentNullBooleanSelect())
    separate_toilet = BooleanForNumberFilter(label="Toilettes séparés", widget = IndifferentNullBooleanSelect())
    bathroom = BooleanForNumberFilter(label="Salle de bain", widget = IndifferentNullBooleanSelect())
    shower = BooleanForNumberFilter(label="Salle d'eau (douche)", widget = IndifferentNullBooleanSelect())
    def __init__(self, *args, **kwargs):
        # improve : set default to none if key doesnt exist
        try:
            search = kwargs['search']
            del kwargs['search']
        except:
            search = None
        super(HomeForSaleAdFilterSet, self).__init__(*args, **kwargs)
        if search:
            self.form.fields['location'].widget = GooglePolygonWidget(ads=self.qs, search=search, fillColor="#FFB82E", strokeColor="#20B2AA")
        else:
            self.form.fields['location'].widget = GooglePolygonWidget(ads=[], search=search, fillColor="#FFB82E", strokeColor="#20B2AA")
        # here we open collapsible search filter item
        for f in self.form.helper.layout.fields[1].fields[0].fields:
            for field in f.fields:
                if not isinstance(self.form.fields[field], BootstrapFieldset) and has_value(self.form[field]) == 'has_value':
                    f.set_collapse('in')
    class Meta:
        model = HomeForSaleAd
        form = HomeForSaleAdFilterSetForm