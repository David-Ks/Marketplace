from django import template

from shop.Services.cart import UserCart, UserSavedCard

register = template.Library()


@register.simple_tag(takes_context=True)
def get_cart_count(context):
    request = context['request']
    count = 0
    try:
        userCart = UserCart(request)
        count = len(userCart.get_cart())
    except Exception as e:
        print("Error:", e)
    return count


@register.simple_tag(takes_context=True)
def get_saved_cards(context):
    request = context['request']
    cards = UserSavedCard(request)
    return len(cards.get_saves())


@register.simple_tag()
def get_elem_by_id(arr, id):
    return arr[id]


@register.simple_tag()
def get_by_barcode_in_query(q, barcode):
    query = False
    try:
        query = q.get(barcode=barcode)
    except Exception as e:
        print("Error:", e)
    return query
