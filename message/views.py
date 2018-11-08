from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from django.template import loader
from django import forms
import boto3

def index(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = SNSForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            if form.commit():
                return HttpResponse("Message Sent Successfully")
            else:
                return HttpResponse("Failed to send to topic")

    template = loader.get_template('message/index.html')
    return HttpResponse(template.render({}, request))

class SNSForm(forms.Form):
    message = forms.CharField(label='Message', max_length=100)

    def commit(self):
        try:
            client = boto3.client(
                "sns",
                aws_access_key_id=settings.ACCESS_KEY,
                aws_secret_access_key=settings.SECRET_KEY,
                region_name="us-east-1"
            )

            client.publish(
                TopicArn=settings.TOPIC_ARN,
                Message=self.cleaned_data.get('message')
            )
        except:
            return False

        return True
