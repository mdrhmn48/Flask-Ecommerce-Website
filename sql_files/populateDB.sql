INSERT INTO product_categories(category_id,category_name)
    values(1, "Fruits"),
	      (2,"Vegetables"),
	      (3,"Snacks"),
	       (4, "Grains"),
          (5,  "Meat"),
          (6, "Dairy");
          
INSERT INTO products(product_name,product_quantity,product_price,category_id)
    values("Grapes", 20, 2.34, 1),
	      ("Apple", 25, 2, 1),
	      ("Banana", 30, 1.5, 1),
	       ("Kiwi",27, 3, 1),
          ("Pineapple",30, 2.34, 1),
          ("Green peper", 27, 1.67, 2),
	      ("Potatoes", 32, 1.99, 2),
	      ("Cauliflower", 20, 2.99, 2),
	       ("Squash",37, 3.45, 2),
          ("Mushroom",40, 2.45, 2),
          ("Potatoes chips", 45, 3.56, 3),
	      ("Trail mix", 55, 4, 3),
	      ("Cookies", 35, 2.99, 3),
	       ("Cheese puff",27, 3.15, 3),
          ("pocky",30, 2.45, 3);
          
INSERT INTO Products (product_name, product_quantity, product_price, category_id)
	values ("White Bread", 50, 3.25, 4),
	    ("Cereals", 20, 4.47, 4),
            ("Rice", 25, 2.12, 4),
            ("Wheat Bread", 50, 3.75, 4),
            ("Quinoa", 25, 4.25, 4),
            ("Beef", 50, 16.50, 5),
            ("Chicken", 50, 13.12, 5),
            ("Fish", 35, 10, 5),
            ("Turkey", 40, 14.30, 5),
            ("Pork", 40, 11.75, 5),
            ("Milk", 30, 2.10, 6),
            ("Cheese", 20, 3.60, 6),
            ("Yogurt", 25, 4.00, 6),
            ("Frozen Yogurt", 20, 5.25, 6),
            ("Cream Cheese", 15, 3.32, 6);
	
