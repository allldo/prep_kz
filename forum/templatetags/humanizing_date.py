import datetime
from pytz import timezone
from django import template
from ..services import plural_time
from shop.service import get_customer

register = template.Library()


@register.simple_tag
def humanizing(request, value):
    """Removes all values of arg from the given string"""
    customer_timezone = timezone(get_customer(request).timezone)
    hDate = datetime.datetime.strptime(str(value), '%Y-%m-%d %H:%M:%S.%f%z').replace(tzinfo=customer_timezone)
    # TODO Захардкожено, надо поменять
    hDate = hDate + datetime.timedelta(hours=6)
    subtraction = (datetime.datetime.now().replace(tzinfo=customer_timezone) - hDate).seconds
    print(subtraction)
    if 120 < subtraction < 43200:
        divided_subtraction = subtraction/3600
        if divided_subtraction > 1:
            return plural_time(int(divided_subtraction), 'час')
        else:
            return plural_time(int(subtraction/60), 'минута')
    elif 86400 < subtraction < 172800:
        return 'вчера в ' + str(hDate).split(' ')[1].split('.')[0][:5]
    elif subtraction > 172800:
        return 'вчера в ' + str(hDate).split(' ')[1].split('.')[0][:5]
    else:
        return 'только что'



