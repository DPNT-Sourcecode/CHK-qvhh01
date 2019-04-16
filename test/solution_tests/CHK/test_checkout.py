from lib.solutions.CHK import checkout_solution

class TestSkus():
    def test_skus_should_created(self):
        skus_a = checkout_solution.Skus(product_name='A', price=10.0)
        assert skus_a.get_product_name() == 'A'
        assert skus_a.get_price() == 10.0
        assert skus_a.get_number_of_items() == 1
        assert skus_a.get_discount_purchase() == None
        assert skus_a.get_discount_receive() == None
    
    def test_skus_should_created_with_discount_info(self):
        skus_a = checkout_solution.Skus(product_name='A', price=50, discount_purchase=3, discount_receive=130)
        assert skus_a.get_product_name() == 'A'
        assert skus_a.get_price() == 50
        assert skus_a.get_number_of_items() == 1
        assert skus_a.get_discount_purchase() == 3
        assert skus_a.get_discount_receive() == 130

class TestBasket():
    
    def test_basket_items(self):
        skus_a = checkout_solution.Skus(product_name='A', price=50, discount_purchase=3, discount_receive=130)
        basket = checkout_solution.Basket()
        assert len(basket.get_items()) == 0
        basket.add_item(skus_a)
        assert len(basket.get_items()) == 1

    def test_when_added_the_same_skus_in_basket(self):
        skus_a = checkout_solution.Skus(product_name='A', price=50, discount_purchase=3, discount_receive=130)
        skus_b = checkout_solution.Skus(product_name='B', price=30, discount_purchase=2, discount_receive=45)
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

    def test_checkout_without_discount(self):
        skus_a = checkout_solution.Skus(product_name='A', price=50)
        skus_b = checkout_solution.Skus(product_name='B', price=30)
        skus_c = checkout_solution.Skus(product_name='C', price=20)
        basket = checkout_solution.Basket()
        basket.add_item(skus_a)
        basket.add_item(skus_b)
        basket.add_item(skus_c)
        assert basket.get_total() == 100
    
    def test_checkout_with_discount_not_applied(self):
        skus_a = checkout_solution.Skus(product_name='A', price=50, discount_purchase=3, discount_receive=130)
        skus_b = checkout_solution.Skus(product_name='B', price=30)
        skus_c = checkout_solution.Skus(product_name='C', price=20)
        basket = checkout_solution.Basket()
        basket.add_item(skus_a)
        basket.add_item(skus_a)
        basket.add_item(skus_b)
        basket.add_item(skus_c)
        assert basket.get_total() == 150

    def test_checkout_with_discount_applied(self):
        skus_a = checkout_solution.Skus(product_name='A', price=50, discount_purchase=3, discount_receive=130)
        skus_b = checkout_solution.Skus(product_name='B', price=30)
        skus_c = checkout_solution.Skus(product_name='C', price=20)
        basket = checkout_solution.Basket()
        basket.add_item(skus_a)
        basket.add_item(skus_a)
        basket.add_item(skus_a)
        basket.add_item(skus_b)
        basket.add_item(skus_c)
        assert basket.get_total() == 180
    
    def test_checkout_with_discount_applied_but_not_on_all_items(self):
        skus_a = checkout_solution.Skus(product_name='A', price=50, discount_purchase=3, discount_receive=130)
        skus_b = checkout_solution.Skus(product_name='B', price=30)
        skus_c = checkout_solution.Skus(product_name='C', price=20)
        basket = checkout_solution.Basket()
        basket.add_item(skus_a)
        basket.add_item(skus_a)
        basket.add_item(skus_a)
        basket.add_item(skus_a)
        basket.add_item(skus_b)
        basket.add_item(skus_c)
        assert basket.get_total() == 230
    
    def test_checkout_with_discount_applied_but_not_on_all_items_(self):
        skus_a = checkout_solution.Skus(product_name='A', price=50, discount_purchase=2, discount_receive=80)
        skus_b = checkout_solution.Skus(product_name='B', price=30)
        skus_c = checkout_solution.Skus(product_name='C', price=20)
        basket = checkout_solution.Basket()
        basket.add_item(skus_a)
        basket.add_item(skus_a)
        basket.add_item(skus_a)
        basket.add_item(skus_a)
        basket.add_item(skus_a)
        basket.add_item(skus_b)
        basket.add_item(skus_c)
        assert basket.get_total() == 260

    def test_checkout_from_string(self):
        basket = checkout_solution.Basket()
        assert basket.checkout('ABCD') == 115
    
    def test_checkout_from_string_discount(self):
        assert checkout_solution.checkout('ABCADA') == 195
    
    def test_checkout_from_invalid_string(self):
        assert checkout_solution.checkout('') == 0
        assert checkout_solution.checkout('a') == -1
    
    
        
            



