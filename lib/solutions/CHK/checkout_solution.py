

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
        total = -1
        result = -1
        for discount in self.discounts:
            if discount.discount_purchase and not(discount.free):
                total = self.get_discount(discount)
            if total != -1: 
                if result == -1 or result > total:
                    print('ICI1111: {}'.format(total))
                    result = total
        if len(self.discounts) > 1:
            res = self.compute_discount()
            print('compute_discount :res {} result {}'.format(res, result))
            if result == -1 or result > res:
                    result = res
        if result != -1:
            return result
        else:
            return self.number_of_items * self.price

    def get_discount(self, discount):
        total = -1
        if self.number_of_items >= discount.discount_purchase:
            if (self.number_of_items % discount.discount_purchase) == 0:
                total = (discount.discount_receive * (self.number_of_items / discount.discount_purchase))
            else:
                total = (discount.discount_receive * (self.number_of_items // discount.discount_purchase) + 
                ((self.number_of_items % discount.discount_purchase) * self.price))

        return total

    def get_exact_match_discount(self, discount, reste):
        total = 0
        rescount = reste
        if self.number_of_items >= discount.discount_purchase:
            rescount = reste % discount.discount_purchase 
            if (rescount) == 0:
                total = (discount.discount_receive * (reste / discount.discount_purchase))
            else:
                total = (discount.discount_receive * (reste // discount.discount_purchase))
        return total, rescount

    def compute_discount(self):
        best_discount = self.discounts[1]
        total1 = 0
        total2 = 0
        (total1, reste) = self.get_exact_match_discount(best_discount, self.number_of_items)
        if reste > 0:
            best_discount = self.discounts[0]
            (total2, reste) = self.get_exact_match_discount(best_discount, reste)
            if reste > 0:
                total2 += reste * self.price
        return total1 + total2

    # def get_price(self):
    #     result = -1
    #     total = -1
    #     for discount in self.discounts:
    #         if discount.discount_purchase and not(discount.free):
    #             if self.number_of_items >= discount.discount_purchase:
    #                 if (self.number_of_items % discount.discount_purchase) == 0:
    #                     total = (discount.discount_receive * (self.number_of_items / discount.discount_purchase))
    #                 else:
    #                     total = (discount.discount_receive * (self.number_of_items // discount.discount_purchase) + ((self.number_of_items % discount.discount_purchase) * self.price))
    #         if total != -1: 
    #             if result == -1 or result > total:
    #                 result = total
    #     if result != -1:
    #         return result
    #     else:
    #         return self.number_of_items * self.price
    
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
        self.e_number = 0
        self.b_number = 0

    def add_item(self, item):
        found = False
        index = 0
        current_item = item.get_product_name()
        for el in self.items_list:
            index += 1
            if el.get_product_name() == item.get_product_name():
                found = True
                break
        if found:
            self.items_list[index - 1].increment_number_of_items()
        else:
            self.items_list.append(item)
        
        
        if current_item == 'E':
            self.e_number += 1
        elif current_item == 'B':
            self.b_number += 1


    
    def get_items(self):
        return self.items_list
    
    def get_total(self):
        item_list = [item for item in self.items_list if item.product_name not in ('E', 'B')]
        return sum(map(lambda item : item.get_price(), item_list))
    
    def get_global_discount(self):
        total = 0
        free_b = 0
        item_e = [sku for sku in self.items_list if sku.product_name == 'E']
        item_b = [sku for sku in self.items_list if sku.product_name == 'B']
        for sku in item_e:
            for discount in sku.get_discounts():
                if sku.product_name == 'E':
                    total += sku.number_of_items * sku.price
                    if sku.number_of_items >= discount.discount_purchase:
                        if (sku.number_of_items % discount.discount_purchase) == 0:
                            free_b += discount.occurence * (sku.number_of_items / discount.discount_purchase)
                        else:
                            free_b += discount.occurence * (sku.number_of_items // discount.discount_purchase)
        for sku in item_b:
            for discount in sku.get_discounts():
                if sku.product_name == 'B':
                    sku.number_of_items -= free_b
                    total += sku.get_price()                         
        return total

    def checkout(self, skus_string):
        stock = build_stocks()
                
        for skus_name in skus_string:
            skus_objects = list(filter(lambda item : item.product_name == skus_name, stock))
            if len(skus_objects) == 0:
                return -1
            else:
                self.add_item(skus_objects[0])
        total = self.get_total()
        total_discount = self.get_global_discount()
        print('total {} total_discount {}'.format(total, total_discount))
        return total + total_discount
    

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