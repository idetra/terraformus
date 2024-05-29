import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Avg
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.text import slugify

from terraformus.core.services.choices import cost_types, life_cycle_types, resource_types, external_asset
from terraformus.core.services import help_text as ht, generators


class User(AbstractUser):

    def delete(self, *args, **kwargs):
        """
        Save all data on a new generated anonymous user
        """
        superuser = generators.create_anonymous_user()

        self.solution_set.all().update(user=superuser)
        self.strategy_set.all().update(user=superuser)
        self.rating_set.all().update(author=superuser)
        self.ratingreply_set.all().update(author=superuser)
        self.report_set.all().update(author=superuser)

        super().delete(*args, **kwargs)  # Delete the actual user


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    biography = models.TextField(max_length=5000, null=True, blank=True)

    def __str__(self):
        return self.user.username


# Solutions ------------------------------------------------------------------------------------------------------------


class Solution(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, unique=True, help_text=ht.solution_ht['title'])
    slug = models.SlugField(max_length=255, unique=True)
    subtitle = models.CharField(max_length=255, help_text=ht.solution_ht['subtitle'])
    goal = models.TextField(help_text=ht.solution_ht['goal'])
    # solution_type ----------------------------------------------------------------------------------------------------
    automation = models.BooleanField(default=False, help_text=ht.sol_type_ht['automation'])
    infrastructure = models.BooleanField(default=False, help_text=ht.sol_type_ht['infrastructure'])
    # population target ------------------------------------------------------------------------------------------------
    extreme_poverty = models.BooleanField(default=False, help_text=ht.sol_population_target_ht['extreme_poverty'])
    lower_class = models.BooleanField(default=False, help_text=ht.sol_population_target_ht['lower_class'])
    middle_class = models.BooleanField(default=False, help_text=ht.sol_population_target_ht['middle_class'])
    upper_class = models.BooleanField(default=False, help_text=ht.sol_population_target_ht['upper_class'])
    # dimension_target -------------------------------------------------------------------------------------------------
    individual = models.BooleanField(default=False, help_text=ht.sol_dimension_target_ht['individual'])
    apartment = models.BooleanField(default=False, help_text=ht.sol_dimension_target_ht['apartment'])
    house = models.BooleanField(default=False, help_text=ht.sol_dimension_target_ht['house'])
    apartment_building = models.BooleanField(default=False, help_text=ht.sol_dimension_target_ht['apartment_building'])
    street = models.BooleanField(default=False, help_text=ht.sol_dimension_target_ht['street'])
    house_complex = models.BooleanField(default=False, help_text=ht.sol_dimension_target_ht['house_complex'])
    neighborhood = models.BooleanField(default=False, help_text=ht.sol_dimension_target_ht['neighborhood'])
    town = models.BooleanField(default=False, help_text=ht.sol_dimension_target_ht['town'])
    city = models.BooleanField(default=False, help_text=ht.sol_dimension_target_ht['city'])
    county = models.BooleanField(default=False, help_text=ht.sol_dimension_target_ht['county'])
    state = models.BooleanField(default=False, help_text=ht.sol_dimension_target_ht['state'])
    country = models.BooleanField(default=False, help_text=ht.sol_dimension_target_ht['country'])
    continent = models.BooleanField(default=False, help_text=ht.sol_dimension_target_ht['continent'])
    planet = models.BooleanField(default=False, help_text=ht.sol_dimension_target_ht['planet'])
    # un_target --------------------------------------------------------------------------------------------------------
    no_poverty = models.BooleanField(default=False, help_text=ht.sol_un_target_ht['no_poverty'])
    zero_hunger = models.BooleanField(default=False, help_text=ht.sol_un_target_ht['zero_hunger'])
    good_health_and_well_being = models.BooleanField(default=False, help_text=ht.sol_un_target_ht['good_health_and_well_being'])
    quality_education = models.BooleanField(default=False, help_text=ht.sol_un_target_ht['quality_education'])
    gender_equality = models.BooleanField(default=False, help_text=ht.sol_un_target_ht['gender_equality'])
    clean_water_and_sanitation = models.BooleanField(default=False, help_text=ht.sol_un_target_ht['clean_water_and_sanitation'])
    affordable_and_clean_energy = models.BooleanField(default=False, help_text=ht.sol_un_target_ht['affordable_and_clean_energy'])
    decent_work_and_economic_growth = models.BooleanField(default=False,help_text=ht.sol_un_target_ht['decent_work_and_economic_growth'])
    industry_innovation_and_infrastructure = models.BooleanField(default=False, help_text=ht.sol_un_target_ht['industry_innovation_and_infrastructure'])
    reduced_inequality = models.BooleanField(default=False, help_text=ht.sol_un_target_ht['reduced_inequality'])
    sustainable_cities_and_communities = models.BooleanField(default=False,help_text=ht.sol_un_target_ht['sustainable_cities_and_communities'])
    responsible_consumption_and_production = models.BooleanField(default=False, help_text=ht.sol_un_target_ht['responsible_consumption_and_production'])
    climate_action = models.BooleanField(default=False, help_text=ht.sol_un_target_ht['climate_action'])
    life_below_water = models.BooleanField(default=False, help_text=ht.sol_un_target_ht['life_below_water'])
    life_on_land = models.BooleanField(default=False, help_text=ht.sol_un_target_ht['life_on_land'])
    peace_justice_and_strong_institutions = models.BooleanField(default=False, help_text=ht.sol_un_target_ht['peace_justice_and_strong_institutions'])
    partnerships_for_the_goals = models.BooleanField(default=False, help_text=ht.sol_un_target_ht['partnerships_for_the_goals'])
    # sector -----------------------------------------------------------------------------------------------------------
    housing = models.BooleanField(default=False, help_text=ht.sol_sector_ht['housing'])
    food = models.BooleanField(default=False, help_text=ht.sol_sector_ht['food'])
    energy = models.BooleanField(default=False, help_text=ht.sol_sector_ht['energy'])
    water = models.BooleanField(default=False, help_text=ht.sol_sector_ht['water'])
    health = models.BooleanField(default=False, help_text=ht.sol_sector_ht['health'])
    communication = models.BooleanField(default=False, help_text=ht.sol_sector_ht['communication'])
    education = models.BooleanField(default=False, help_text=ht.sol_sector_ht['education'])
    transportation = models.BooleanField(default=False, help_text=ht.sol_sector_ht['transportation'])
    security = models.BooleanField(default=False, help_text=ht.sol_sector_ht['security'])
    governance = models.BooleanField(default=False, help_text=ht.sol_sector_ht['governance'])

    cost_type = models.PositiveSmallIntegerField(choices=cost_types, default=cost_types[0], help_text=ht.solution_ht['cost_type'])
    update = models.TextField(help_text=ht.solution_ht['update'])
    upgrade = models.TextField(help_text=ht.solution_ht['upgrade'])
    scale_up = models.TextField(help_text=ht.solution_ht['scale_up'])
    depends_on = models.ManyToManyField('self', blank=True, symmetrical=False, related_name='dependencies', help_text=ht.solution_ht['depends_on'])
    derives_from = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='derived_solutions', help_text=ht.solution_ht['derives_from'])

    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)
    banned = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def average_rating(self):
        """returns the average rating for each content"""
        return Rating.objects.filter(solution=self).aggregate(avg_rating=Avg('rate'))["avg_rating"] or 0

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        return super().save(*args, **kwargs)


