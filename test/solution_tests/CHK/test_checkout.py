from lib.solutions.CHK import checkout_solution

class TestSkus():
    def test_skus_should_created(self):
        skus_a = checkout_solution.Skus(product_name='A', price=10.0)
        assert skus_a.get_product_name() == 'A'
        assert skus_a.get_price() == 10.0
        assert skus_a.get_number_of_items() == 1
        assert len(skus_a.get_discounts()) == 0
    
    def test_skus_should_created_with_discount_info(self):
        discount = checkout_solution.Discount(discount_purchase=3, discount_receive=130)
        skus_a = checkout_solution.Skus(product_name='A', price=50)
        skus_a.add_discount(discount)
        assert skus_a.get_product_name() == 'A'
        assert skus_a.get_price() == 50
        assert skus_a.get_number_of_items() == 1
        discounts = skus_a.get_discounts()
        assert len(discounts) == 1
        assert discounts[0].get_discount_purchase() == 3
        assert discounts[0].get_discount_receive() == 130

class TestBasket():
    
    def test_basket_items(self):
        discount = checkout_solution.Discount(discount_purchase=3, discount_receive=130)
        skus_a = checkout_solution.Skus(product_name='A', price=50)
        skus_a.add_discount(discount)
        basket = checkout_solution.Basket()
        assert len(basket.get_items()) == 0
        basket.add_item(skus_a)
        assert len(basket.get_items()) == 1

    def test_when_added_the_same_skus_in_basket(self):
        discount = checkout_solution.Discount(discount_purchase=3, discount_receive=130)
        discount1 = checkout_solution.Discount(discount_purchase=2, discount_receive=45)
        skus_a = checkout_solution.Skus(product_name='A', price=50)
        skus_a.add_discount(discount)
        skus_b = checkout_solution.Skus(product_name='B', price=30)
        skus_b.add_discount(discount1)
        skus_c = checkout_solution.Skus(product_name='C', price=20)
        basket = checkout_solution.Basket()
        basket.add_item(skus_a)
        basket.add_item(skus_b)
        basket.add_item(skus_c)
        items_list = basket.get_items()
        assert len(items_list) == 3
        assert items_list[1].get_number_of_items() == 1
        basket.add_item(skus_b)
        items_list = basket.get_items()
        assert len(items_list) == 3
        assert items_list[1].get_number_of_items() == 2

    # def test_checkout_without_discount(self):
    #     skus_a = checkout_solution.Skus(product_name='A', price=50)
    #     skus_b = checkout_solution.Skus(product_name='B', price=30)
    #     skus_c = checkout_solution.Skus(product_name='C', price=20)
    #     basket = checkout_solution.Basket()
    #     basket.add_item(skus_a)
    #     basket.add_item(skus_b)
    #     basket.add_item(skus_c)
    #     assert basket.get_total() == 100
    
    # def test_checkout_with_discount_not_applied(self):
    #     discount = checkout_solution.Discount(discount_purchase=3, discount_receive=130)
    #     skus_a = checkout_solution.Skus(product_name='A', price=50)
    #     skus_a.add_discount(discount)
    #     skus_b = checkout_solution.Skus(product_name='B', price=30)
    #     skus_c = checkout_solution.Skus(product_name='C', price=20)
    #     basket = checkout_solution.Basket()
    #     basket.add_item(skus_a)
    #     basket.add_item(skus_a)
    #     basket.add_item(skus_b)
    #     basket.add_item(skus_c)
    #     assert basket.get_total() == 150

    # def test_checkout_with_discount_applied(self):
    #     discount = checkout_solution.Discount(discount_purchase=3, discount_receive=130)
    #     skus_a = checkout_solution.Skus(product_name='A', price=50)
    #     skus_a.add_discount(discount)
    #     skus_b = checkout_solution.Skus(product_name='B', price=30)
    #     skus_c = checkout_solution.Skus(product_name='C', price=20)
    #     basket = checkout_solution.Basket()
    #     basket.add_item(skus_a)
    #     basket.add_item(skus_a)
    #     basket.add_item(skus_a)
    #     basket.add_item(skus_b)
    #     basket.add_item(skus_c)
    #     assert basket.get_total() == 180
    
    # def test_checkout_with_discount_applied_but_not_on_all_items(self):
    #     discount = checkout_solution.Discount(discount_purchase=3, discount_receive=130)
    #     skus_a = checkout_solution.Skus(product_name='A', price=50)
    #     skus_a.add_discount(discount)
    #     skus_b = checkout_solution.Skus(product_name='B', price=30)
    #     skus_c = checkout_solution.Skus(product_name='C', price=20)
    #     basket = checkout_solution.Basket()
    #     basket.add_item(skus_a)
    #     basket.add_item(skus_a)
    #     basket.add_item(skus_a)
    #     basket.add_item(skus_a)
    #     basket.add_item(skus_b)
    #     basket.add_item(skus_c)
    #     assert basket.get_total() == 230
    
    # def test_checkout_with_discount_applied_but_not_on_all_items_(self):
    #     discount = checkout_solution.Discount(discount_purchase=2, discount_receive=80)
    #     skus_a = checkout_solution.Skus(product_name='A', price=50)
    #     skus_a.add_discount(discount)
    #     skus_b = checkout_solution.Skus(product_name='B', price=30)
    #     skus_c = checkout_solution.Skus(product_name='C', price=20)
    #     basket = checkout_solution.Basket()
    #     basket.add_item(skus_a)
    #     basket.add_item(skus_a)
    #     basket.add_item(skus_a)
    #     basket.add_item(skus_a)
    #     basket.add_item(skus_a)
    #     basket.add_item(skus_b)
    #     basket.add_item(skus_c)
    #     assert basket.get_total() == 260

    def test_checkout_from_string(self):
        basket = checkout_solution.Basket()
        assert basket.checkout('ABCD') == 115
    
    def test_checkout_from_string_discount(self):
        assert checkout_solution.checkout('ABCADA') == 195

    def test_checkout_from_string_discount2(self):
        assert checkout_solution.checkout('ABCADAAAA') == 315
    
    def test_checkout_from_string_discount3(self):
        assert checkout_solution.checkout('ABCADAAA') == 265
    
    def test_checkout_from_string_discount4(self):
        assert checkout_solution.checkout('ABCDE') == 155
    
    def test_checkout_from_string_discount5(self):
        assert checkout_solution.checkout('ABCEDE') == 165
    
    def test_checkout_from_string_discount6(self):
        assert checkout_solution.checkout('BBEE') == 110 # to check
    
    def test_checkout_from_string_discount7(self):
        assert checkout_solution.checkout('EE') == 80

    def test_checkout_from_string_discount8(self):
        assert checkout_solution.checkout('AAAAAAAA') == 330
    
    def test_checkout_from_string_discount9(self):
        assert checkout_solution.checkout('ABCDEABCDE') == 280 
        
    
    def test_checkout_from_string_discount10(self):
        assert checkout_solution.checkout('CCADDEEBBA') == 280
    
    def test_checkout_from_string_discount11(self):
        assert checkout_solution.checkout('EEEEBB') == 160
    
    def test_checkout_from_string_discount12(self):
        assert checkout_solution.checkout('FF') == 20
    
    def test_checkout_from_string_discount13(self):
        assert checkout_solution.checkout('FFF') == 20

    def test_checkout_from_string_discount14(self):
        assert checkout_solution.checkout('NNNM') == 120
    
    def test_checkout_from_string_discount15(self):
        assert checkout_solution.checkout('NNN') == 120
    
    def test_checkout_from_string_discount16(self):
        assert checkout_solution.checkout('NNNNNNMM') == 240
    
    def test_checkout_from_string_discount17(self):
        assert checkout_solution.checkout('NNNNNNM') == 240
    def test_checkout_from_string_discount18(self):
        assert checkout_solution.checkout('M') == 15
    
    def test_checkout_from_string_discount19(self):
        assert checkout_solution.checkout('ABCDEFGHIJKLMNOPQRSTUVWXYZ') == 965
    
    def test_checkout_from_string_discount20(self):
        assert checkout_solution.checkout('ABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZ') == 1880
    
    def test_checkout_from_string_discount21(self):
        assert checkout_solution.checkout('SSS') == 45
    
    def test_checkout_from_string_discount22(self):
        assert checkout_solution.checkout('TTT') == 45
    
    def test_checkout_from_string_discount23(self):
        assert checkout_solution.checkout('ZZZ') == 45
    
    def test_checkout_from_string_discount24(self):
        assert checkout_solution.checkout('STY') == 45
    
    def test_checkout_from_string_discount25(self):
        assert checkout_solution.checkout('STYX') == 62
    
    def test_checkout_from_string_discount26(self):
        assert checkout_solution.checkout('XXXX') == 62
    
    def test_checkout_from_string_discount27(self):
        assert checkout_solution.checkout('XXXST') == 79

    def test_checkout_from_invalid_string(self):
        assert checkout_solution.checkout('') == 0
        assert checkout_solution.checkout('a') == -1
    
    
        
            



