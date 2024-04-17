CREATE TABLE products_dim (
    product_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    unit_price REAL NOT NULL
);

CREATE TABLE sales_fact (
    sale_id INTEGER PRIMARY KEY,
    date DATE NOT NULL,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    FOREIGN KEY (product_id) REFERENCES products_dim(product_id)
);

CREATE TABLE expenses_categories_dim (
    category_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE expenses_fact (
    expense_id INTEGER PRIMARY KEY,
    date DATE NOT NULL,
    category_id INTEGER NOT NULL,
    amount REAL NOT NULL,
    FOREIGN KEY (category_id) REFERENCES expenses_categories_dim(category_id)
);
