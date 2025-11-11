from django.core.management.base import BaseCommand
from Wildlife.models import Property

class Command(BaseCommand):
    help = "Run Wildlife ORM"

    def function_1(self):
        """Get properties by type"""
        print("1. Get properties by type")
        # implement your code
        properties = Property.objects.filter(
            property_type__name__in=['Private', 'Community']
        )

        if properties.exists():
            for prop in properties:
                print(f"- {prop.name} ({prop.property_type.name})")
        else:
            print("No properties found with type 'Private' or 'Community'.")

    def function_2(self):
        """Get provinces with organisations or properties"""
        print("2. Get provinces with organisations or properties")
        # implement your code

    def handle(self, *args, **options):
        """Logic of the command"""
        self.function_1()
        self.function_2()