class ExternalAsset(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    solution = models.ForeignKey('Solution', on_delete=models.CASCADE, null=True, blank=True)
    strategy = models.ForeignKey('Strategy', on_delete=models.CASCADE, null=True, blank=True)
    type = models.CharField(max_length=3, choices=external_asset, default=external_asset['doc'], help_text=ht.ext_asset_ht['type'])
    title = models.CharField(max_length=255, help_text=ht.ext_asset_ht['title'])
    url = models.URLField(help_text=ht.ext_asset_ht['url'])

    def __str__(self):
        return self.title


class LifeCycle(models.Model):
    """
    Added through a button with its own crud/view
    """
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    solution = models.ForeignKey('Solution', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    type = models.CharField(max_length=2, choices=life_cycle_types,default=life_cycle_types['b'])
    total_duration = models.TextField(help_text=ht.life_cycle_ht['total_duration'])
    description = models.TextField(help_text=ht.life_cycle_ht['description'])

    def __str__(self):
        return f"{self.get_type_display()} - {self.title} - {self.solution.title}"


class LifeCycleInput(models.Model):
    """
    crud in inline form of LifeCycle
    """
    lifecycle = models.ForeignKey('LifeCycle', on_delete=models.CASCADE)
    resource_name = models.CharField(max_length=255, help_text=ht.life_cycle_input_ht['resource_name'])
    resource_type = models.CharField(max_length=2, choices=resource_types, help_text=ht.life_cycle_input_ht['resource_type'])
    unit = models.CharField(max_length=255, help_text=ht.life_cycle_input_ht['unit'])
    quantity = models.IntegerField(help_text=ht.life_cycle_input_ht['quantity'])
    reference_cost = models.IntegerField(help_text=ht.life_cycle_input_ht['reference_cost'])
    notes = models.TextField(help_text=ht.life_cycle_input_ht['notes'], null=True, blank=True)

    def __str__(self):
        return self.resource_name


class LifeCycleWaste(models.Model):
    """
    crud in inline form of LifeCycle
    """
    lifecycle = models.ForeignKey('LifeCycle', on_delete=models.CASCADE)
    waste_type = models.TextField(help_text=ht.life_cycle_waste_ht['waste_type'])
    reusable = models.BooleanField(default=False, help_text=ht.life_cycle_waste_ht['reusable'])
    recyclable = models.BooleanField(default=False, help_text=ht.life_cycle_waste_ht['recyclable'])
    cradle2cradle = models.BooleanField(default=False, help_text=ht.life_cycle_waste_ht['cradle2cradle'])
    unit = models.CharField(max_length=255, help_text=ht.life_cycle_waste_ht['unit'])
    quantity = models.IntegerField(help_text=ht.life_cycle_waste_ht['quantity'])
    reference_cost = models.IntegerField(help_text=ht.life_cycle_waste_ht['reference_cost'])
    destination_method = models.TextField(help_text=ht.life_cycle_waste_ht['destination_method'])
    notes = models.TextField(help_text=ht.life_cycle_waste_ht['notes'], null=True, blank=True)

    def __str__(self):
        return self.waste_type


# Strategy -------------------------------------------------------------------------------------------------------------


class Strategy(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, unique=True, help_text=ht.strategy_ht['title'])
    slug = models.SlugField(max_length=255, unique=True)
    goal = models.TextField(help_text=ht.strategy_ht['goal'])
    definitions = models.TextField(help_text=ht.strategy_ht['definitions'])
    solutions = models.ManyToManyField('StrategySolution', help_text=ht.strategy_ht['solutions'])

    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)
    banned = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def average_rating(self):
        """returns the average rating for each content"""
        return Rating.objects.filter(content=self).aggregate(avg_rating=Avg('rate'))["avg_rating"] or 0

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Strategies'


class StrategySolution(models.Model):
    solution = models.OneToOneField(Solution, on_delete=models.CASCADE)
    notes = models.TextField(help_text=ht.strategy_solution_ht['notes'])

    def __str__(self):
        return self.solution.title


# Rating, Rating reply & Report ----------------------------------------------------------------------------------------


class Rating(models.Model):
    STAR_RATING = tuple((i, str(i)) for i in range(1, 11))

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    solution = models.ForeignKey('Solution', on_delete=models.CASCADE, null=True, blank=True)
    strategy = models.ForeignKey('Strategy', on_delete=models.CASCADE, null=True, blank=True)
    rate = models.PositiveSmallIntegerField(choices=STAR_RATING, default=1)
    comment = models.TextField()
    last_edited = models.DateField(auto_now=True)

    def __str__(self):
        return f"{self.user}"


class RatingReply(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.OneToOneField(Rating, on_delete=models.CASCADE, related_name='rating_reply')
    comment = models.TextField()
    last_edited = models.DateField(auto_now=True)

    class Meta:
        verbose_name_plural = "Rating Replies"

    def __str__(self):
        return f"{self.user}"


class Report(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    solution = models.ForeignKey('Solution', on_delete=models.CASCADE, null=True, blank=True)
    strategy = models.ForeignKey('Strategy', on_delete=models.CASCADE, null=True, blank=True)
    comment = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.user}"


# User -----------------------------------------------------------------------------------------------------------------


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()