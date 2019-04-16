

import json

class Stock():
    SKUS_JSON = "[{ \"product_name\" : \"A\", \"price\" : 50, \"discount_purchase\" : 3, \"discount_receive\" : 130},\
                    { \"product_name\" : \"B\", \"price\" : 30, \"discount_purchase\" : 2, \"discount_receive\" : 45},\
                    { \"product_name\" : \"C\", \"price\" : 20}, \
                    { \"product_name\" : \"D\", \"price\" : 15}]"
    


class Skus(object):
    def __init__(self, product_name, price, discount_purchase=None, discount_receive=None):
        self.product_name = product_name
        self.price = price
        self.discount_purchase = discount_purchase
        self.discount_receive = discount_receive
        self.number_of_items = 1

    def get_product_name(self):
        return self.product_name

    def get_price(self):
        if self.discount_purchase:
            if self.number_of_items >= self.discount_purchase:
                if (self.number_of_items % self.discount_purchase) == 0:
                    return (self.discount_receive * (self.number_of_items / self.discount_purchase))
                else:
                     return (self.discount_receive * (self.number_of_items // self.discount_purchase) + ((self.number_of_items % self.discount_purchase) * self.price))

        return self.number_of_items * self.price

    def get_number_of_items(self):
        return self.number_of_items

    def get_discount_purchase(self):
        return self.discount_purchase

    def get_discount_receive(self):
        return self.discount_receive
    
    def increment_number_of_items(self):
        self.number_of_items += 1

class Basket():

    def __init__(self):
        self.items_list = list()

    def add_item(self, item):
        found = False
        index = 0
        for el in self.items_list:
            index += 1
            if el.get_product_name() == item.get_product_name():
                found = True
                break

        if found:
            self.items_list[index - 1].increment_number_of_items()
        else:
            self.items_list.append(item)
    
    def get_items(self):
        return self.items_list
    
    def get_total(self):
        return sum(map(lambda item : item.get_price(), self.items_list))
    
    def checkout(self, skus_string):
        stock = []
        data = json.loads(Stock.SKUS_JSON)
        for dt in data:
            skus = Skus(**dt)
            stock.append(skus)
        
        for skus_name in skus_string:
            skus_objects = list(filter(lambda item : item.product_name == skus_name, stock))
            if len(skus_objects) == 0:
                return -1
            else:
                self.add_item(skus_objects[0])

        return self.get_total()
    

# noinspection PyUnusedLocal
# skus = unicode string
def checkout(skus):
    basket = Basket()
    return basket.checkout(skus)
    



