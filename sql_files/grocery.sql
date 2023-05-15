Drop database grocery;

CREATE DATABASE IF NOT EXISTS grocery;
use grocery;

create table Product_categories
(
	category_id int primary key,
    category_name varchar(50) not null
);

create table Products
(
	product_id int primary key auto_increment,
    product_name varchar(50) Not NULL,
    product_quantity int NOT NULL,
    product_price float,
    category_id int,
    
    foreign key (category_id) references Product_categories(category_id)
    ON DELETE CASCADE
);

create table Product_reviews
(
	product_review_id int primary key auto_increment,
    num_stars int not null,
    product_id int,
    
    foreign key (product_id) references Products(product_id)
    ON DELETE CASCADE
);

create table customers
(
	customer_id int primary key auto_increment,
	email VARCHAR (50) NOT NULL UNIQUE,
	first_name VARCHAR (50) NOT NULL,
	customer_pass VARCHAR (50) NOT NULL
);

create table customer_product_review
(
	customer_id int,
    product_review_id int,
    primary key(customer_id, product_review_id),
    foreign key (customer_id) references Customers(customer_id)
    ON DELETE CASCADE,
    foreign key (product_review_id) references Product_reviews(product_review_id)
    ON DELETE CASCADE
);

create table customer_products
(
	customer_id int,
    product_id int,
    primary key(customer_id, product_id),
    foreign key (customer_id) references Customers(customer_id)
    ON DELETE CASCADE,
    foreign key (product_id) references Products(product_id)
    ON DELETE CASCADE
);


