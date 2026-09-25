-- Active: 1789212612684@@127.0.0.1@5432@testdev
-- ============================================================================
-- E-COMMERCE MICROSERVICES DATABASE SCHEMAS (PostgreSQL)
-- Quy ước:
-- 1. Database-per-service (Mỗi service sở hữu schema riêng biệt).
-- 2. KHÔNG có FOREIGN KEY liên-service (xử lý ở tầng Application / Event-driven).
-- 3. CHỈ tạo FOREIGN KEY giữa các bảng cùng thuộc 1 service.
-- 4. Bổ sung Outbox Pattern Table (outbox_events) cho các service tham gia Saga/Event streaming.
-- ============================================================================

-- ============================================================================
-- SERVICE 1: USER / PROFILE SERVICE
-- Quản lý hồ sơ người dùng, sổ địa chỉ nhận hàng
-- ============================================================================
CREATE SCHEMA IF NOT EXISTS user_service;

CREATE TABLE user_service.user_profiles (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    auth_user_id UUID NOT NULL UNIQUE, -- ID trỏ sang bảng users ở Auth Service
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    phone VARCHAR(20) UNIQUE,
    avatar_url VARCHAR(500),
    gender VARCHAR(10),
    date_of_birth DATE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE user_service.user_addresses (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    profile_id UUID NOT NULL,
    recipient_name VARCHAR(100) NOT NULL,
    phone_number VARCHAR(20) NOT NULL,
    province VARCHAR(100) NOT NULL,
    district VARCHAR(100) NOT NULL,
    ward VARCHAR(100) NOT NULL,
    detailed_address VARCHAR(255) NOT NULL,
    is_default BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_address_profile FOREIGN KEY (profile_id) 
        REFERENCES user_service.user_profiles(id) ON DELETE CASCADE
);

CREATE INDEX idx_user_addresses_profile_id ON user_service.user_addresses(profile_id);

-- ============================================================================
-- SERVICE 2: PRODUCT SERVICE
-- Mô hình quản lý danh mục, sản phẩm, ảnh và các biến thể (SKUs)
-- ============================================================================
CREATE SCHEMA IF NOT EXISTS product_service;

CREATE TABLE product_service.providers (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(192) NOT NULL,
    phone VARCHAR(20),
    email VARCHAR(100),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE product_service.categories (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    parent_id UUID,
    name VARCHAR(100) NOT NULL,
    slug VARCHAR(120) NOT NULL UNIQUE,
    description TEXT,
    CONSTRAINT fk_category_parent FOREIGN KEY (parent_id) 
        REFERENCES product_service.categories(id) ON DELETE SET NULL
);

CREATE TABLE product_service.products (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    provider_id UUID NOT NULL,
    name VARCHAR(255) NOT NULL,
    slug VARCHAR(255) NOT NULL UNIQUE,
    description TEXT,
    status VARCHAR(20) NOT NULL DEFAULT 'DRAFT', -- DRAFT, PUBLISHED, ARCHIVED
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_product_provider FOREIGN KEY (provider_id) 
        REFERENCES product_service.providers(id)
);

CREATE TABLE product_service.product_categories (
    product_id UUID NOT NULL,
    category_id UUID NOT NULL,
    PRIMARY KEY (product_id, category_id),
    CONSTRAINT fk_pc_product FOREIGN KEY (product_id) 
        REFERENCES product_service.products(id) ON DELETE CASCADE,
    CONSTRAINT fk_pc_category FOREIGN KEY (category_id) 
        REFERENCES product_service.categories(id) ON DELETE CASCADE
);

CREATE TABLE product_service.product_skus (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    product_id UUID NOT NULL,
    sku_code VARCHAR(100) NOT NULL UNIQUE,
    price NUMERIC(15, 2) NOT NULL,
    original_price NUMERIC(15, 2),
    status VARCHAR(20) NOT NULL DEFAULT 'ACTIVE',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_sku_product FOREIGN KEY (product_id) 
        REFERENCES product_service.products(id) ON DELETE CASCADE
);

CREATE TABLE product_service.product_images (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    product_id UUID NOT NULL,
    image_url VARCHAR(500) NOT NULL,
    is_thumbnail BOOLEAN DEFAULT FALSE,
    sort_order INT DEFAULT 0,
    CONSTRAINT fk_images_product FOREIGN KEY (product_id) 
        REFERENCES product_service.products(id) ON DELETE CASCADE
);

-- ============================================================================
-- SERVICE 3: CART SERVICE
-- Quản lý giỏ hàng của người dùng
-- ============================================================================
CREATE SCHEMA IF NOT EXISTS cart_service;

CREATE TABLE cart_service.carts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL UNIQUE, -- ID trỏ sang Auth/User Service
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE cart_service.cart_items (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    cart_id UUID NOT NULL,
    product_sku_id UUID NOT NULL, -- ID trỏ sang Product Service
    quantity INT NOT NULL CHECK (quantity > 0),
    added_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT uq_cart_sku UNIQUE (cart_id, product_sku_id),
    CONSTRAINT fk_cart_items_cart FOREIGN KEY (cart_id) 
        REFERENCES cart_service.carts(id) ON DELETE CASCADE
);

-- ============================================================================
-- SERVICE 4: ORDER SERVICE (Bao gồm Outbox Table)
-- Quản lý vòng đời đơn hàng và phát sinh Order events
-- ============================================================================
CREATE SCHEMA IF NOT EXISTS order_service;

CREATE TABLE order_service.orders (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    order_code VARCHAR(32) NOT NULL UNIQUE,
    user_id UUID NOT NULL, -- ID trỏ sang Auth/User Service
    status VARCHAR(30) NOT NULL DEFAULT 'PENDING',
    -- Status: PENDING, PAYMENT_PENDING, CONFIRMED, SHIPPING, COMPLETED, CANCELLED, REFUNDED
    total_amount NUMERIC(15, 2) NOT NULL,
    discount_amount NUMERIC(15, 2) NOT NULL DEFAULT 0.00,
    shipping_fee NUMERIC(15, 2) NOT NULL DEFAULT 0.00,
    final_amount NUMERIC(15, 2) NOT NULL,
    recipient_name VARCHAR(100) NOT NULL,
    recipient_phone VARCHAR(20) NOT NULL,
    shipping_address TEXT NOT NULL,
    
    note TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_orders_user_id ON order_service.orders(user_id);
CREATE INDEX idx_orders_status ON order_service.orders(status);

CREATE TABLE order_service.order_items (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    order_id UUID NOT NULL,
    product_sku_id UUID NOT NULL, -- ID trỏ sang Product Service
    product_name VARCHAR(255) NOT NULL,
    sku_code VARCHAR(100) NOT NULL,
    unit_price NUMERIC(15, 2) NOT NULL,
    quantity INT NOT NULL CHECK (quantity > 0),
    total_price NUMERIC(15, 2) NOT NULL,
    CONSTRAINT fk_order_items_order FOREIGN KEY (order_id) 
        REFERENCES order_service.orders(id) ON DELETE CASCADE
);

CREATE TABLE order_service.order_status_history (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    order_id UUID NOT NULL,
    from_status VARCHAR(30),
    to_status VARCHAR(30) NOT NULL,
    reason TEXT,
    changed_by UUID,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_order_history_order FOREIGN KEY (order_id) 
        REFERENCES order_service.orders(id) ON DELETE CASCADE
);

-- Bảng Outbox cho Order Service (Publish events: OrderCreated, OrderCancelled,...)
CREATE TABLE order_service.outbox_events (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    aggregate_type VARCHAR(50) NOT NULL DEFAULT 'ORDER',
    aggregate_id VARCHAR(50) NOT NULL, -- order_id
    type VARCHAR(100) NOT NULL,        -- 'OrderCreated', 'OrderCancelled'
    payload JSONB NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'PENDING', -- PENDING, PROCESSED, FAILED
    retry_count INT NOT NULL DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    processed_at TIMESTAMP WITH TIME ZONE
);

CREATE INDEX idx_order_outbox_status_created ON order_service.outbox_events(status, created_at);

-- ============================================================================
-- SERVICE 5: PAYMENT SERVICE (Bao gồm Outbox Table)
-- Quản lý thanh toán và thông báo kết quả giao dịch
-- ============================================================================
CREATE SCHEMA IF NOT EXISTS payment_service;

CREATE TABLE payment_service.payments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    order_id UUID NOT NULL UNIQUE, -- ID trỏ sang Order Service
    user_id UUID NOT NULL,         -- ID trỏ sang Auth/User Service
    payment_method VARCHAR(50) NOT NULL, -- COD, MOMO, VNPAY, STRIPE, BANK_TRANSFER
    status VARCHAR(30) NOT NULL DEFAULT 'PENDING', -- PENDING, SUCCESS, FAILED, REFUNDED
    amount NUMERIC(15, 2) NOT NULL,
    currency VARCHAR(10) NOT NULL DEFAULT 'VND',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE payment_service.payment_transactions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    payment_id UUID NOT NULL,
    transaction_code VARCHAR(100),
    gateway_response JSONB,
    status VARCHAR(30) NOT NULL, -- INITIATED, SUCCESS, FAILED
    amount NUMERIC(15, 2) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_trans_payment FOREIGN KEY (payment_id) 
        REFERENCES payment_service.payments(id) ON DELETE CASCADE
);

-- Bảng Outbox cho Payment Service (Publish events: PaymentSucceeded, PaymentFailed,...)
CREATE TABLE payment_service.outbox_events (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    aggregate_type VARCHAR(50) NOT NULL DEFAULT 'PAYMENT',
    aggregate_id VARCHAR(50) NOT NULL, -- payment_id hoặc order_id
    type VARCHAR(100) NOT NULL,        -- 'PaymentSucceeded', 'PaymentFailed'
    payload JSONB NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'PENDING',
    retry_count INT NOT NULL DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    processed_at TIMESTAMP WITH TIME ZONE
);

CREATE INDEX idx_payment_outbox_status_created ON payment_service.outbox_events(status, created_at);

-- ============================================================================
-- SERVICE 6: INVENTORY / STOCK SERVICE (Bao gồm Outbox Table)
-- Quản lý tồn kho và giữ hàng (Hold/Reserve)
-- ============================================================================
CREATE SCHEMA IF NOT EXISTS inventory_service;

CREATE TABLE inventory_service.inventory_stocks (
    product_sku_id UUID PRIMARY KEY, -- ID trỏ sang Product Service
    total_quantity INT NOT NULL DEFAULT 0 CHECK (total_quantity >= 0),
    reserved_quantity INT NOT NULL DEFAULT 0 CHECK (reserved_quantity >= 0),
    available_quantity INT GENERATED ALWAYS AS (total_quantity - reserved_quantity) STORED,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE inventory_service.stock_reservations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    order_id UUID NOT NULL,         -- ID trỏ sang Order Service
    product_sku_id UUID NOT NULL,   -- ID trỏ sang Product Service
    reserved_quantity INT NOT NULL CHECK (reserved_quantity > 0),
    status VARCHAR(30) NOT NULL DEFAULT 'HELD', -- HELD, COMMITTED, RELEASED
    expires_at TIMESTAMP WITH TIME ZONE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_res_stock FOREIGN KEY (product_sku_id) 
        REFERENCES inventory_service.inventory_stocks(product_sku_id)
);

CREATE INDEX idx_stock_res_order_id ON inventory_service.stock_reservations(order_id);

-- Bảng Outbox cho Inventory Service (Publish events: StockReserved, StockReservationFailed,...)
CREATE TABLE inventory_service.outbox_events (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    aggregate_type VARCHAR(50) NOT NULL DEFAULT 'INVENTORY',
    aggregate_id VARCHAR(50) NOT NULL, -- order_id hoặc reservation_id
    type VARCHAR(100) NOT NULL,        -- 'StockReserved', 'StockReservationFailed'
    payload JSONB NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'PENDING',
    retry_count INT NOT NULL DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    processed_at TIMESTAMP WITH TIME ZONE
);

CREATE INDEX idx_inventory_outbox_status_created ON inventory_service.outbox_events(status, created_at);

-- ============================================================================
-- SERVICE 7: PROMOTION / VOUCHER SERVICE
-- Quản lý khuyến mãi, voucher giảm giá
-- ============================================================================
CREATE SCHEMA IF NOT EXISTS promotion_service;

CREATE TABLE promotion_service.vouchers (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    code VARCHAR(50) NOT NULL UNIQUE,
    discount_type VARCHAR(20) NOT NULL, -- PERCENTAGE, FIXED_AMOUNT
    discount_value NUMERIC(15, 2) NOT NULL,
    min_order_value NUMERIC(15, 2) DEFAULT 0.00,
    max_discount_value NUMERIC(15, 2),
    usage_limit INT,
    usage_count INT NOT NULL DEFAULT 0,
    start_date TIMESTAMP WITH TIME ZONE NOT NULL,
    end_date TIMESTAMP WITH TIME ZONE NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE promotion_service.voucher_usages (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    voucher_id UUID NOT NULL,
    order_id UUID NOT NULL UNIQUE, -- ID trỏ sang Order Service
    user_id UUID NOT NULL,         -- ID trỏ sang Auth/User Service
    discount_applied NUMERIC(15, 2) NOT NULL,
    used_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_usage_voucher FOREIGN KEY (voucher_id) 
        REFERENCES promotion_service.vouchers(id) ON DELETE CASCADE
);