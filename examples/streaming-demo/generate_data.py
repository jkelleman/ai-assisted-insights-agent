#!/usr/bin/env python3
"""
Generate realistic streaming services dataset for 2025.

Creates CSV files with sample data for:
- Subscriptions
- Viewing activity
- Revenue
- Churn events
"""

import csv
import random
from datetime import datetime, timedelta
from pathlib import Path

# Configuration
NUM_SUBSCRIBERS = 10000
NUM_VIEWING_RECORDS = 50000
START_DATE = datetime(2025, 1, 1)
END_DATE = datetime(2025, 12, 31)

PLATFORMS = ["Netflix", "Disney+", "Max", "AppleTV+", "Paramount+", "Peacock", "Hulu"]
PLAN_TYPES = ["Basic", "Standard", "Premium", "Family"]
COUNTRIES = ["USA", "Canada", "UK", "Australia", "Germany", "France", "Japan"]
DEVICES = ["TV", "Mobile", "Tablet", "Desktop", "Gaming Console"]
CONTENT_TYPES = ["Movie", "Series", "Documentary", "Sports", "Kids"]
ACQUISITION_CHANNELS = ["Organic", "Paid Search", "Social Media", "Referral", "App Store"]
CHURN_REASONS = ["Price", "Content", "Technical Issues", "Competitor", "Other"]

PLAN_PRICES = {
    "Basic": 9.99,
    "Standard": 14.99,
    "Premium": 19.99,
    "Family": 22.99
}

def random_date(start, end):
    """Generate random date between start and end."""
    delta = end - start
    random_days = random.randint(0, delta.days)
    return start + timedelta(days=random_days)

