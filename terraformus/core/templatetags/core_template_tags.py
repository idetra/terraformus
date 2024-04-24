from django import template


register = template.Library()


@register.simple_tag
def main_url_two_params(param1, value1, param2, value2, urlencode=None):
    """Persists any GET request that needs to store and render again its two first parameters.
    Used for pagination persistence when another form (like filter) runs on the same data set"""
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



