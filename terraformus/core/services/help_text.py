solution_ht = {
    'title': 'An identifiable unique name for this solution',
    'subtitle': 'An extension of the title you gave to your solution',
    'goal': 'What problem(s) your solution aims to solve',
    'cost_type': 'What is the cost tier or your solution',
    'update': 'How to modernize this solution',
    'upgrade': 'How to enhanced this solution',
    'scale_up': 'How to expand this solution',
    'depends_on': 'FORM DEPENDENT',
    'derives_from': 'If your solution is branching out from another solution, refer it above.',
}

sol_type_ht = {
    'automation': 'Your solution automates one or more processes',
    'infrastructure': 'Your solution improves or creates known infrastructure',
}

sol_dimension_target_ht = {
    'individual': 'For small or personal solutions',
    'apartment': 'Solutions for small homes',
    'house': 'Solutions for houses',
    'apartment_building': 'For collective housing solutions',
    'street': 'Solutions for your entire street',
    'house_complex': 'Solutions for a housing complex',
    'neighborhood': 'Solutions for an entire neighborhood',
    'town': 'Solutions that impact a town',
    'city': 'Solutions for an entire city',
    'county': 'Solutions for a geographic county',
    'state': 'Solutions that impact an entire state',
    'country': 'Solutions that impact an entire country',
    'continent': 'solutions that impact a continent',
    'planet': 'Solutions for our entire planet',
}

sol_un_target_ht = {
    'no_poverty': 'Addresses poverty',
    'zero_hunger': 'Stops hunger',
    'good_health_and_well_being': 'Promotes health and well-being',
    'quality_education': 'Improves education',
    'gender_equality': 'Ensures gender equality',
    'clean_water_and_sanitation': 'Clean water and sanitation for all',
    'affordable_and_clean_energy': 'Affordable, clean energy',
    'decent_work_and_economic_growth': 'Decent work, economic growth',
    'industry_innovation_and_infrastructure': 'Builds industry and innovation',
    'reduced_inequality': 'Reduces inequality',
    'sustainable_cities_and_communities': 'Sustainable cities and communities',
    'responsible_consumption_and_production': 'Sustainable consumption and production',
    'climate_action': 'Takes climate action',
    'life_below_water': 'Protects life below water',
    'life_on_land': 'Protects life on land',
    'peace_justice_and_strong_institutions': 'Peace, justice, and strong institutions',
    'partnerships_for_the_goals': 'Builds global partnerships',
}

sol_sector_ht = {
    'housing': 'Related to housing solutions',
    'food': 'Related to food supply or production',
    'energy': 'Energy production or improvement',
    'water': 'Water supply or management',
    'health': 'Healthcare solutions',
    'communication': 'Improves communication',
    'education': 'Education-related solutions',
    'transportation': 'Mobility related solutions',
    'security': 'Generates or improves security',
    'governance': 'Creates or Enhances governance systems',
}

ext_asset_ht = {
    'type': 'Choose the type of asset your are referencing to your solution',
    'title': 'Give your asset a descriptive title',
    'url': 'Insert the link to the asset',
}

life_cycle_ht = {
    'title': 'Give the lifecycle a descriptive but concise name',
    'type': 'Also known as "phase" of a life cycle',
    'total_duration': 'How long will it take to execute this entire life cycle/phase',
    'description': 'Describe with as much detail as possible what and how this life cycle/phase intends to achieve its goals',
}

life_cycle_input_ht = {
    'resource_name': 'What is the name of this resource',
    'resource_type': 'IS this a tangible or human resource',
    'unit': 'What is the resource unit (man-hour, kilo, liter, meter, etc)',
    'quantity': 'How many units this input requires',
    'reference_cost': 'What is the cost for each unit described above',
    'notes': 'Insert any notes that can help contextualizing this input',
}

life_cycle_waste_ht = {
    'waste_type': 'What is the name of this waste',
    'reusable': 'Is this waste reusable',
    'recyclable': 'Is this waste recyclable',
    'cradle2cradle': 'Is this waste capable of returning to constituents components',
    'unit': 'What is the waste unit (kilo, liter, meter, etc)',
    'quantity': 'How many waste units will be generated',
    'reference_cost': 'What is the cost for each unit described above',
    'destination_method': 'How this waste will be disposed',
    'notes': 'Insert any notes that can help contextualizing this waste management',
}

strategy_ht = {
    'title': 'Give your strategy an identifiable unique name',
    'goal': 'Describe in details the problems this strategy aims to solve',
    'definitions': 'Define what is being achieved by combining the solutions provided that cannot be achieved by them separately',
    'solutions': 'What are the solutions that comprise this strategy',
}

strategy_solution_ht = {
    'title': 'FORM DEPENDENT + strategy_solution model does not have a title, only M2M to solutions',
    'notes': 'Contextualize this solution from the perspective of this strategy',
}