def generate_subscriptions(output_dir: Path):
    """Generate subscription data."""
    print("Generating subscriptions...")
    
    output_file = output_dir / "subscriptions.csv"
    
    with open(output_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([
            'user_id', 'subscription_date', 'plan_type', 'platform',
            'monthly_price', 'status', 'country', 'acquisition_channel'
        ])
        
        for user_id in range(1, NUM_SUBSCRIBERS + 1):
            platform = random.choice(PLATFORMS)
            plan_type = random.choice(PLAN_TYPES)
            country = random.choice(COUNTRIES)
            subscription_date = random_date(START_DATE, END_DATE)
            status = "active" if random.random() > 0.15 else "churned"  # 15% churn
            channel = random.choice(ACQUISITION_CHANNELS)
            price = PLAN_PRICES[plan_type]
            
            writer.writerow([
                user_id, subscription_date.strftime('%Y-%m-%d'), plan_type,
                platform, price, status, country, channel
            ])
    
    print(f"✓ Created {output_file}")

def generate_viewing_activity(output_dir: Path):
    """Generate viewing activity data."""
    print("Generating viewing activity...")
    
    output_file = output_dir / "viewing_activity.csv"
    
    with open(output_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([
            'user_id', 'event_date', 'content_id', 'content_type',
            'watch_duration_minutes', 'completed', 'device_type', 'platform'
        ])
        
        for _ in range(NUM_VIEWING_RECORDS):
            user_id = random.randint(1, NUM_SUBSCRIBERS)
            event_date = random_date(START_DATE, END_DATE)
            content_id = f"CONTENT_{random.randint(1000, 9999)}"
            content_type = random.choice(CONTENT_TYPES)
            
            # More realistic watch durations
            if content_type == "Movie":
                duration = random.randint(30, 180)
                completed = duration > 90 and random.random() > 0.3
            elif content_type == "Series":
                duration = random.randint(15, 60)
                completed = duration > 35 and random.random() > 0.4
            else:
                duration = random.randint(10, 90)
                completed = random.random() > 0.5
            
            device = random.choice(DEVICES)
            platform = random.choice(PLATFORMS)
            
            writer.writerow([
                user_id, event_date.strftime('%Y-%m-%d'), content_id,
                content_type, duration, completed, device, platform
            ])
    
    print(f"✓ Created {output_file}")

def generate_revenue(output_dir: Path):
    """Generate revenue data."""
    print("Generating revenue...")
    
    output_file = output_dir / "revenue.csv"
    
    with open(output_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([
            'transaction_date', 'user_id', 'amount', 'payment_type',
            'platform', 'country', 'plan_type'
        ])
        
        # Monthly subscriptions for each user
        for user_id in range(1, NUM_SUBSCRIBERS + 1):
            platform = random.choice(PLATFORMS)
            plan_type = random.choice(PLAN_TYPES)
            country = random.choice(COUNTRIES)
            amount = PLAN_PRICES[plan_type]
            
            # Generate monthly payments throughout the year
            subscription_start = random_date(START_DATE, END_DATE - timedelta(days=30))
            current_date = subscription_start
            
            while current_date <= END_DATE:
                if random.random() > 0.02:  # 98% payment success rate
                    writer.writerow([
                        current_date.strftime('%Y-%m-%d'), user_id, amount,
                        'subscription', platform, country, plan_type
                    ])
                current_date += timedelta(days=30)
    
    print(f"✓ Created {output_file}")

def generate_churn_events(output_dir: Path):
    """Generate churn event data."""
    print("Generating churn events...")
    
    output_file = output_dir / "churn_events.csv"
    
    with open(output_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([
            'user_id', 'churn_date', 'subscription_length_days',
            'reason_category', 'platform', 'last_plan_type'
        ])
        
        # Generate churn events for ~15% of users
        num_churned = int(NUM_SUBSCRIBERS * 0.15)
        churned_users = random.sample(range(1, NUM_SUBSCRIBERS + 1), num_churned)
        
        for user_id in churned_users:
            churn_date = random_date(START_DATE + timedelta(days=30), END_DATE)
            subscription_length = random.randint(30, 365)
            reason = random.choice(CHURN_REASONS)
            platform = random.choice(PLATFORMS)
            plan_type = random.choice(PLAN_TYPES)
            
            writer.writerow([
                user_id, churn_date.strftime('%Y-%m-%d'), subscription_length,
                reason, platform, plan_type
            ])
    
    print(f"✓ Created {output_file}")

def generate_statistics(output_dir: Path):
    """Generate summary statistics file."""
    print("\nGenerating dataset summary...")
    
    summary_file = output_dir / "dataset_summary.txt"
    
    with open(summary_file, 'w') as f:
        f.write("Streaming Services 2025 - Dataset Summary\n")
        f.write("=" * 60 + "\n\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(f"Total Subscribers: {NUM_SUBSCRIBERS:,}\n")
        f.write(f"Viewing Records: {NUM_VIEWING_RECORDS:,}\n")
        f.write(f"Date Range: {START_DATE.strftime('%Y-%m-%d')} to {END_DATE.strftime('%Y-%m-%d')}\n\n")
        f.write("Platforms:\n")
        for platform in PLATFORMS:
            f.write(f"  - {platform}\n")
        f.write("\nPlan Types:\n")
        for plan, price in PLAN_PRICES.items():
            f.write(f"  - {plan}: ${price}/month\n")
        f.write("\nMetrics Available:\n")
        f.write("  - Total Subscribers\n")
        f.write("  - Monthly Recurring Revenue\n")
        f.write("  - Churn Rate (~15%)\n")
        f.write("  - Engagement Rate\n")
        f.write("  - Average Watch Time\n")
        f.write("  - Content Completion Rate\n")
        f.write("  - Customer Lifetime Value\n")
    
    print(f"✓ Created {summary_file}")

def main():
    """Generate all datasets."""
    print("\n" + "=" * 60)
    print("  Streaming Services 2025 - Data Generator")
    print("=" * 60 + "\n")
    
    # Create output directory
    output_dir = Path("data/generated")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate datasets
    generate_subscriptions(output_dir)
    generate_viewing_activity(output_dir)
    generate_revenue(output_dir)
    generate_churn_events(output_dir)
    generate_statistics(output_dir)
    
    print("\n" + "=" * 60)
    print("✓ Dataset generation complete!")
    print(f"  Files saved to: {output_dir.absolute()}")
    print("=" * 60 + "\n")
    print("Next steps:")
    print("1. Update config_streaming.yaml to point to generated data")
    print("2. Run: python -m insights_agent.cli --config config_streaming.yaml")
    print("3. Try: ask How many total subscribers do we have?")
    print()

if __name__ == "__main__":
    main()
