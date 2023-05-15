import unittest
import product_database as db

class TestGroceryQueries(unittest.TestCase):

    def test_categories(self):
        self.assertEqual(len(db.get_product_categories()), 6)

    def test_categories(self):
        self.assertGreaterEqual(5, len(db.get_products("Fruits")))
    
    def test_create_user(self):
        #Unique so I cannot make duplicates
        with self.assertRaises(Exception):
            db.create_user('yoel@gmail.com', 'Yoel', '12345')
    
    # Passing anything besides a string should throw an error
    def test_get_products(self):
        with self.assertRaises(ValueError):
            db.get_products(1234)

    # Email and Product Name should be a string, and quantity should be an int
    def test_buy_product(self):
        #testing email
        with self.assertRaises(ValueError):
            db.buy_product(123, "Pizza", 1)
        #testing product name
        with self.assertRaises(ValueError): 
            db.buy_product("Pizza", 123, 1)
        #Testing quantity
        with self.assertRaises(ValueError):
            db.buy_product("123", "Pizza", "Number")
    
    #Email, first_name, and password should be strings
    def test_create_user(self):
        #testing email
        with self.assertRaises(ValueError):
            db.create_user(123, "Pizza", "1")
        #testing first_name
        with self.assertRaises(ValueError): 
            db.create_user("Pizza", 123, "1")
        #Testing password
        with self.assertRaises(ValueError):
            db.create_user("123", "Pizza", 123)

    #Email should be a string
    def test_view_owned_products(self):
        #testing email
        with self.assertRaises(ValueError):
            db.view_owned_products(123)

    # Email and product should be a string, and star number should be an int
    def test_create_user_review(self):
        #testing email
        with self.assertRaises(ValueError):
            db.create_user_review(123, "Pizza", "1")
        #testing product
        with self.assertRaises(ValueError): 
            db.create_user_review("Pizza", 123, "1")
        #Testing password
        with self.assertRaises(ValueError):
            db.create_user_review("123", "Pizza", "123")

    # Both amount taken and product should be ints
    def test_update_quantity(self):                
        with self.assertRaises(ValueError):
            db.update_quantity("test", 123)
        with self.assertRaises(ValueError):
            db.update_quantity(123, "123")
    
    # Order by should be a string, and the only inputs are category
    # or price, if it is not either, it will be empty
    def test_get_all_products(self):
        with self.assertRaises(ValueError):
            db.get_all_products(123)
        with self.assertRaises(Exception):
            db.get_all_products("Wrong Category")
    
    def test_delete_user(self):
        with self.assertRaises(ValueError):
            db.delete_user(1234)
    
    def test_add_fruit(self):
        # product name has to be string
        with self.assertRaises(ValueError):
            db.add_fruit(1234, 1, 10.0, "temp")

        #quantity has to be int
        with self.assertRaises(ValueError):
            db.add_fruit("1234", "1", 10.0, "temp")
        
        #price has to be float
        with self.assertRaises(ValueError):
            db.add_fruit("1234", 1, "10.0", "temp")

        #category has to be string
        with self.assertRaises(ValueError):
            db.add_fruit("1234", 1, 10.0, 1234)



if (__name__ == '__main__'):
    unittest.main()