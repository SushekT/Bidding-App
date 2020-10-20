from django.core.mail import EmailMessage
from django.template.loader import get_template

class CustomMail:
    template_name = str()
    subject = str()
    context = dict()
    email_list = str()

    def __init__(self, template_name, subject, email_list, **kwargs):
        self.template_name = template_name
        self.subject = subject
        self.email_list = email_list
        self.context = kwargs

    def push(self):
        temp = get_template(template_name=self.template_name).render(self.context)
        email = EmailMessage(subject=self.subject, body=temp, to=self.email_list)
        email.content_subtype = 'html'
        try:
            email.send()
        except:
            pass