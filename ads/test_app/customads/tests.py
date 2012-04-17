# coding=utf-8
""" ads test module"""

from django.utils import unittest
from django.test.client import Client
from django.core.urlresolvers import reverse
from django.test.client import RequestFactory
from django.contrib.auth.models import User
from django.http import HttpRequest, Http404

from moderation.helpers import auto_discover

from ads.test_app.customads.models import TestAd
from ads.test_app.customads.filtersets import TestAdFilterSet
from ads.test_app.customads.forms import TestAdForm
from ads import views


class AdViewsTestCase(unittest.TestCase):
    # basic test for ad generic views

    def setUp(self):
        # ad moderation manager to our moderated model
        auto_discover()
        # set up request factory
        self.factory = RequestFactory()
        

    def test_get_adsearchview(self):
        # client just get the adsearchview
        request = self.factory.get('/')
        response = views.AdSearchView.as_view(model=TestAd, 
                                      filterset_class=TestAdFilterSet)(request)
        self.assertEqual(response.status_code, 200)
        # at first time client get search view, and doesn't search ads
        self.assertEqual(response.context_data['search'], False)
        # check that we set initial_ads
        self.assertTrue('initial_ads' in response.context_data)

    '''
    TODO: need to clean post and get view
    def test_post_adsearchview(self):
        # client post to the adsearchview, filtering ads
        request = self.factory.post('/')
        print request
        response = views.AdSearchView.as_view(model=TestAd, 
                                      filterset_class=TestAdFilterSet)(request)
        #self.assertFalse('initial_ads' in response.context_data)
    '''
    
    def test_adcreateview(self):
        # init 
        request = self.factory.get('/ad/create')
        user = User.objects.create_user('paul', 'maccartney@thebeatles.com', 
                                                                'paulpassword')
        request.user = user
        response = views.AdCreateView.as_view(model=TestAd)(request)
        
        # can reach ad create view
        self.assertEqual(response.status_code, 200)
        
        # be sure that picture formset is available
        self.assertTrue('picture_formset' in response.context_data)
        
        # post without filling form/data
        request = self.factory.post('/ad/create')
        request.user = user
        response = views.AdCreateView.as_view(model=TestAd, form_class=TestAdForm)(request)
        self.assertEqual(response.status_code, 200)
        # form is invalid
        self.assertEqual(response.context_data['form'].is_valid(), False)
        
        # post with a good datas
        form_data = {'slug':'my_awesome_ad', 
                     'user_entered_address':'5 rue de Vernueil, Paris', 
                     'ads-adpicture-content_type-object_id-TOTAL_FORMS':4, 
                     'ads-adpicture-content_type-object_id-INITIAL_FORMS':0}
        request = self.factory.post('/ad/create', data=form_data, files=[])
        request.user = user
        response = views.AdCreateView.as_view(model=TestAd, form_class=TestAdForm)(request)
        # redirect after valid form
        self.assertEqual(response.status_code, 302)

        # post with wrong datas
        form_data = {'slug':'my_awesome_ad', 
                     'user_entered_address':'foo bar', 
                     'ads-adpicture-content_type-object_id-TOTAL_FORMS':4, 
                     'ads-adpicture-content_type-object_id-INITIAL_FORMS':0}
        request = self.factory.post('/ad/create', data=form_data, files=[])
        request.user = user
        response = views.AdCreateView.as_view(model=TestAd, form_class=TestAdForm)(request)
        # return to form edition view to correct address
        self.assertEqual(response.status_code, 200)
        

    def test_adreadview(self):
        user = User.objects.create_user('john', 'lennon@thebeatles.com', 
                                                                'johnpassword')
        test_ad, created = TestAd.objects.get_or_create(user=user, 
                     user_entered_address="13 place d'Aligre Paris", slug="1",
                     location="POINT (2.3479424000000000 48.8714721999999995)")
        test_ad.save()
        request = self.factory.get('/ad/read/1')
        # here ad is pending => we shouldn't be able to read it 
        view = views.AdDetailView.as_view(model=TestAd)
        self.assertRaises(Http404, view, request, slug="1")
        # here ad is approved => we shoud be able to view it
        test_ad.moderated_object.approve()
        response = view(request, slug="1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context_data['ad'], test_ad)