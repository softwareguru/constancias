from django.contrib import admin

from django.urls import path
from django.shortcuts import redirect, render
from django import forms

from .models import BadgeTemplate, Person, Badge, STATUS
from badges import utils

import csv

import logging
logger = logging.getLogger(__name__)

admin.site.register(BadgeTemplate)
admin.site.register(Person)

class CsvImportForm(forms.Form):
    template_id = forms.IntegerField()
    csv_file = forms.FileField()

@admin.register(Badge)
class BadgeAdmin(admin.ModelAdmin):
    list_display = ['person', 'template','status']

    change_list_template = "badges/change_list.html"

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [     
            path('import-csv/', self.import_csv),
        ]
        return my_urls + urls

    def import_csv(self, request):
        if request.method == "POST":
            logger.info("importing csv")	

            csv_file = request.FILES["csv_file"]
            from io import StringIO
            content = StringIO(csv_file.read().decode('utf-8'))
            reader = csv.DictReader(content)
            template_id = request.POST.get("template_id")
            try:
                template = BadgeTemplate.objects.get(pk=template_id)
            except BadgeTemplate.DoesNotExist:
                self.message_user(request, "Could not find template with ID "+template_id)
                return redirect("..")

            for row in reader:
                email = row['email'].lower().strip()
                name = utils.fix_name(row['name'])

                person, created = Person.objects.get_or_create(email=email)
                person.name = name
                person.save()

                Badge.objects.create(person=person, template=template,status=STATUS.queued)

            self.message_user(request, "Your csv file has been imported")
            return redirect("..")

        form = CsvImportForm()
        payload = {"form": form}

        return render(request, "badges/csv_form.html", payload)
