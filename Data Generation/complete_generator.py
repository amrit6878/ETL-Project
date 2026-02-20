#!/usr/bin/env python3
"""
Large-scale data generator for AWS ETL processing (3-4GB dataset)
Optimized for memory efficiency and system stability
"""
import pandas as pd
from faker import Faker
import random
from datetime import datetime, timedelta
import os
import sys
import gc
import psutil

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
START_DATE = config.START_DATE
END_DATE = config.END_DATE

# Memory monitoring
def get_memory_usage():
    """Get current memory usage in GB"""
    process = psutil.Process()
    return process.memory_info().rss / (1024 ** 3)

def print_memory_status():
    """Print current memory usage"""
    mem_used = get_memory_usage()
    print(f"  Memory usage: {mem_used:.2f}GB", end='\r')

print("=" * 70)
print("LARGE-SCALE DATA GENERATION FOR AWS ETL PROCESSING")
print("Target: 3-4GB dataset (~10M transactions)")
print("=" * 70)

# ==================== CUSTOMERS ====================
def generate_customer_batch(start_id, batch_size):
    """Generate a batch of customers"""
    customers = []
    for i in range(batch_size):
        customer_id = start_id + i
        acquisition_date = fake.date_between(start_date='-5y', end_date='today')
        customer = {
            'customer_id': f'CUST{customer_id:08d}',
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
            'lifetime_value': round(random.uniform(100, 500000), 2),
            'created_at': datetime.now()
        }
        customers.append(customer)
    return pd.DataFrame(customers)

def generate_all_customers():
    """Generate all customers in batches"""
    output_dir = 'generated-data/customers'
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"\n[1/4] GENERATING CUSTOMERS ({NUM_CUSTOMERS:,} records)")
    print("-" * 70)
    
    num_batches = (NUM_CUSTOMERS + CUSTOMER_BATCH_SIZE - 1) // CUSTOMER_BATCH_SIZE
    all_files = []
    
    for batch_num in range(num_batches):
        start_id = batch_num * CUSTOMER_BATCH_SIZE
        current_batch_size = min(CUSTOMER_BATCH_SIZE, NUM_CUSTOMERS - start_id)
        
        print(f"  Batch {batch_num + 1:3d}/{num_batches} ({start_id:,} to {start_id + current_batch_size - 1:,})", end='')
        
        df_batch = generate_customer_batch(start_id, current_batch_size)
        
        if OUTPUT_FORMAT == 'parquet':
            filename = f"{output_dir}/customers_batch_{batch_num:05d}.parquet"
            df_batch.to_parquet(filename, compression=COMPRESSION, index=False)
        else:
            filename = f"{output_dir}/customers_batch_{batch_num:05d}.csv"
            df_batch.to_csv(filename, index=False)
        
        all_files.append(filename)
        del df_batch
        gc.collect()
        print_memory_status()
    
    print(f"\n✓ Generated {NUM_CUSTOMERS:,} customers in {len(all_files)} files")
    print(f"✓ Files saved in: {output_dir}")

# ==================== PRODUCTS ====================
def generate_products():
    """Generate products"""
    output_dir = 'generated-data/products'
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"\n[2/4] GENERATING PRODUCTS ({NUM_PRODUCTS:,} records)")
    print("-" * 70)
    
    num_batches = (NUM_PRODUCTS + PRODUCT_BATCH_SIZE - 1) // PRODUCT_BATCH_SIZE
    all_files = []
    
    for batch_num in range(num_batches):
        start_id = batch_num * PRODUCT_BATCH_SIZE
        current_batch_size = min(PRODUCT_BATCH_SIZE, NUM_PRODUCTS - start_id)
        
        print(f"  Batch {batch_num + 1:3d}/{num_batches} ({start_id:,} to {start_id + current_batch_size - 1:,})", end='')
        
        products = []
        for i in range(current_batch_size):
            product_id = start_id + i
            product = {
                'product_id': f'PROD{product_id:08d}',
                'product_name': fake.word() + ' ' + fake.word(),
                'category': random.choice(PRODUCT_CATEGORIES),
                'subcategory': fake.word(),
                'unit_price': round(random.uniform(10, 1000), 2),
                'cost_price': round(random.uniform(5, 500), 2),
                'supplier_id': f'SUPP{random.randint(1, 1000):06d}',
                'stock_quantity': random.randint(0, 10000),
                'reorder_point': random.randint(50, 500),
                'created_at': datetime.now()
            }
            products.append(product)
        
        df_batch = pd.DataFrame(products)
        
        if OUTPUT_FORMAT == 'parquet':
            filename = f"{output_dir}/products_batch_{batch_num:05d}.parquet"
            df_batch.to_parquet(filename, compression=COMPRESSION, index=False)
        else:
            filename = f"{output_dir}/products_batch_{batch_num:05d}.csv"
            df_batch.to_csv(filename, index=False)
        
        all_files.append(filename)
        del df_batch
        gc.collect()
        print_memory_status()
    
    print(f"\n✓ Generated {NUM_PRODUCTS:,} products in {len(all_files)} files")
    print(f"✓ Files saved in: {output_dir}")

