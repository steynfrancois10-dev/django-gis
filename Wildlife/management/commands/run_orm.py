from django.core.management.base import BaseCommand
from Wildlife.models import Property
from Wildlife.models import Province
from django.db.models import Q
from django.db.models import Count
from Wildlife.models import AnnualPopulation, Taxon, Property
from django.db.models import Sum
from Wildlife.models import Organisation

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
        
    
    def function_5(self):
        """Count distinct species for 'Zakki Property'"""
        print("\n5. Species count for 'Zakki Property':")

        try:
            zakki_property = Property.objects.get(name__iexact='Zakki Property')
        except Property.DoesNotExist:
            print("   Property 'Zakki Property' not found.")
            return

        species_count = AnnualPopulation.objects.filter(
            property=zakki_property
        ).values('taxon').distinct().count()

        print(f"   Number of distinct species: {species_count}")

    def function_6(self):
        """Identify organisation with largest total area available to species"""
        print("\n6. Organisation with largest total area:")

        org_areas = AnnualPopulation.objects.values(
            'property__organisation__id', 'property__organisation__name'
        ).annotate(
            total_area=Sum('area_available_to_species')
        ).order_by('-total_area')

        if org_areas:
            top_org = org_areas[0]
            print(f"   Organisation: {top_org['property__organisation__name']}")
            print(f"   Total area available to species: {top_org['total_area']}")
        else:
            print("   No organisations or areas found.")

    def function_7(self):
        """Identify property with most distinct species"""
        print("\n7. Property with most distinct species:")

        property_species_counts = AnnualPopulation.objects.values(
            'property__id', 'property__name'
        ).annotate(
            species_count=Count('taxon', distinct=True)
        ).order_by('-species_count')

        if property_species_counts:
            top_property = property_species_counts[0]
            print(f"   Property: {top_property['property__name']}")
            print(f"   Number of distinct species: {top_property['species_count']}")
        else:
            print("   No properties or species found.")
    

    def handle(self, *args, **options):
        """Logic of the command"""
        self.function_1()
        self.function_2()
        self.function_3()
        self.function_4()
        self.function_5()
        self.function_6()
        self.function_7()