-- Products to sell dimension table
CREATE TABLE products_dim (
    product_id INTEGER PRIMARY KEY,
    name TEXT UNIQUE NOT NULL,
    unit_price REAL NOT NULL
);

-- Sales fact table
CREATE TABLE sales_fact (
    sale_id INTEGER PRIMARY KEY,
    date DATE NOT NULL,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    FOREIGN KEY (product_id) REFERENCES products_dim(product_id)
);

-- Expenses categories dimension table
CREATE TABLE expenses_categories_dim (
    category_id INTEGER PRIMARY KEY,
    name TEXT UNIQUE NOT NULL
);

-- Expenses fact table
CREATE TABLE expenses_fact (
    expense_id INTEGER PRIMARY KEY,
    date DATE NOT NULL,
    category_id INTEGER NOT NULL,
    amount REAL NOT NULL,
    FOREIGN KEY (category_id) REFERENCES expenses_categories_dim(category_id)
);
