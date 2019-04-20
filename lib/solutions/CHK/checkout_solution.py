

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
        item_list = [item for item in self.items_list if item.product_name not in ('E', 'B', 'N', 'M', 'R', 'Q')]
        return sum(map(lambda item : item.get_price(), item_list))
    
    def get_global_discount(self):
        total = 0
        item_e = [sku for sku in self.items_list if sku.product_name == 'E']
        item_b = [sku for sku in self.items_list if sku.product_name == 'B']
        item_n = [sku for sku in self.items_list if sku.product_name == 'N']
        item_m = [sku for sku in self.items_list if sku.product_name == 'M']
        item_r = [sku for sku in self.items_list if sku.product_name == 'R']
        item_q = [sku for sku in self.items_list if sku.product_name == 'Q']
        total += self.get_linked_discounts(item_e, item_b)             
        total += self.get_linked_discounts(item_n, item_m)             
        total += self.get_linked_discounts(item_r, item_q)             
        return total

    def get_linked_discounts(self, item_1, item_2):
        total = 0
        free = 0
        for sku in item_1:
            for discount in sku.get_discounts():
                total += sku.number_of_items * sku.price
                if sku.number_of_items >= discount.discount_purchase:
                    if (sku.number_of_items % discount.discount_purchase) == 0:
                        free += discount.occurence * (sku.number_of_items / discount.discount_purchase)
                    else:
                        free += discount.occurence * (sku.number_of_items // discount.discount_purchase)
        for sku in item_2:
            for discount in sku.get_discounts():
                sku.number_of_items -= free
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
    discount5 = Discount(discount_purchase=3, discount_receive=20)
    discount6 = Discount(discount_purchase=5, discount_receive=45)
    discount7 = Discount(discount_purchase=10, discount_receive=80)
    discount8 = Discount(discount_purchase=2, discount_receive=150)
    discount9 = Discount(discount_purchase=3, ref_skus="M", free=True, occurence=1)
    discount10 = Discount(discount_purchase=3, discount_receive=80)
    discount11 = Discount(discount_purchase=3, ref_skus="Q", free=True, occurence=1)
    discount12 = Discount(discount_purchase=4, discount_receive=120)
    discount13 = Discount(discount_purchase=2, discount_receive=90)
    discount14 = Discount(discount_purchase=3, discount_receive=130)
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
    skus_f = Skus(product_name="F", price=10)
    skus_f.add_discount(discount5)
    skus_g = Skus(product_name='G', price=20)
    skus_h = Skus(product_name='H', price=10)
    skus_h.add_discount(discount6)
    skus_h.add_discount(discount7)
    skus_i = Skus(product_name='I', price=35)
    skus_j = Skus(product_name='J', price=60)
    skus_k = Skus(product_name='K', price=80)
    skus_k.add_discount(discount8)
    skus_l = Skus(product_name='L', price=90)
    skus_m = Skus(product_name='M', price=15)
    skus_n = Skus(product_name='N', price=40)
    skus_n.add_discount(discount9)
    skus_o = Skus(product_name='O', price=10)
    skus_p = Skus(product_name='P', price=50)
    skus_p.add_discount(discount3)
    skus_q = Skus(product_name='Q', price=30)
    skus_q.add_discount(discount10)
    skus_r = Skus(product_name='R', price=50)
    skus_r.add_discount(discount11)
    skus_s = Skus(product_name='S', price=30)
    skus_t = Skus(product_name='T', price=20)
    skus_u = Skus(product_name='U', price=40)
    skus_u.add_discount(discount12)
    skus_v = Skus(product_name='V', price=50)
    skus_v.add_discount(discount13)
    skus_v.add_discount(discount14)
    skus_w = Skus(product_name='W', price=20)
    skus_x = Skus(product_name='X', price=90)
    skus_y = Skus(product_name='Y', price=10)
    skus_z = Skus(product_name='Z', price=50)






    stock.append(skus_c)
    stock.append(skus_d)
    stock.append(skus_e)
    stock.append(skus_f)
    stock.append(skus_g)
    stock.append(skus_h)
    stock.append(skus_i)
    stock.append(skus_j)
    stock.append(skus_k)
    stock.append(skus_l)
    stock.append(skus_m)
    stock.append(skus_n)
    stock.append(skus_o)
    stock.append(skus_p)
    stock.append(skus_q)
    stock.append(skus_r)
    stock.append(skus_s)
    stock.append(skus_t)
    stock.append(skus_u)
    stock.append(skus_v)
    stock.append(skus_w)
    stock.append(skus_x)
    stock.append(skus_y)
    stock.append(skus_z)
    return stock