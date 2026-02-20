"""
Configuration for data generation
Adjust these numbers based on your needs
"""

# Data volumes for large-scale AWS processing (~3-4GB target)
# Increased transactions to better reach 3-4GB on-disk (parquet compressed)
NUM_CUSTOMERS = 2000000      # 2M customers
NUM_PRODUCTS = 200000        # 200K products
NUM_SALES_REPS = 20000       # 20K sales representatives
NUM_TRANSACTIONS = 85000000  # 85M transactions (~3-4GB expected compressed)

# Date range for transactions
START_DATE = '2023-01-01'
END_DATE = '2024-12-31'

# Batch sizes for chunk processing (critical for RAM efficiency)
# Keep transaction batches at 1M to limit memory usage on your machine
CUSTOMER_BATCH_SIZE = 200000  # Larger batches for efficiency
PRODUCT_BATCH_SIZE = 50000
TRANSACTION_BATCH_SIZE = 1000000  # 1M transactions per batch

# File output settings
OUTPUT_FORMAT = 'parquet'  # or 'csv' - parquet is more efficient
COMPRESSION = 'snappy'     # for parquet files

# Regions and categories
REGIONS = ['North', 'South', 'East', 'West', 'Central']
COUNTRIES = ['USA', 'Canada', 'UK', 'Germany', 'France', 'Australia']
PRODUCT_CATEGORIES = ['Electronics', 'Clothing', 'Home & Garden', 'Sports', 'Books']
CUSTOMER_SEGMENTS = ['Bronze', 'Silver', 'Gold', 'Platinum']
