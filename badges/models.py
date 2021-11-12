from django.db import models

from django.db.models.deletion import PROTECT
from collections import namedtuple
from django.utils.translation import pgettext_lazy, gettext_lazy as _
from django.utils import timezone
from django.conf import settings

STATUS = namedtuple('STATUS', 'queued created sent failed')._make(range(4))

class BadgeTemplate(models.Model):
    event = models.CharField(max_length=250)
    role = models.CharField(max_length=250)
    subdirectory = models.CharField(max_length=50, default="")
    # LinkedIn organization ID, used for LinkedIn certificate. Default is Software Guru's id.
    org_id = models.IntegerField(default=794778)
    template_file = models.FileField(upload_to='pdf_templates')
    coords_x = models.IntegerField(blank=True, null=True)
    coords_y = models.IntegerField(blank=True, null=True)
    color_r = models.IntegerField(default=0, null=False)
    color_g = models.IntegerField(default=0, null=False)
    color_b = models.IntegerField(default=0, null=False)
    event_year = models.IntegerField(default=0, null=False)
    event_month = models.IntegerField(default=0, null=False)

    def __str__(self):
        return f'{self.event} - {self.role}' 

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        from pathlib import Path
        Path(settings.RESULTS_DIR+"/"+self.subdirectory).mkdir(parents=True, exist_ok=True)


class Person(models.Model):
    name = models.CharField(max_length=250)
    email = models.EmailField(max_length=250, unique=True)

    def __str__(self):
        return self.name

class Badge(models.Model):
    STATUS_CHOICES = [(STATUS.queued, _("queued")), (STATUS.created, _("created")), 
                      (STATUS.sent, _("sent")), (STATUS.failed, _("failed")), ]

    template = models.ForeignKey(
        BadgeTemplate, on_delete=PROTECT, related_name='template')
    person = models.ForeignKey(Person, on_delete=PROTECT, related_name='person')   
    status = models.PositiveSmallIntegerField(_("Status"),
        choices=STATUS_CHOICES, db_index=True, default=STATUS.queued)
    created = models.DateTimeField(auto_now_add=True, db_index=True)
    last_updated = models.DateTimeField(db_index=True, auto_now=True)
    url = models.URLField(max_length=250, blank=True, null=True)

    def __str__(self):
        return f'{self.person.name} - {self.template.event} - {self.template.role}'

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['template', 'person'], name='unique_badge'),
        ]


