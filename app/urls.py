from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('services/', views.services, name='services'),
    path('services/mechanicLocator/', views.mechanicLocator, name='mechanicLocator'),
    path('services/policeStations/', views.policeStations, name='policeStations'),
    path('services/emergencyContact/', views.emergencyContact, name='emergencyContact'),
    path('services/emergnecyContact/delete/<int:contact_id>/', views.delete_contact, name='delete_contact'),

    path('services/fuelStations/', views.fuelStations, name='fuelStations'),
    path('services/ngo/', views.ngo, name='ngo'),
    path('services/quickAlert/', views.quickAlert, name='quickAlert'),
    path('blogs/', views.blogs, name='blogs'),
    path('blogs/addBlogs/', views.addBlogs, name='addBlogs'),
    path('blog/<int:id>/', views.blog_detail, name='blog_detail'),
    path('blog/delete/<int:id>/', views.delete_blog, name='delete_blog'),
    path('blog/approve/<int:id>/', views.approve_blog, name='approve_blog'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('homeAdmin/messages/', views.show_messages, name='show_messages'),
    path('update_contact/<int:contact_id>/', views.update_contact, name='update_contact'),


    #ADMIN VIEW
    path('homeAdmin/', views.homeAdmin, name='homeAdmin'),
    path('homeAdmin/addCampaign', views.addCampaign, name='addCampaign'),
    path('delete-campaign/<int:id>/', views.delete_campaign, name='delete_campaign'),
    path('campaigns/', views.campaigns, name='campaigns'),
    path('campaigns/volunteer/<int:campaign_id>/', views.volunteer_campaign, name='volunteer_campaign'),

]