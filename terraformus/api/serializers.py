from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers
from terraformus.core.models import Solution, ExternalAsset, LifeCycle, LifeCycleInput, LifeCycleWaste, Strategy, \
    StrategySolution


class LifeCycleInputSerializer(serializers.ModelSerializer):
    class Meta:
        model = LifeCycleInput
        fields = '__all__'


class LifeCycleWasteSerializer(serializers.ModelSerializer):
    class Meta:
        model = LifeCycleWaste
        fields = '__all__'


class LifeCycleSerializer(serializers.ModelSerializer):
    inputs = LifeCycleInputSerializer(source='lifecycleinput_set', many=True)
    wastes = LifeCycleWasteSerializer(source='lifecyclewaste_set', many=True)

    class Meta:
        model = LifeCycle
        exclude = ['id']


class ExternalAssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExternalAsset
        exclude = ['id']


class SolutionsSerializer(serializers.ModelSerializer):
    external_assets = ExternalAssetSerializer(source='externalasset_set', many=True)
    lifecycles = LifeCycleSerializer(source='lifecycle_set', many=True)
    user_full_name = serializers.SerializerMethodField()

    class Meta:
        model = Solution
        fields = [
            'title',
            'uuid',
            'user_full_name',
            'slug',
            'subtitle',
            'goal',
            'automation',
            'infrastructure',
            'individual',
            'apartment',
            'house',
            'apartment_building',
            'street',
            'house_complex',
            'neighborhood',
            'town',
            'city',
            'county',
            'state',
            'country',
            'continent',
            'planet',
            'no_poverty',
            'zero_hunger',
            'good_health_and_well_being',
            'quality_education',
            'gender_equality',
            'clean_water_and_sanitation',
            'affordable_and_clean_energy',
            'decent_work_and_economic_growth',
            'industry_innovation_and_infrastructure',
            'reduced_inequality',
            'sustainable_cities_and_communities',
            'responsible_consumption_and_production',
            'climate_action',
            'life_below_water',
            'life_on_land',
            'peace_justice_and_strong_institutions',
            'partnerships_for_the_goals',
            'housing',
            'food',
            'energy',
            'water',
            'health',
            'communication',
            'education',
            'transportation',
            'security',
            'governance',
            'cost_type',
            'update',
            'upgrade',
            'scale_up',
            'depends_on',
            'derives_from',
            'created_at',
            'edited_at',
            'external_assets',
            'lifecycles',
        ]

    @extend_schema_field(serializers.CharField)
    def get_user_full_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"


class StrategySolutionSerializer(serializers.ModelSerializer):
    solution = SolutionsSerializer()

    class Meta:
        model = StrategySolution
        fields = ['solution', 'notes']


class StrategySerializer(serializers.ModelSerializer):
    external_assets = ExternalAssetSerializer(source='externalasset_set', many=True)
    solutions = StrategySolutionSerializer(source='strategysolution_set', many=True)
    user_full_name = serializers.SerializerMethodField()

    class Meta:
        model = Strategy
        fields = [
            'title',
            'uuid',
            'user_full_name',
            'slug',
            'goal',
            'definitions',
            'solutions',
            'created_at',
            'edited_at',
            'external_assets',
        ]

    @extend_schema_field(serializers.CharField)
    def get_user_full_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"
