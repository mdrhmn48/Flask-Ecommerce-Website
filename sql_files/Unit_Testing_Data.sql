#Populate data for unit testing
#Customers table
INSERT into customers(email,first_name,customer_pass)
values("olivia1@gmail.com","Olivia","345"),
	   ("Helena2@gmail.com","Ella", "321"),
	   ("Ella3@gmail.com","Joy", "765"),
       ("Joy4@gmail.com","Jimmy", "165"),
	   ("Jimmy5@gmail.com", "Jimmy", "165"),
      ("Jose6@gmail.com", "Jose", "365"),
      ("Nima7@gmail.com", "Nima", "231"),
      ("Lara8@gmail.com", "Lara", "325"),
      ("Ivy9@gmail.com", "Ivy", "867"),
      ("Neil10@gmail.com", "Neil", "965");

#Customer Product table with customer id and product id
INSERT INTO customer_products (customer_id,product_id)
VALUES ((Select customer_id from Customers where email = "olivia1@gmail.com"),
(Select product_id from Products where product_name = "Quinoa"));
   
INSERT INTO customer_products (customer_id,product_id)
VALUES ((Select customer_id from Customers where email = "Neil10@gmail.com"),
(Select product_id from Products where product_name = "Chicken")); 
    
INSERT INTO customer_products (customer_id,product_id)
VALUES ((Select customer_id from Customers where email = "Ivy9@gmail.com"),
(Select product_id from Products where product_name = "White Bread")); 

INSERT INTO customer_products (customer_id,product_id)
VALUES ((Select customer_id from Customers where email = "Nima7@gmail.com"),
(Select product_id from Products where product_name = "Turkey")); 

INSERT INTO customer_products (customer_id,product_id)
VALUES ((Select customer_id from Customers where email = "Jose6@gmail.com"),
(Select product_id from Products where product_name = "Grapes")); 

INSERT INTO customer_products (customer_id,product_id)
VALUES ((Select customer_id from Customers where email = "Ella3@gmail.com"),
(Select product_id from Products where product_name = "Cauliflower"));