# ==================== SALES REPS ====================
def generate_sales_reps():
    """Generate sales representatives"""
    output_dir = 'generated-data/sales-reps'
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"\n[3/4] GENERATING SALES REPRESENTATIVES ({NUM_SALES_REPS:,} records)")
    print("-" * 70)
    
    # Generate in batches even for sales reps
    num_batches = (NUM_SALES_REPS + PRODUCT_BATCH_SIZE - 1) // PRODUCT_BATCH_SIZE
    all_files = []
    
    for batch_num in range(num_batches):
        start_id = batch_num * PRODUCT_BATCH_SIZE
        current_batch_size = min(PRODUCT_BATCH_SIZE, NUM_SALES_REPS - start_id)
        
        print(f"  Batch {batch_num + 1:3d}/{num_batches} ({start_id:,} to {start_id + current_batch_size - 1:,})", end='')
        
        sales_reps = []
        for i in range(current_batch_size):
            rep_id = start_id + i
            sales_rep = {
                'sales_rep_id': f'SREP{rep_id:08d}',
                'name': fake.name(),
                'email': fake.email(),
                'phone': fake.phone_number(),
                'region': random.choice(REGIONS),
                'territory': fake.city(),
                'hire_date': fake.date_between(start_date='-15y', end_date='today'),
                'commission_rate': round(random.uniform(0.01, 0.25), 4),
                'created_at': datetime.now()
            }
            sales_reps.append(sales_rep)
        
        df_batch = pd.DataFrame(sales_reps)
        
        if OUTPUT_FORMAT == 'parquet':
            filename = f"{output_dir}/sales_reps_batch_{batch_num:05d}.parquet"
            df_batch.to_parquet(filename, compression=COMPRESSION, index=False)
        else:
            filename = f"{output_dir}/sales_reps_batch_{batch_num:05d}.csv"
            df_batch.to_csv(filename, index=False)
        
        all_files.append(filename)
        del df_batch
        gc.collect()
        print_memory_status()
    
    print(f"\n✓ Generated {NUM_SALES_REPS:,} sales representatives in {len(all_files)} files")
    print(f"✓ Files saved in: {output_dir}")

