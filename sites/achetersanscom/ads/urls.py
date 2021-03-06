"""
AcheterSansCom urls.py

"""
from django.conf.urls.defaults import patterns, url
from geoads.views import (AdDetailView, AdSearchUpdateView, AdPotentialBuyerContactView, AdSearchDeleteView, AdCreateView, CompleteView, AdPotentialBuyersView)
from sites.achetersanscom.ads.models import HomeForSaleAd, HomeForSaleAdSearch, HomeForSaleAdSearchResult
from sites.achetersanscom.ads.forms import HomeForSaleAdForm
from sites.achetersanscom.ads.views import HomeForSaleAdSearchView

from utils.views import ModeratedAdUpdateView, CustomAdDeleteView
from utils.forms import PrettyAdPictureForm
from homeads.forms import HomeContactForm


urlpatterns = patterns('',
    url(r'^(?P<slug>[-\w]+)$', AdDetailView.as_view(model=HomeForSaleAd, contact_form=HomeContactForm), name="view"),
    url(r'^search/$', HomeForSaleAdSearchView.as_view(), name='search'),
    url(r'^search/(?P<search_id>\d+)/$', HomeForSaleAdSearchView.as_view(), name='search'),
    url(r'^delete_search/(?P<pk>\d+)$', AdSearchDeleteView.as_view(model=HomeForSaleAdSearch), name='delete_search'),
    url(r'^edit_search/(?P<pk>\d+)$', AdSearchUpdateView.as_view(model=HomeForSaleAdSearch), name="update_search"),
    url(r'^add/$', AdCreateView.as_view(model=HomeForSaleAd, form_class=HomeForSaleAdForm, ad_picture_form=PrettyAdPictureForm), name='add'),
    url(r'^add/complete/$', CompleteView.as_view(), name='complete'),
    url(r'^(?P<pk>\d+)/edit$', ModeratedAdUpdateView.as_view(model=HomeForSaleAd, form_class=HomeForSaleAdForm, ad_picture_form=PrettyAdPictureForm), name='edit'),
    url(r'^(?P<pk>\d+)/delete$', CustomAdDeleteView.as_view(model=HomeForSaleAd), name='delete'),
    url(r'^contact_buyers/(?P<pk>\d+)$', AdPotentialBuyersView.as_view(model=HomeForSaleAd, search_model=HomeForSaleAdSearchResult), name="contact_buyers"),
    url(r'^contact_buyer/(?P<adsearchresult_id>\d+)$', AdPotentialBuyerContactView.as_view(), name="contact_buyer"),
)
