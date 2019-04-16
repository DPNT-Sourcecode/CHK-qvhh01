

import json


# class Stock():
#     SKUS_JSON = "[{ \"product_name\" : \"A\", \"price\" : 50, \"discounts\" : [ {\"discount_purchase\" : 3, \"discount_receive\" : 130}]},\
#                     { \"product_name\" : \"B\", \"price\" : 30, \"discounts\" : [ {\"discount_purchase\" : 2, \"discount_receive\" : 45}]},\
#                     { \"product_name\" : \"C\", \"price\" : 20}, \
#                     { \"product_name\" : \"D\", \"price\" : 15}]"
    
class Discount(object):
    def __init__(self, discount_purchase=None, discount_receive=None, ref_skus="", occurence=0, free=False):
        self.discount_purchase = discount_purchase
        self.discount_receive = discount_receive
        self.ref_skus = ref_skus
        self.free = free
        self.occurence = occurence

    def get_discount_purchase(self):
        return self.discount_purchase
    
    def get_discount_receive(self):
        return self.discount_receive
    
    def __str__(self):
        print('discount_purchase: {}, discount_receive: {}'.format(self.discount_purchase, self.discount_receive))

class Skus(object):
    def __init__(self, product_name, price):
        self.product_name = product_name
        self.price = price
        self.discounts = []
        self.number_of_items = 1

    def get_product_name(self):
        return self.product_name

    def get_price(self):
        result = -1
        total = -1
        for discount in self.discounts:
            print('Product name:{}'.format(self.product_name))
            print('total:{}'.format(total))
            print('result:{}'.format(result))
            if discount.discount_purchase and not(discount.free):
                if self.number_of_items >= discount.discount_purchase:
                    if (self.number_of_items % discount.discount_purchase) == 0:
                        total = (discount.discount_receive * (self.number_of_items / discount.discount_purchase))
                    else:
                        total = (discount.discount_receive * (self.number_of_items // discount.discount_purchase) + ((self.number_of_items % discount.discount_purchase) * self.price))
            if total != -1: 
                if result == -1 or result > total:
                    result = total
        if result != -1:
            return result
        else:
            return self.number_of_items * self.price
    
    def get_number_of_items(self):
        return self.number_of_items

    def add_discount(self, discount):
        self.discounts.append(discount)
    
    def get_discounts(self):
        return self.discounts

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
    
    def get_global_discount(self):
        total = 0
        for sku in self.items_list:
            for discount in sku.get_discounts():
                if discount.free and sku.number_of_items >= discount.discount_purchase:
                    total += [item.price * discount.occurence for item in self.items_list if item.product_name == discount.ref_skus][0]

        return total

    def checkout(self, skus_string):
        stock = build_stocks()
                
        for skus_name in skus_string:
            skus_objects = list(filter(lambda item : item.product_name == skus_name, stock))
            if len(skus_objects) == 0:
                return -1
            else:
                self.add_item(skus_objects[0])
        return self.get_total() - self.get_global_discount()
    

# noinspection PyUnusedLocal
# skus = unicode string
def checkout(skus):
    basket = Basket()
    return basket.checkout(skus)

def build_stocks():
    stock = []
    discount1 = Discount(discount_purchase=3, discount_receive=130)
    discount2 = Discount(discount_purchase=2, discount_receive=45)
    discount3 = Discount(discount_purchase=5, discount_receive=200)
    discount4 = Discount(discount_purchase=2, ref_skus="B", free=True, occurence=1)
    skus_a = Skus(product_name="A", price=50)
    skus_a.add_discount(discount1)
    skus_a.add_discount(discount3)
    skus_b = Skus(product_name="B", price=30)
    skus_b.add_discount(discount2)
    stock.append(skus_a)
    stock.append(skus_b)
    skus_c = Skus(product_name="C", price=20)
    skus_d = Skus(product_name="D", price=15)
    skus_e = Skus(product_name="E", price=40)
    skus_e.add_discount(discount4)
    stock.append(skus_c)
    stock.append(skus_d)
    stock.append(skus_e)
    return stock