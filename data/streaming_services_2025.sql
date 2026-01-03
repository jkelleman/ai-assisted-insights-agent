-- Streaming Services 2025 Sample Dataset
-- This creates tables with realistic streaming platform data

-- User subscriptions and activity
CREATE TABLE IF NOT EXISTS analytics.subscriptions (
    user_id INTEGER,
    subscription_date DATE,
    plan_type TEXT,
    platform TEXT,
    monthly_price DECIMAL(10,2),
    status TEXT,
    country TEXT,
    acquisition_channel TEXT
);

CREATE TABLE IF NOT EXISTS analytics.viewing_activity (
    user_id INTEGER,
    event_date DATE,
    content_id TEXT,
    content_type TEXT,
    watch_duration_minutes INTEGER,
    completed BOOLEAN,
    device_type TEXT,
    platform TEXT
);

CREATE TABLE IF NOT EXISTS analytics.revenue (
    transaction_date DATE,
    user_id INTEGER,
    amount DECIMAL(10,2),
    payment_type TEXT,
    platform TEXT,
    country TEXT,
    plan_type TEXT
);

CREATE TABLE IF NOT EXISTS analytics.content_library (
    content_id TEXT,
    title TEXT,
    content_type TEXT,
    genre TEXT,
    release_year INTEGER,
    duration_minutes INTEGER,
    platform TEXT,
    added_date DATE
);

CREATE TABLE IF NOT EXISTS analytics.churn_events (
    user_id INTEGER,
    churn_date DATE,
    subscription_length_days INTEGER,
    reason_category TEXT,
    platform TEXT,
    last_plan_type TEXT
);

-- Sample data for 2025
-- Note: In a real scenario, you'd load actual data here
-- This structure supports the metrics we'll define