# ==================== TRANSACTIONS ====================
def generate_all_transactions():
    """Generate transactions"""
    output_dir = 'generated-data/transactions'
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"\n[4/4] GENERATING TRANSACTIONS ({NUM_TRANSACTIONS:,} records)")
    print("-" * 70)
    
    start = datetime.strptime(START_DATE, '%Y-%m-%d')
    end = datetime.strptime(END_DATE, '%Y-%m-%d')
    num_days = (end - start).days
    
    num_batches = (NUM_TRANSACTIONS + TRANSACTION_BATCH_SIZE - 1) // TRANSACTION_BATCH_SIZE
    all_files = []
    
    for batch_num in range(num_batches):
        start_id = batch_num * TRANSACTION_BATCH_SIZE
        current_batch_size = min(TRANSACTION_BATCH_SIZE, NUM_TRANSACTIONS - start_id)
        
        print(f"  Batch {batch_num + 1:3d}/{num_batches} ({start_id:,} to {start_id + current_batch_size - 1:,})", end='')
        
        transactions = []
        for i in range(current_batch_size):
            transaction_id = start_id + i
            transaction_date = start + timedelta(days=random.randint(0, num_days))
            
            transaction = {
                'transaction_id': f'TXN{transaction_id:012d}',
                'customer_id': f'CUST{random.randint(0, NUM_CUSTOMERS - 1):08d}',
                'product_id': f'PROD{random.randint(0, NUM_PRODUCTS - 1):08d}',
                'sales_rep_id': f'SREP{random.randint(0, NUM_SALES_REPS - 1):08d}',
                'transaction_date': transaction_date,
                'quantity': random.randint(1, 500),
                'unit_price': round(random.uniform(10, 1000), 2),
                'discount_percent': round(random.uniform(0, 50), 2),
                'tax_amount': round(random.uniform(10, 1000), 2),
                'total_amount': round(random.uniform(50, 50000), 2),
                'payment_method': random.choice(['Credit Card', 'Debit Card', 'Check', 'Bank Transfer', 'Online Payment']),
                'region': random.choice(REGIONS),
                'created_at': datetime.now()
            }
            transactions.append(transaction)
        
        df_batch = pd.DataFrame(transactions)
        
        if OUTPUT_FORMAT == 'parquet':
            filename = f"{output_dir}/transactions_batch_{batch_num:05d}.parquet"
            df_batch.to_parquet(filename, compression=COMPRESSION, index=False)
        else:
            filename = f"{output_dir}/transactions_batch_{batch_num:05d}.csv"
            df_batch.to_csv(filename, index=False)
        
        all_files.append(filename)
        del df_batch
        gc.collect()
        print_memory_status()
    
    print(f"\n✓ Generated {NUM_TRANSACTIONS:,} transactions in {len(all_files)} files")
    print(f"✓ Files saved in: {output_dir}")

