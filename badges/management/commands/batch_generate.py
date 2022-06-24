from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from urllib import parse

from post_office import mail

from badges.models import Badge, STATUS
from badges import utils

class Command(BaseCommand):
    help = 'Generates pending badges in batch'

    def add_arguments(self, parser):
        parser.add_argument('--size', type=int, default=50, help='Number of badges to generate')

    def handle(self, *args, **options):
        self.stdout.write('Generating badges...')
        size = options['size']
        self.stdout.write(f'Batch size is {size}')
        pending_badges = Badge.objects.filter(status=STATUS.queued)[:size]
        for badge in pending_badges:
            success, result = utils.generate_pdf(
                template_path=badge.template.template_file.name,
                name=badge.person.name,
                coords_y=badge.template.coords_y,
                result_path=badge.template.subdirectory,
                r = badge.template.color_r,
                g = badge.template.color_g,
                b = badge.template.color_b,
                )
            self.stdout.write(result)
            if success:
                badge.status=STATUS.created
                badge.url = settings.BASE_URL+result
                context = {
                    "url" : parse.quote(badge.url,safe='/:'),
                    "event" : badge.template.event,
                    "org_id" : badge.template.org_id,
                    "year" : badge.template.event_year,
                    "month": badge.template.event_month,
                }
                try:
                    self.stdout.write(f'Enviando mail a {badge.person.email}')
                    mail.send([badge.person.email],settings.DEFAULT_FROM_EMAIL,badge.template.email_template.name,context, priority='now')
                    badge.status=STATUS.sent
                except Exception as e:
                    self.stdout.write(f'Error sending email: {e}')
                    badge.status=STATUS.failed
                finally:
                    badge.save()       

        self.stdout.write('Done')



