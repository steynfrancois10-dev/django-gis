from django.core.management.base import BaseCommand
from Wildlife.models import Property
from Wildlife.models import Province
from django.db.models import Q
from django.db.models import Count
from Wildlife.models import AnnualPopulation, Taxon
from django.db.models import Sum

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

    def function_3(self):
        """Display organisation and property count per province"""
        print("\n3. Organisation and Property Count per Province:")

        provinces = Province.objects.annotate(
            org_count=Count('organisation', distinct=True),
            prop_count=Count('property', distinct=True)
        ).filter(
            Q(organisation__isnull=False) | Q(property__isnull=False)
        ).order_by('name')

        if provinces.exists():
            for i, province in enumerate(provinces, start=1):
                print(f"   {i}. {province.name}: {province.org_count} organisation(s), {province.prop_count} propert(y/ies)")
        else:
            print("   No provinces found.")

    def function_4(self):
        """Annual population for Acinonyx jubatus in 2021"""
        print("\n4. Annual population for Acinonyx jubatus (2021):")

        try:
            cheetah_taxon = Taxon.objects.get(scientific_name__iexact='Acinonyx jubatus')
        except Taxon.DoesNotExist:
            print("   No taxon found for Acinonyx jubatus.")
            return

        population_data = AnnualPopulation.objects.filter(
            taxon=cheetah_taxon,
            year=2021
        ).aggregate(
            total_males=Sum('adult_male'),
            total_females=Sum('adult_female')
        )

        total_males = population_data['total_males'] or 0
        total_females = population_data['total_females'] or 0

        print(f"   Total adult males: {total_males}")
        print(f"   Total adult females: {total_females}")
        print(f"   Total individuals: {total_males + total_females}")
        


    def handle(self, *args, **options):
        """Logic of the command"""
        self.function_1()
        self.function_2()
        self.function_3()
        self.function_4()
