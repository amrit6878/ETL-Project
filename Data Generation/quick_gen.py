#!/usr/bin/env python3
"""
Complete non-interactive data generator
"""
import pandas as pd
from faker import Faker
import random
from datetime import datetime, timedelta
import os
import sys

# Import config
import config

# Disable input globally
import builtins
builtins.input = lambda prompt='': 'n'

fake = Faker()
Faker.seed(42)
random.seed(42)

# Extract config values
NUM_CUSTOMERS = config.NUM_CUSTOMERS
NUM_PRODUCTS = config.NUM_PRODUCTS
NUM_SALES_REPS = config.NUM_SALES_REPS
NUM_TRANSACTIONS = config.NUM_TRANSACTIONS
CUSTOMER_BATCH_SIZE = config.CUSTOMER_BATCH_SIZE
PRODUCT_BATCH_SIZE = config.PRODUCT_BATCH_SIZE
TRANSACTION_BATCH_SIZE = config.TRANSACTION_BATCH_SIZE
OUTPUT_FORMAT = config.OUTPUT_FORMAT
COMPRESSION = config.COMPRESSION
REGIONS = config.REGIONS
COUNTRIES = config.COUNTRIES
PRODUCT_CATEGORIES = config.PRODUCT_CATEGORIES
CUSTOMER_SEGMENTS = config.CUSTOMER_SEGMENTS

print("=" * 60)
print("SALES DATA WAREHOUSE - DATA GENERATION (Non-Interactive)")
print("=" * 60)

def generate_customer_batch(start_id, batch_size):
    """Generate a batch of customers"""
    customers = []
    for i in range(batch_size):
        customer_id = start_id + i
        acquisition_date = fake.date_between(start_date='-3y', end_date='today')
        customer = {
            'customer_id': f'CUST{customer_id:06d}',
            'customer_name': fake.name(),
            'email': fake.email(),
            'phone': fake.phone_number(),
            'segment': random.choice(CUSTOMER_SEGMENTS),
            'region': random.choice(REGIONS),
            'country': random.choice(COUNTRIES),
            'city': fake.city(),
            'state': fake.state_abbr(),
            'zip_code': fake.zipcode(),
            'acquisition_date': acquisition_date,
            'lifetime_value': round(random.uniform(100, 50000), 2),
            'created_at': datetime.now()
        }
        customers.append(customer)
    return pd.DataFrame(customers)

def generate_all_customers():
    """Generate all customers in batches"""
    output_dir = 'generated-data/customers'
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"\n[1/4] GENERATING CUSTOMERS")
    print("-" * 60)
    print(f"Generating {NUM_CUSTOMERS} customers in batches of {CUSTOMER_BATCH_SIZE}...")
    
    num_batches = (NUM_CUSTOMERS + CUSTOMER_BATCH_SIZE - 1) // CUSTOMER_BATCH_SIZE
    all_files = []
    
    for batch_num in range(num_batches):
        start_id = batch_num * CUSTOMER_BATCH_SIZE
        current_batch_size = min(CUSTOMER_BATCH_SIZE, NUM_CUSTOMERS - start_id)
        
        print(f"  Batch {batch_num + 1}/{num_batches} ({start_id} to {start_id + current_batch_size - 1})")
        
        df_batch = generate_customer_batch(start_id, current_batch_size)
        
        if OUTPUT_FORMAT == 'parquet':
            filename = f"{output_dir}/customers_batch_{batch_num:03d}.parquet"
            df_batch.to_parquet(filename, compression=COMPRESSION, index=False)
        else:
            filename = f"{output_dir}/customers_batch_{batch_num:03d}.csv"
            df_batch.to_csv(filename, index=False)
        
        all_files.append(filename)
        del df_batch
    
    print(f"✓ Generated {NUM_CUSTOMERS} customers")
    print(f"✓ Files saved in: {output_dir}")
    return all_files

try:
    generate_all_customers()
    
    print("\n" + "=" * 60)
    print("✓ DATA GENERATION COMPLETE!")
    print("=" * 60)
    print("Generated data is in the 'generated-data' folder")
    
except Exception as e:
    print(f"\n✗ ERROR: {str(e)}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
