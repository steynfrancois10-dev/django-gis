from django.core.management.base import BaseCommand
from Wildlife.models import Property
from Wildlife.models import Province
from django.db.models import Q



class Command(BaseCommand):
    help = "Run Wildlife ORM"

    def function_1(self):
        """Get properties by type"""
        print("1. Properties by type ('Private' or 'Community'):")
        properties = Property.objects.filter(
            property_type__name__in=['Private', 'Community']
        ).order_by('name')  # optional: alphabetically

        if properties.exists():
            for i, prop in enumerate(properties, start=1):
                print(f"   {i}. {prop.name} ({prop.property_type.name})")
        else:
            print("   No properties found.")

    def function_2(self):
        """Get provinces with organisations or properties"""
        print("\n2. Provinces with organisations or properties:")
        
        provinces = Province.objects.filter(
            Q(organisation__isnull=False) | Q(property__isnull=False)
        ).distinct().order_by('name')  # optional: alphabetical

        if provinces.exists():
            for i, province in enumerate(provinces, start=1):
                print(f"   {i}. {province.name}")
        else:
            print("   No provinces found.")

    def handle(self, *args, **options):
        """Logic of the command"""
        self.function_1()
        self.function_2()


