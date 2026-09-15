CREATE TABLE addresses (
    id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    address_type TEXT,
    postal_code TEXT,
    street TEXT,
    number INTEGER,
    complement TEXT,
    district TEXT,
    city TEXT,
    state TEXT,
    country TEXT,
    is_primary BOOLEAN
);

CREATE TABLE attributes (
    id INTEGER PRIMARY KEY,
    name TEXT,
    data_type TEXT
);

CREATE TABLE brands (
    id INTEGER PRIMARY KEY,
    name TEXT,
    country TEXT,
    is_active BOOLEAN,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

CREATE TABLE categories (
    id INTEGER PRIMARY KEY,
    name TEXT,
    slug TEXT,
    parent_category_id INTEGER,
    is_active BOOLEAN,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

CREATE TABLE customers (
    id INTEGER PRIMARY KEY,
    person_type TEXT,
    legal_name TEXT,
    trade_name TEXT,
    tax_id BIGINT,
    state_registration TEXT,
    email TEXT,
    phone TEXT,
    is_active BOOLEAN,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

CREATE TABLE employees (
    id INTEGER PRIMARY KEY,
    full_name TEXT,
    cpf BIGINT,
    email TEXT,
    role TEXT,
    primary_location_id INTEGER,
    hire_date TIMESTAMP,
    termination_date TIMESTAMP,
    is_active BOOLEAN,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

CREATE TABLE fiscal_invoices (
    id INTEGER PRIMARY KEY,
    order_id INTEGER,
    nfe_number TEXT,
    nfe_access_key TEXT,
    series INTEGER,
    issued_at TIMESTAMP,
    status TEXT,
    total_amount NUMERIC(14,2),
    xml_storage_uri TEXT,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

CREATE TABLE goods_receipt_items (
    id INTEGER PRIMARY KEY,
    goods_receipt_id INTEGER,
    purchase_order_item_id INTEGER,
    quantity_received NUMERIC(14,2)
);

CREATE TABLE goods_receipts (
    id INTEGER PRIMARY KEY,
    purchase_order_id INTEGER,
    received_by_employee_id INTEGER,
    received_at TIMESTAMP,
    notes TEXT,
    created_at TIMESTAMP
);

CREATE TABLE locations (
    id INTEGER PRIMARY KEY,
    name TEXT,
    location_type TEXT,
    postal_code TEXT,
    street TEXT,
    number INTEGER,
    complement TEXT,
    district TEXT,
    city TEXT,
    state TEXT,
    country TEXT,
    is_active BOOLEAN,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

CREATE TABLE order_items (
    id INTEGER PRIMARY KEY,
    order_id INTEGER,
    product_variant_id INTEGER,
    quantity INTEGER,
    unit_price NUMERIC(14,2),
    icms_rate NUMERIC(14,2),
    ipi_rate NUMERIC(14,2),
    line_total NUMERIC(14,2)
);

CREATE TABLE orders (
    id INTEGER PRIMARY KEY,
    order_number TEXT,
    channel TEXT,
    customer_id INTEGER,
    salesperson_id INTEGER,
    location_id INTEGER,
    status TEXT,
    subtotal NUMERIC(14,2),
    discount_amount NUMERIC(14,2),
    total NUMERIC(14,2),
    placed_at TIMESTAMP,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

CREATE TABLE payments (
    id INTEGER PRIMARY KEY,
    order_id INTEGER,
    method TEXT,
    installments INTEGER,
    amount NUMERIC(14,2),
    status TEXT,
    paid_at TIMESTAMP,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

CREATE TABLE product_suppliers (
    product_variant_id INTEGER,
    supplier_id INTEGER,
    supplier_sku TEXT,
    last_quoted_cost NUMERIC(14,2),
    lead_time_days INTEGER,
    is_preferred BOOLEAN,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

CREATE TABLE product_variants (
    id INTEGER PRIMARY KEY,
    product_id INTEGER,
    sku TEXT,
    barcode_ean BIGINT,
    sale_price NUMERIC(14,2),
    cost_price NUMERIC(14,2),
    weight_kg NUMERIC(14,2),
    icms_rate NUMERIC(14,2),
    ipi_rate NUMERIC(14,2),
    is_active BOOLEAN,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

CREATE TABLE products (
    id INTEGER PRIMARY KEY,
    name TEXT,
    description TEXT,
    brand_id INTEGER,
    category_id INTEGER,
    ncm_code INTEGER,
    unit_of_measure TEXT,
    is_active BOOLEAN,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

CREATE TABLE purchase_order_items (
    id INTEGER PRIMARY KEY,
    purchase_order_id INTEGER,
    product_variant_id INTEGER,
    quantity_ordered INTEGER,
    unit_cost NUMERIC(14,2),
    line_total NUMERIC(14,2)
);

CREATE TABLE purchase_orders (
    id INTEGER PRIMARY KEY,
    po_number TEXT,
    supplier_id INTEGER,
    buyer_id INTEGER,
    destination_location_id INTEGER,
    status TEXT,
    currency TEXT,
    subtotal NUMERIC(14,2),
    total NUMERIC(14,2),
    placed_at TIMESTAMP,
    expected_delivery_at TIMESTAMP,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

CREATE TABLE return_items (
    id INTEGER PRIMARY KEY,
    return_id INTEGER,
    order_item_id INTEGER,
    quantity NUMERIC(14,2),
    action TEXT,
    exchange_variant_id INTEGER,
    unit_refund_amount NUMERIC(14,2)
);

CREATE TABLE returns (
    id INTEGER PRIMARY KEY,
    return_number TEXT,
    order_id INTEGER,
    customer_id INTEGER,
    received_at_location_id INTEGER,
    status TEXT,
    reason TEXT,
    total_refund_amount NUMERIC(14,2),
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

CREATE TABLE stock_levels (
    product_variant_id INTEGER,
    location_id INTEGER,
    quantity_on_hand NUMERIC(14,2),
    reorder_point TEXT,
    updated_at TIMESTAMP
);

CREATE TABLE stock_movements (
    id INTEGER PRIMARY KEY,
    product_variant_id INTEGER,
    location_id INTEGER,
    movement_type TEXT,
    quantity NUMERIC(14,2),
    reference_table TEXT,
    reference_id INTEGER,
    employee_id INTEGER,
    notes TEXT,
    occurred_at TIMESTAMP,
    created_at TIMESTAMP
);

CREATE TABLE suppliers (
    id INTEGER PRIMARY KEY,
    legal_name TEXT,
    trade_name TEXT,
    country TEXT,
    tax_id TEXT,
    tax_id_type TEXT,
    email TEXT,
    phone BIGINT,
    contact_name TEXT,
    is_active BOOLEAN,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

CREATE TABLE variant_attribute_values (
    product_variant_id INTEGER,
    attribute_id INTEGER,
    value TEXT
);
SELECT current_database();

