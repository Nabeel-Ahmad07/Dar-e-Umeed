from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.cache import never_cache
from .models import Contacts, Messages, Blogs, Campaign, Volunteer, Messages
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings


# Create your views here.
def home(request):
    campaigns = Campaign.objects.all()[:3]  
    blogs = Blogs.objects.filter(isApproved = True)[:3]
    return render(request, 'home.html', {'campaigns': campaigns, 'blogs': blogs})

def services(request):
    return render(request, 'services.html')

@login_required
def mechanicLocator(request):
    return render(request, 'mechanicLocator.html')

@login_required
def policeStations(request):
    return render(request, 'policeStations.html')

@never_cache
@login_required
def emergencyContact(request):
    if request.method == 'POST':
        if request.POST.get('alert_type') == 'emergency':
            location = request.POST.get('location')
            message_body = (
                "⚠️ EMERGENCY ALERT ⚠️\n\n"
                f"{request.user.first_name} {request.user.last_name} has triggered an emergency alert.\n\n"
                f"Location: {location}\n\n"
                "Please try to contact them immediately."
            )

            contacts = Contacts.objects.filter(user=request.user)
            recipient_list = [c.email for c in contacts if c.email]

            if recipient_list:
                send_mail(
                    subject='🚨 Emergency Alert',
                    message=message_body,
                    from_email='noreply@yourapp.com',
                    recipient_list=recipient_list,
                    fail_silently=False
                )
                messages.success(request, "Emergency alert sent to all contacts.")
            else:
                messages.warning(request, "No contacts available to send the alert.")
        else:
            name = request.POST['name']
            relation = request.POST['relation']
            email = request.POST['email']
            phone = request.POST['phone']

            Contacts.objects.create(
                user=request.user,
                name=name,
                relation=relation,
                email=email,
                phone_number=phone
            )
            messages.success(request, 'Contact added successfully.')

    contacts = Contacts.objects.filter(user=request.user)
    return render(request, 'emergencyContact.html', {'contacts': contacts})

@login_required
def delete_contact(request, contact_id):
    contact = Contacts.objects.get(id=contact_id, user=request.user)
    contact.delete()
    messages.success(request, 'Contact deleted successfully.')
    return redirect('emergencyContact')


@login_required
def fuelStations(request):
    return render(request, 'fuelStations.html')

@never_cache
@login_required
def ngo(request):
    return render(request, 'ngo.html')

@login_required
def quickAlert(request):
    contacts = Contacts.objects.filter(user=request.user)

    if request.method == 'POST':
        from_location = request.POST.get('from_location')
        to_location = request.POST.get('to_location')
        mode = request.POST.get('mode')

        subject = f"Travel Alert by {request.user.username}"
        message = (
            f"{request.user.first_name} {request.user.last_name} has sent a travel alert.\n\n"
            f"From: {from_location}\n"
            f"To: {to_location}\n"
            f"Mode of Travel: {mode}\n\n"
            f"If this wasn't initiated by them or you sense something's wrong, please contact them immediately."
        )

        recipient_list = [contact.email for contact in contacts if contact.email]

        if recipient_list:
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                recipient_list,
                fail_silently=False
            )
            messages.success(request, "Travel alert sent to your contacts.")
        else:
            messages.warning(request, "No contacts with valid emails found.")

        return redirect('quickAlert')

    return render(request, 'quickAlert.html', {'contacts': contacts})

def blogs(request):
    blogs = Blogs.objects.filter(isApproved = True)
    return render(request, 'blogs.html', {'blogs': blogs})

@login_required
def addBlogs(request):
    if request.method == 'POST':
        blog = Blogs(
            title=request.POST['title'],
            author=request.user,
            img=request.FILES['img'],
            main_para=request.POST['main_para'],
            heading1=request.POST.get('heading1'),
            para1=request.POST.get('para1'),
            heading2=request.POST.get('heading2'),
            para2=request.POST.get('para2'),
            isApproved=False 
        )
        blog.save()
        return redirect('blogs')  
    return render(request, 'addBlogs.html')

def blog_detail(request, id):
    blog = get_object_or_404(Blogs, id=id)
    return render(request, 'blog_detail.html', {'blog': blog})

@user_passes_test(lambda u: u.is_superuser) 
def delete_blog(request, id):
    blog = get_object_or_404(Blogs, id=id)
    blog.delete()
    return redirect('homeAdmin')

@user_passes_test(lambda u: u.is_superuser) 
def approve_blog(request, id):
    blog = get_object_or_404(Blogs, id=id)
    blog.isApproved = True
    blog.save()
    return redirect('homeAdmin') 

@login_required
def volunteer_campaign(request, campaign_id):
    campaign = get_object_or_404(Campaign, id=campaign_id)

    if Volunteer.objects.filter(user=request.user, campaign=campaign).exists():
        messages.info(request, "You have already volunteered for this campaign.")
    else:
        Volunteer.objects.create(user=request.user, campaign=campaign)
        messages.success(request, f"You've successfully volunteered for '{campaign.title}'.")

    return redirect('campaigns')  

def about(request):
    return render(request, 'about.html')

def contact(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        message_text = request.POST['message']

        Messages.objects.create(name=name, email=email, message=message_text)
        messages.success(request, 'Thank you! Your message has been sent.')

    return render(request, 'contact.html')



@login_required
@user_passes_test(lambda u: u.is_superuser) 
def homeAdmin(request):
    campaigns = Campaign.objects.all()
    blogs = Blogs.objects.all()
    return render(request, 'homeAdmin.html', {'campaigns': campaigns, 'blogs': blogs})

@login_required
@user_passes_test(lambda u: u.is_superuser)
def addCampaign(request):
    if request.method == 'POST':
        title = request.POST['title']
        desc = request.POST['desc']
        Campaign.objects.create(title=title, desc=desc)
        return redirect('homeAdmin')  

    return render(request, 'addCampaign.html')

@login_required
@user_passes_test(lambda u: u.is_superuser)
def delete_campaign(request, id):
    campaign = get_object_or_404(Campaign, id=id)
    if request.method == 'POST':
        campaign.delete()
    return redirect('homeAdmin')  

def campaigns(request):
    campaigns = Campaign.objects.all()
    volunteered_campaigns = []

    if request.user.is_authenticated:
        volunteered_campaigns = Campaign.objects.filter(volunteer__user=request.user)

    return render(request, 'campaigns.html', {
        'campaigns': campaigns,
        'volunteered_campaigns': volunteered_campaigns,
    })


@login_required
@user_passes_test(lambda u: u.is_superuser)
def show_messages(request):
    if not request.user.is_superuser:
        return redirect('home')  

    messages_list = Messages.objects.all().order_by('-id')  
    return render(request, 'messages.html', {'messages_list': messages_list})

@login_required
def update_contact(request, contact_id):
    contact = get_object_or_404(Contacts, id=contact_id, user=request.user)

    if request.method == 'POST':
        contact.name = request.POST['name']
        contact.relation = request.POST['relation']
        contact.email = request.POST['email']
        contact.phone_number = request.POST['phone']
        contact.save()

        messages.success(request, 'Contact updated successfully.')
        return redirect('emergencyContact') 

    return render(request, 'updateContact.html', {'contact': contact})
