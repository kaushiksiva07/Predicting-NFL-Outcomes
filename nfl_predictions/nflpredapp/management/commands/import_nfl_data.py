from django.core.management.base import BaseCommand
from nflpredapp.data_processing import main_function, data_already_exists  # Import your data processing script/function

class Command(BaseCommand):
    help = 'Import and process NFL data'

    def handle(self, *args, **options):
        self.stdout.write("Starting data import...")
        if data_already_exists():
            self.stdout.write("Data already exists. No import necessary.")
        else:
            main_function()  # Call your main data processing function
            self.stdout.write("Data import completed successfully.")