import uuid
from django.db.models import Q
from django.db import IntegrityError
from django.apps import apps
from django.db import models


def create_anonymous_user():
    from django.contrib.auth import get_user_model

    user = get_user_model()
    anonymous_user = None

    while True:
        # Generate a secure unique string
        security_string = str(uuid.uuid4())[:5]
        anonymous_username = f'Anonymous-{security_string}'

        try:
            # Create an anonymous user and customized user model fields
            anonymous_user = user.objects.create_user(
                username=anonymous_username,
                first_name='Anonymous',
                last_name=security_string,
                password=None,
                email=None
            )

            break
        except IntegrityError:
            continue

    return anonymous_user


class TableGenerator:
    """
    A class used to generate a table from a model.
    Rows is a list of the boolean fields.
    Cols is a list from a choice list.
    Both Rows and Cols are from the same model.

    Returns a table with a count of row/col cross-reference and a uuid's list for get request
    (UUID field is required in the model)

    Usage example:

    View:
        cost_types = [key for key, value in services.choices.cost_types.items()]
        dimensions = services.aux_lists.dimension_target
        dimensions_table = services.generators.TableGenerator("Solution", "cost_type", dimensions, cost_types).table()

    Template:
        {% load core_template_tags %}
        <table class="table table-bordered table-sm table-striped text-center mt-3">
            <thead>
                <tr>
                    <th scope="col">Dimension</th>
                    <th scope="col">0 cost <br> (time/effort/material)</th>
                    <th scope="col">$ <br>(up to 1.000 USD)</th>
                    <th scope="col">$$ <br>(1.000 to 50.000 USD)</th>
                    <th scope="col">$$$ <br>(50.000 to 500.000 USD)</th>
                    <th scope="col">$$$$ <br>(over 500.000 USD)</th>
                </tr>
            </thead>

            <tbody>
                {% for dimension, cost_data in dimensions_table.items %}
                    <tr>
                        <th>{{ dimension|replace:"_, "|title }}</th>
                        {% for cost, solution_uuids in cost_data.items %}
                            <td>
                                {% if solution_uuids.count != 0 %}
                                    <a href="{% url 'solutions' %}?uuids={{ solution_uuids.uuids }}">
                                        <span class="badge badge-pill badge-primary">
                                            {{ solution_uuids.count }} Solution{{ solution_uuids.count|pluralize }}
                                        </span>
                                    </a>
                                {% endif %}
                            </td>
                        {% endfor %}
                    </tr>
                {% endfor %}
            </tbody>
        </table>
    """

    def __init__(self, model:str, col_name:str, rows_data:list, cols_data:list):
        self.model = model  # model name
        self.col_name = col_name  # name of field that has the dropdown selection in the model
        self.rows_data = rows_data  # List of names of fields that will comprise the rows
        self.cols_data = cols_data  # List of references of choices from the choice field

    def table(self):
        """
        Generates the table based on given parameters
        """
        output_table = {}
        model_class = apps.get_model('core', self.model)  # 'core' = your app
        for row in self.rows_data:
            output_table[row] = {}
            for col in self.cols_data:
                kwargs = {row: True, self.col_name: col}
                queryset = model_class.objects.filter(**kwargs)
                output_table[row][col] = {
                    'uuids': ','.join(str(item.uuid) for item in queryset),
                    'count': queryset.count()
                }

        return output_table


def build_query(q, search_fields):
    query = Q()  # Instantiate a Q object to build complex queries
    split_q = q.split()  # Split the query string into separate terms
    for field in search_fields:
        for term in split_q:
            query |= Q(**{f'{field}__icontains': term})  # For each term in each search field, add an 'icontains' lookup
    return query


def rate_compare(a, b):
    if a.avg_rating is None:
        return -1
    elif b.avg_rating is None:
        return 1
    else:
        return b.avg_rating - a.avg_rating


def collect_boolean_fieldnames(model_name, instance):
    fieldnames = []
    model = apps.get_model('core', model_name)
    for field in model._meta.fields:  # noqa
        if isinstance(field, models.BooleanField):
            if getattr(instance, field.name) == True:  # Check if BooleanField value is True
                fieldnames.append(field.name)
    return fieldnames
