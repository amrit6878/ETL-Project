# Generated Dataset Summary

**Generation Date:** February 13, 2026

## Dataset Statistics

| Table | Records | Files | Size | Format |
|-------|---------|-------|------|--------|
| Customers | 2,000,000 | 10 | ~130MB | Parquet |
| Products | 200,000 | 4 | ~8MB | Parquet |
| Sales Representatives | 20,000 | 1 | ~1.3MB | Parquet |
| Transactions | 85,000,000 | 85 | ~3.4GB | Parquet |
| **TOTAL** | **87,220,000** | **100** | **~6.8GB** | Parquet |

## Directory Structure

```
generated-data/
├── customers/           (10 parquet files × 200K rows each)
│   ├── customers_batch_00000.parquet
│   ├── customers_batch_00001.parquet
│   └── ... (10 files total)
├── products/            (4 parquet files × 50K rows each)
│   ├── products_batch_00000.parquet
│   └── ... (4 files total)
├── sales-reps/          (1 parquet file × 20K rows)
│   └── sales_reps_batch_00000.parquet
└── transactions/        (85 parquet files × 1M rows each)
    ├── transactions_batch_00000.parquet
    ├── transactions_batch_00001.parquet
    └── ... (85 files total)
```

## Data Schema

### Customers Table
- `customer_id` (string): CUST{8-digit}
- `customer_name` (string): Faker-generated names
- `email` (string): Email addresses
- `phone` (string): Phone numbers
- `segment` (string): Bronze, Silver, Gold, Platinum
- `region` (string): North, South, East, West, Central
- `country` (string): USA, Canada, UK, Germany, France, Australia
- `city` (string): Cities
- `state` (string): US state abbreviations
- `zip_code` (string): Zip codes
- `acquisition_date` (date): Last 5 years
- `lifetime_value` (float): $100 - $500,000
- `created_at` (timestamp): Generation timestamp

### Products Table
- `product_id` (string): PROD{8-digit}
- `product_name` (string): Faker-generated names
- `category` (string): Electronics, Clothing, Home & Garden, Sports, Books
- `subcategory` (string): Faker-generated
- `unit_price` (float): $10 - $1,000
- `cost_price` (float): $5 - $500
- `supplier_id` (string): SUPP{6-digit}
- `stock_quantity` (integer): 0 - 10,000
- `reorder_point` (integer): 50 - 500
- `created_at` (timestamp): Generation timestamp

### Sales Representatives Table
- `sales_rep_id` (string): SREP{8-digit}
- `name` (string): Faker-generated names
- `email` (string): Email addresses
- `phone` (string): Phone numbers
- `region` (string): North, South, East, West, Central
- `territory` (string): City names
- `hire_date` (date): Last 15 years
- `commission_rate` (float): 1% - 25%
- `created_at` (timestamp): Generation timestamp

### Transactions Table
- `transaction_id` (string): TXN{12-digit}
- `customer_id` (string): Reference to CUST{8-digit}
- `product_id` (string): Reference to PROD{8-digit}
- `sales_rep_id` (string): Reference to SREP{8-digit}
- `transaction_date` (date): 2023-01-01 to 2024-12-31
- `quantity` (integer): 1 - 500
- `unit_price` (float): $10 - $1,000
- `discount_percent` (float): 0% - 50%
- `tax_amount` (float): $10 - $1,000
- `total_amount` (float): $50 - $50,000
- `payment_method` (string): Credit Card, Debit Card, Check, Bank Transfer, Online Payment
- `region` (string): North, South, East, West, Central
- `created_at` (timestamp): Generation timestamp

## Generation Configuration

- **Batch Processing:** Optimized to keep memory usage under 1GB
- **Compression:** Snappy compression on all Parquet files
- **Format:** Apache Parquet (columnar format, ideal for AWS analytics)
- **Seed:** Faker seeded for reproducibility
- **Total Generation Time:** ~23 minutes
- **Peak Memory Usage:** < 1GB

## AWS ETL Readiness

✓ Data structure is ready for AWS Glue, Athena, and S3 analytics
✓ Parquet format is optimal for Columnar storage and query performance
✓ Files are distributed across batches for parallel processing
✓ Schema is normalized and suitable for star schema data warehouse design

## Usage

To read data in Python:
```python
import pandas as pd

# Read a single parquet file
df = pd.read_parquet('generated-data/customers/customers_batch_00000.parquet')

# Read all customer files
import glob
customer_files = glob.glob('generated-data/customers/*.parquet')
df_all = pd.concat([pd.read_parquet(f) for f in customer_files])
```

To upload to AWS S3:
```bash
# Example AWS CLI command
aws s3 cp generated-data/ s3://your-bucket/etl-data/ --recursive
```