# ==================== MAIN EXECUTION ====================
try:
    import time
    start_time = time.time()
    
    print(f"\nMemory available: {psutil.virtual_memory().available / (1024**3):.2f}GB")
    print(f"Starting generation at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    generate_all_customers()
    gc.collect()
    
    generate_products()
    gc.collect()
    
    generate_sales_reps()
    gc.collect()
    
    generate_all_transactions()
    gc.collect()
    
    elapsed_time = time.time() - start_time
    
    # Calculate final size
    import os
    total_size = sum(f.stat().st_size for f in os.scandir('generated-data') 
                     for f in os.scandir(f) if f.is_file()) / (1024**3)
    
    print("\n" + "=" * 70)
    print("✓ DATA GENERATION COMPLETE!")
    print("=" * 70)
    print(f"Completion time: {elapsed_time:.2f} seconds ({elapsed_time/60:.2f} minutes)")
    print(f"Final dataset size: {total_size:.2f}GB")
    print(f"Completion time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    print("Generated data structure:")
    print(f"  - generated-data/customers/       ({NUM_CUSTOMERS//CUSTOMER_BATCH_SIZE + 1} parquet files)")
    print(f"  - generated-data/products/        ({NUM_PRODUCTS//PRODUCT_BATCH_SIZE + 1} parquet files)")
    print(f"  - generated-data/sales-reps/      ({NUM_SALES_REPS//PRODUCT_BATCH_SIZE + 1} parquet files)")
    print(f"  - generated-data/transactions/    ({NUM_TRANSACTIONS//TRANSACTION_BATCH_SIZE + 1} parquet files)")
    print("\nReady for AWS ETL processing!")
    
except Exception as e:
    print(f"\n✗ ERROR: {str(e)}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# ==================== CUSTOMERS ====================
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
        
        print(f"  Batch {batch_num + 1}/{num_batches} ({start_id} to {start_id + current_batch_size - 1})", end='\r')
        
        df_batch = generate_customer_batch(start_id, current_batch_size)
        
        if OUTPUT_FORMAT == 'parquet':
            filename = f"{output_dir}/customers_batch_{batch_num:03d}.parquet"
            df_batch.to_parquet(filename, compression=COMPRESSION, index=False)
        else:
            filename = f"{output_dir}/customers_batch_{batch_num:03d}.csv"
            df_batch.to_csv(filename, index=False)
        
        all_files.append(filename)
        del df_batch
    
    print(f"  Batch {num_batches}/{num_batches} ({NUM_CUSTOMERS - CUSTOMER_BATCH_SIZE} to {NUM_CUSTOMERS - 1})  ")
    print(f"\n✓ Generated {NUM_CUSTOMERS:,} customers in {len(all_files)} files")
    print(f"✓ Files saved in: {output_dir}")

# ==================== PRODUCTS ====================
def generate_products():
    """Generate products"""
    output_dir = 'generated-data/products'
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"\n[2/4] GENERATING PRODUCTS")
    print("-" * 60)
    print(f"Generating {NUM_PRODUCTS} products in batches of {PRODUCT_BATCH_SIZE}...")
    
    num_batches = (NUM_PRODUCTS + PRODUCT_BATCH_SIZE - 1) // PRODUCT_BATCH_SIZE
    all_files = []
    
    for batch_num in range(num_batches):
        start_id = batch_num * PRODUCT_BATCH_SIZE
        current_batch_size = min(PRODUCT_BATCH_SIZE, NUM_PRODUCTS - start_id)
        
        print(f"  Batch {batch_num + 1}/{num_batches} ({start_id} to {start_id + current_batch_size - 1})", end='\r')
        
        products = []
        for i in range(current_batch_size):
            product_id = start_id + i
            product = {
                'product_id': f'PROD{product_id:06d}',
                'product_name': fake.word() + ' ' + fake.word(),
                'category': random.choice(PRODUCT_CATEGORIES),
                'subcategory': fake.word(),
                'unit_price': round(random.uniform(10, 1000), 2),
                'cost_price': round(random.uniform(5, 500), 2),
                'supplier_id': f'SUPP{random.randint(1, 100):04d}',
                'stock_quantity': random.randint(0, 1000),
                'reorder_point': random.randint(50, 200),
                'created_at': datetime.now()
            }
            products.append(product)
        
        df_batch = pd.DataFrame(products)
        
        if OUTPUT_FORMAT == 'parquet':
            filename = f"{output_dir}/products_batch_{batch_num:03d}.parquet"
            df_batch.to_parquet(filename, compression=COMPRESSION, index=False)
        else:
            filename = f"{output_dir}/products_batch_{batch_num:03d}.csv"
            df_batch.to_csv(filename, index=False)
        
        all_files.append(filename)
        del df_batch
    
    print(f"  Batch {num_batches}/{num_batches} ({NUM_PRODUCTS - PRODUCT_BATCH_SIZE} to {NUM_PRODUCTS - 1})  ")
    print(f"✓ Generated {NUM_PRODUCTS} products in {len(all_files)} files")
    print(f"✓ Files saved in: {output_dir}")

# ==================== SALES REPS ====================
def generate_sales_reps():
    """Generate sales representatives"""
    output_dir = 'generated-data/sales-reps'
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"\n[3/4] GENERATING SALES REPRESENTATIVES")
    print("-" * 60)
    print(f"Generating {NUM_SALES_REPS} sales representatives...")
    
    sales_reps = []
    for i in range(NUM_SALES_REPS):
        sales_rep = {
            'sales_rep_id': f'SREP{i+1:04d}',
            'name': fake.name(),
            'email': fake.email(),
            'phone': fake.phone_number(),
            'region': random.choice(REGIONS),
            'territory': fake.city(),
            'hire_date': fake.date_between(start_date='-10y', end_date='today'),
            'commission_rate': round(random.uniform(0.01, 0.15), 4),
            'created_at': datetime.now()
        }
        sales_reps.append(sales_rep)
    
    df = pd.DataFrame(sales_reps)
    
    if OUTPUT_FORMAT == 'parquet':
        filename = f"{output_dir}/sales_reps.parquet"
        df.to_parquet(filename, compression=COMPRESSION, index=False)
    else:
        filename = f"{output_dir}/sales_reps.csv"
        df.to_csv(filename, index=False)
    
    print(f"✓ Generated {NUM_SALES_REPS} sales representatives")
    print(f"✓ Files saved in: {output_dir}")

# ==================== TRANSACTIONS ====================
def generate_all_transactions():
    """Generate transactions"""
    output_dir = 'generated-data/transactions'
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"\n[4/4] GENERATING TRANSACTIONS")
    print("-" * 60)
    print(f"Generating {NUM_TRANSACTIONS} transactions in batches of {TRANSACTION_BATCH_SIZE}...")
    
    start = datetime.strptime(START_DATE, '%Y-%m-%d')
    end = datetime.strptime(END_DATE, '%Y-%m-%d')
    num_days = (end - start).days
    
    num_batches = (NUM_TRANSACTIONS + TRANSACTION_BATCH_SIZE - 1) // TRANSACTION_BATCH_SIZE
    all_files = []
    
    for batch_num in range(num_batches):
        start_id = batch_num * TRANSACTION_BATCH_SIZE
        current_batch_size = min(TRANSACTION_BATCH_SIZE, NUM_TRANSACTIONS - start_id)
        
        print(f"  Batch {batch_num + 1}/{num_batches} ({start_id} to {start_id + current_batch_size - 1})", end='\r')
        
        transactions = []
        for i in range(current_batch_size):
            transaction_id = start_id + i
            transaction_date = start + timedelta(days=random.randint(0, num_days))
            
            transaction = {
                'transaction_id': f'TXN{transaction_id:09d}',
                'customer_id': f'CUST{random.randint(0, NUM_CUSTOMERS - 1):06d}',
                'product_id': f'PROD{random.randint(0, NUM_PRODUCTS - 1):06d}',
                'sales_rep_id': f'SREP{random.randint(1, NUM_SALES_REPS):04d}',
                'transaction_date': transaction_date,
                'quantity': random.randint(1, 100),
                'unit_price': round(random.uniform(10, 1000), 2),
                'discount_percent': round(random.uniform(0, 50), 2),
                'tax_amount': round(random.uniform(10, 500), 2),
                'total_amount': round(random.uniform(50, 10000), 2),
                'payment_method': random.choice(['Credit Card', 'Debit Card', 'Check', 'Bank Transfer']),
                'region': random.choice(REGIONS),
                'created_at': datetime.now()
            }
            transactions.append(transaction)
        
        df_batch = pd.DataFrame(transactions)
        
        if OUTPUT_FORMAT == 'parquet':
            filename = f"{output_dir}/transactions_batch_{batch_num:03d}.parquet"
            df_batch.to_parquet(filename, compression=COMPRESSION, index=False)
        else:
            filename = f"{output_dir}/transactions_batch_{batch_num:03d}.csv"
            df_batch.to_csv(filename, index=False)
        
        all_files.append(filename)
        del df_batch
    
    print(f"  Batch {num_batches}/{num_batches} ({NUM_TRANSACTIONS - TRANSACTION_BATCH_SIZE} to {NUM_TRANSACTIONS - 1})  ")
    print(f"✓ Generated {NUM_TRANSACTIONS} transactions in {len(all_files)} files")
    print(f"✓ Files saved in: {output_dir}")

# ==================== MAIN EXECUTION ====================
try:
    import time
    start_time = time.time()
    
    generate_all_customers()
    generate_products()
    generate_sales_reps()
    generate_all_transactions()
    
    elapsed_time = time.time() - start_time
    
    print("\n" + "=" * 60)
    print("✓ DATA GENERATION COMPLETE!")
    print("=" * 60)
    print(f"Total time: {elapsed_time:.2f} seconds ({elapsed_time/60:.2f} minutes)")
    print("\nGenerated data structure:")
    print("  - generated-data/customers/  (10 parquet files)")
    print("  - generated-data/products/   (5 parquet files)")
    print("  - generated-data/sales-reps/ (1 parquet file)")
    print("  - generated-data/transactions/ (20 parquet files)")
    
except Exception as e:
    print(f"\n✗ ERROR: {str(e)}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
