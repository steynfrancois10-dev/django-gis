from django.test import TestCase
from django.contrib.auth.models import User
from django.db.models import Sum, Count, Q
from Wildlife.models import PropertyType, Province, Organisation, Property, Taxon, TaxonRank, AnnualPopulation

class WildlifeORMTests(TestCase):

    def setUp(self):
        # --- Property Types ---
        self.private_type = PropertyType.objects.create(name="Private")
        self.community_type = PropertyType.objects.create(name="Community")

        # --- Provinces ---
        self.province1 = Province.objects.create(name="Province A")
        self.province2 = Province.objects.create(name="Province B")

        # --- Organisations ---
        self.org1 = Organisation.objects.create(name="Org 1", province=self.province1)
        self.org2 = Organisation.objects.create(name="Org 2", province=self.province2)

        # --- Properties ---
        self.prop1 = Property.objects.create(
            name="Zakki Property",
            province=self.province1,
            property_type=self.private_type,
            organisation=self.org1
        )
        self.prop2 = Property.objects.create(
            name="Other Property",
            province=self.province2,
            property_type=self.community_type,
            organisation=self.org2
        )

        # --- Taxon Ranks ---
        self.rank_species = TaxonRank.objects.create(name="Species")

        # --- Taxa (Parent & Child) ---
        self.taxon_parent = Taxon.objects.create(scientific_name="Parent Taxon", taxon_rank=self.rank_species)
        self.taxon_child = Taxon.objects.create(scientific_name="Child Taxon", taxon_rank=self.rank_species, parent=self.taxon_parent)

        # --- Users ---
        self.user1 = User.objects.create_user(username="user1")
        self.user2 = User.objects.create_user(username="user2")

        # --- Annual Population ---
        AnnualPopulation.objects.create(
            year=2021,
            total=10,
            adult_male=4,
            adult_female=6,
            taxon=self.taxon_child,
            property=self.prop1,
            user=self.user1,
            area_available_to_species=100.0
        )
        AnnualPopulation.objects.create(
            year=2021,
            total=5,
            adult_male=2,
            adult_female=3,
            taxon=self.taxon_child,
            property=self.prop2,
            user=self.user2,
            area_available_to_species=50.0
        )

    # --- 1. Properties by Type ---
    def test_properties_by_type(self):
        properties = Property.objects.filter(property_type__name__in=['Private', 'Community'])
        self.assertEqual(properties.count(), 2)
        self.assertIn(self.prop1, properties)
        self.assertIn(self.prop2, properties)

    # --- 2. Provinces with Organisations or Properties ---
    def test_provinces_with_orgs_or_props(self):
        provinces = Province.objects.filter(
            Q(organisation__isnull=False) | Q(property__isnull=False)
        ).distinct()
        self.assertEqual(provinces.count(), 2)
        self.assertIn(self.province1, provinces)
        self.assertIn(self.province2, provinces)

    # --- 3. Organisation and Property Count per Province ---
    def test_org_and_property_count_per_province(self):
        provinces = Province.objects.annotate(
            org_count=Count('organisation', distinct=True),
            prop_count=Count('property', distinct=True)
        ).filter(
            Q(organisation__isnull=False) | Q(property__isnull=False)
        )
        counts = {p.name: (p.org_count, p.prop_count) for p in provinces}
        self.assertEqual(counts['Province A'], (1, 1))
        self.assertEqual(counts['Province B'], (1, 1))

    # --- 4. Annual population for a species in a year ---
    def test_annual_population_species_2021(self):
        population_data = AnnualPopulation.objects.filter(
            taxon__scientific_name__iexact='Child Taxon',
            year=2021
        ).aggregate(
            total_males=Sum('adult_male'),
            total_females=Sum('adult_female')
        )
        self.assertEqual(population_data['total_males'], 6)
        self.assertEqual(population_data['total_females'], 9)
        self.assertEqual(population_data['total_males'] + population_data['total_females'], 15)

    # --- 5. Species count for a given property ---
    def test_species_count_for_property(self):
        species_count = AnnualPopulation.objects.filter(property=self.prop1).values('taxon').distinct().count()
        self.assertEqual(species_count, 1)

    # --- 6. Organisation with largest total area ---
    def test_organisation_largest_total_area(self):
        org_areas = AnnualPopulation.objects.values(
            'property__organisation__id', 'property__organisation__name'
        ).annotate(
            total_area=Sum('area_available_to_species')
        ).order_by('-total_area')
        top_org = org_areas[0]
        self.assertEqual(top_org['property__organisation__name'], self.org1.name)
        self.assertEqual(top_org['total_area'], 100.0)

    # --- 7. Property with most distinct species ---
    def test_property_most_distinct_species(self):
        property_species_counts = AnnualPopulation.objects.values(
            'property__id', 'property__name'
        ).annotate(
            species_count=Count('taxon', distinct=True)
        ).order_by('-species_count')
        top_property = property_species_counts[0]
        self.assertEqual(top_property['property__name'], self.prop1.name)
        self.assertEqual(top_property['species_count'], 1)

    # --- 8. Property with highest total animal count ---
    def test_property_highest_animal_count(self):
        property_totals = AnnualPopulation.objects.values(
            'property__id', 'property__name'
        ).annotate(
            total_animals=Sum('total')
        ).order_by('-total_animals')
        top_property = property_totals[0]
        self.assertEqual(top_property['property__name'], self.prop1.name)
        self.assertEqual(top_property['total_animals'], 10)

    # --- 9. Province with highest adult male count ---
    def test_province_highest_adult_male_count(self):
        province_totals = AnnualPopulation.objects.values(
            'property__province__id', 'property__province__name'
        ).annotate(
            total_adult_males=Sum('adult_male')
        ).order_by('-total_adult_males')
        top_province = province_totals[0]
        self.assertEqual(top_province['property__province__name'], self.province1.name)
        self.assertEqual(top_province['total_adult_males'], 4)

    # --- 10. Taxon parent-child relationships ---
    def test_taxon_parent_child_relationships(self):
        self.assertEqual(self.taxon_child.parent, self.taxon_parent)
        children = Taxon.objects.filter(parent=self.taxon_parent)
        self.assertIn(self.taxon_child, children)

    # --- 11. Taxa without child taxa (leaf taxa) ---
    def test_leaf_taxa(self):
        all_taxa = Taxon.objects.all()
        leaf_taxa = [taxon for taxon in all_taxa if not Taxon.objects.filter(parent=taxon).exists()]
        self.assertIn(self.taxon_child, leaf_taxa)
        self.assertNotIn(self.taxon_parent, leaf_taxa)

    # --- 12. User with most Annual Population records ---
    def test_user_with_most_records(self):
        user_counts = AnnualPopulation.objects.values(
            'user__id', 'user__username'
        ).annotate(
            record_count=Count('id')
        ).order_by('-record_count')
        top_user = user_counts[0]
        self.assertEqual(top_user['user__username'], self.user1.username)
        self.assertEqual(top_user['record_count'], 1)



