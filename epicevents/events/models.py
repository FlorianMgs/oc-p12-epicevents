from django.db import models
from accounts.models import User, Client


class EventStatus(models.Model):

    CREATED = 'created'
    INPROGRESS = 'in_progress'
    FINISHED = 'finished'
    EVENT_STATUS = (
        (CREATED, 'created'),
        (INPROGRESS, 'in_progress'),
        (FINISHED, 'finished')
    )

    event_status = models.CharField(max_length=20, choices=EVENT_STATUS)

    def __str__(self):
        return f'{self.event_status}'


class Event(models.Model):

    name = models.CharField(max_length=30, null=True, blank=True)
    support_contact = models.ForeignKey(to=User, on_delete=models.CASCADE)
    client = models.ForeignKey(to=Client, on_delete=models.CASCADE)

    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now_add=True)

    event_status = models.ForeignKey(to=EventStatus, on_delete=models.CASCADE)

    attendees = models.IntegerField(default=0)
    event_date = models.DateTimeField(auto_now_add=False)

    notes = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'{Client.objects.get(id=self.client.id)} {self.date_created}'



