from django.core.management.base import BaseCommand
from restaurant.models import Table


class Command(BaseCommand):
    help = "Create restaurant tables 1 to 5 if they do not exist"

    def handle(self, *args, **kwargs):

        for number in range(1, 6):

            table, created = Table.objects.get_or_create(
                table_number=number
            )

            if created:
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Created Table {number}: {table.qr_token}"
                    )
                )
            else:
                self.stdout.write(
                    self.style.WARNING(
                        f"Table {number} already exists: {table.qr_token}"
                    )
                )

        self.stdout.write(
            self.style.SUCCESS("All 5 tables are ready!")
        )