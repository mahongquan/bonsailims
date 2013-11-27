from django.core.mail import send_mass_mail, send_mail
import models

def send_sample_created_email(sender, instance, **kwargs):
    project = instance.subject.project
    subscriptions = models.UserProjectSubscription.objects.filter(project=project, notify_me=True).all()
    users_to_notify =[]
    [(users_to_notify.append(s.user.email)) for s in subscriptions]
    if len(users_to_notify) > 0:
        subject = '[BonsaiLIMS] Project Update: ' % project
        from_email = 's.bozdag@dundee.ac.uk'
        message = 'sample(%s) is created or updated in BonsaiLIMS.' % instance
        print len(users_to_notify)
        print users_to_notify
        email = ((subject, message, from_email, users_to_notify),)
        send_mass_mail(email)
    
