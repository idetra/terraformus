from django import template


register = template.Library()


@register.simple_tag
def main_url_two_params(param1, value1, param2, value2, urlencode=None):
    """
    Persists any GET request that needs to store and render again its two first parameters.
    Used for pagination persistence when another form (like filter) runs on the same data set
    """
    url = f'?{param1}={value1}&{param2}={value2}'

    if urlencode:
        querystring = urlencode.split('&')
        filtered_querystring = filter(lambda p: p.split('=')[0] not in [param1, param2], querystring)
        encoded_querystring = '&'.join(filtered_querystring)
        if encoded_querystring:
            url = f'{url}&{encoded_querystring}'
        else:
            url = f'{url}'

    return url


@register.filter
def get_item(form, key):
    """
    Retrieves a specific item from a form's fields using the provided key.

    Parameters:
        form (django.forms.Form): The form from which to retrieve the item.
        key (str): The key to identify the item to retrieve.

    Returns:
        The requested item if found, otherwise None.
    """
    return form.fields.get(key)


@register.filter
def replace(value, args):
    """
    Used to replace underscores, etc. with space on template tag calls, like {{ item }}

    Usage: {{ item|replace:"_, "|title }} or {{ item|replace:"_, "|capfirst }}

    Second parameter (title, capfirst) is optional

    """
    search, replace_with = args.split(',')
    return value.replace(search, replace_with)