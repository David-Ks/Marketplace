import json


class UserCart:
    def __init__(self, request):
        self.request = request

    def get_cart(self):
        userCart = self.request.COOKIES.get('cart')
        if not userCart:
            userCart = []
        else:
            userCart = userCart[1:-1]
            userCart = userCart.replace("\'", "\"").split('}, ')

            newCart = []
            for cart in userCart:
                if not cart:
                    continue
                if cart[-1] != "}":
                    cart += "}"
                newCart.append(json.loads(cart))

            userCart = newCart

        return userCart

    def add_to_cart(self, data):
        cartItems = self.get_cart()

        haveThatItem = False
        for item in cartItems:
            if data['barcode'] == item['barcode']:  # If that item exists
                item['count'] = float(item['count']) + float(data['count'])
                if (item['count'] * 10) % 10 == 0:  # mb not float
                    item['count'] = int(item['count'])
                haveThatItem = True

        if not haveThatItem:
            cartItems.append(data)

        return cartItems

    def remove_cart_item(self, card_barcode):
        cartItems = self.get_cart()

        index = 0
        for item in cartItems:
            if item['barcode'] == card_barcode:
                cartItems.pop(index)
                break
            index += 1

        return cartItems


class UserSavedCard:
    def __init__(self, request):
        self.request = request

    def get_saves(self):
        cards = self.request.COOKIES.get('saves')
        if not cards or len(cards) <= 2:
            cards = []
        else:
            cards = cards[1:-1].replace("\'", "")
            cards = list(map(int, cards.split(', ')))

        return cards

    def add_to_saves(self, data):
        cards = self.get_saves()

        hasThatSaveItem = False
        for card in cards:
            if card and data and int(card) == int(data):
                hasThatSaveItem = True
                break
        if not hasThatSaveItem:
            if data:
                cards.append(int(data))

        return cards

    def remove_saves_item(self, card_barcode):
        cards = self.get_saves()

        for card in cards:
            if int(card) == int(card_barcode):
                cards.remove(card)

        return cards
