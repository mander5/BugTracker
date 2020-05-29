from django.db import models
from django.urls import reverse
from django.conf import settings
import misaka
from projects.models import Project
# Create your models here.
from django.contrib.auth import get_user_model
User = get_user_model()

class Ticket(models.Model):
    user = models.ForeignKey(User,related_name='tickets', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
    message = models.TextField()
    message_html = models.TextField(editable=False)
    project = models.ForeignKey(Project, related_name='tickets', null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.message

    def save(self,*args,**kwargs):
        self.message_html = misaka.html(self.message)
        super().save(*args,**kwargs)

    def get_absolute_url(self):
        return reverse('tickets:single',kwargs={'username':self.user.username,'pk':self.pk})

    class Meta:
        ordering = ['-created_at']
        unique_together = ['user','message']
