"""
louersanscom urls.py

"""
from django.conf.urls.defaults import patterns, url
from geoads.views import AdDetailView, AdSearchView, AdSearchDeleteView, AdUpdateView, AdSearchUpdateView, AdCreateView, CompleteView, AdDeleteView, AdPotentialBuyersView, AdPotentialBuyerContactView

from sites.louersanscom.ads.models import HomeForRentAd, HomeForRentAdSearch, HomeForRentAdSearchResult
from sites.louersanscom.ads.forms import HomeForRentAdForm
from sites.louersanscom.ads.views import HomeForRentAdSearchView



urlpatterns = patterns('',
    url(r'^(?P<slug>[-\w]+)$', AdDetailView.as_view(model=HomeForRentAd),
                                                            name="view"),
    url(r'^search/$', HomeForRentAdSearchView.as_view(),
                                                                  name='search'),
    url(r'^search/(?P<search_id>\d+)/$', HomeForRentAdSearchView.as_view(),
                                                                  name='search'),
    url(r'^delete_search/(?P<pk>\d+)$', AdSearchDeleteView.as_view(model=HomeForRentAdSearch),
                                         name='delete_search'),
    url(r'^edit_search/(?P<pk>\d+)$', AdSearchUpdateView.as_view(model=HomeForRentAdSearch),
      name="update_search"),
    url(r'^add/$', AdCreateView.as_view(model=HomeForRentAd,
                                        form_class=HomeForRentAdForm),
                                                             name='add'),
    url(r'^add/complete/$', CompleteView.as_view(), name='complete'),
    url(r'^(?P<pk>\d+)/edit$', AdUpdateView.as_view(model=HomeForRentAd,
                                        form_class=HomeForRentAdForm),
                                                            name='edit'),
    url(r'^(?P<pk>\d+)/delete$', AdDeleteView.as_view(model=HomeForRentAd),
                                                          name='delete'),
    url(r'^contact_buyers/(?P<pk>\d+)$', AdPotentialBuyersView.as_view(model=HomeForRentAd,
      search_model=HomeForRentAdSearchResult), name="contact_buyers"),
    url(r'^contact_buyer/(?P<adsearchresult_id>\d+)$', AdPotentialBuyerContactView.as_view(), name="contact_buyer"),
)