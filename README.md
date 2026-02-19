# ETL-Project
# 📊 Serverless Sales Data Warehouse on AWS

> **End-to-end ETL pipeline demonstrating AWS serverless architecture proficiency**  
> From raw data generation to automated reporting and interactive dashboards — no servers, just services.

[![AWS](https://img.shields.io/badge/AWS-Serverless-FF9900?style=for-the-badge&logo=amazon-aws&logoColor=white)](https://aws.amazon.com/)
[![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg?style=for-the-badge)](LICENSE)

---

## 🎯 Project Overview

This project showcases a **production-grade serverless data warehouse** built entirely on AWS, demonstrating:

- **Multi-source data ingestion** (CSV, Parquet, APIs)
- **Automated ETL pipeline** with data quality checks
- **Dimensional data modeling** (star schema)
- **Serverless compute** (Lambda, Glue, Athena)
- **Workflow orchestration** (Step Functions)
- **Automated reporting** (EventBridge scheduling)
- **Interactive analytics** (QuickSight dashboards)
- **Monitoring & alerting** (CloudWatch, SNS)

### Business Use Case

Sales performance analytics platform that:
- Tracks daily sales metrics across products, regions, and sales representatives
- Generates automated daily/weekly reports
- Provides real-time analytics through interactive dashboards
- Monitors data quality and pipeline health

---

## 🏗️ Architecture

```
┌─────────────────┐
│  Data Sources   │
│  (S3 Landing)   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐      ┌──────────────┐
│  Lambda ETL     │◄─────┤ EventBridge  │  (Scheduled)
│  Functions      │      │  Triggers    │
└────────┬────────┘      └──────────────┘
         │
         ▼
┌─────────────────┐
│ Step Functions  │  (Orchestration)
│   Workflow      │
└────────┬────────┘
         │
         ├──► Data Quality Check
         ├──► Transform & Load
         └──► Generate Reports
         │
         ▼
┌─────────────────────────────────────────┐
│        AWS Glue Data Catalog            │
│    (Metadata & Schema Management)       │
└─────────────┬───────────────────────────┘
              │
              ▼
    ┌─────────────────┐
    │     Athena      │  (SQL Queries)
    │   Query Engine  │
    └────────┬────────┘
             │
             ▼
    ┌─────────────────┐
    │   QuickSight    │  (Dashboards)
    │   Analytics     │
    └─────────────────┘
```

### AWS Services Used

| Service | Purpose | Cost-Efficient? |
|---------|---------|-----------------|
| **S3** | Data lake storage (landing, raw, processed, curated zones) | ✅ Pay per GB |
| **Lambda** | Serverless compute for ETL logic | ✅ Pay per invocation |
| **AWS Glue** | Data catalog & schema discovery (crawlers) | ✅ Pay per DPU-hour |
| **Athena** | Interactive SQL queries on S3 data | ✅ Pay per TB scanned |
| **Step Functions** | Visual workflow orchestration | ✅ Pay per state transition |
| **EventBridge** | Scheduled automation (cron jobs) | ✅ Free for schedules |
| **QuickSight** | BI dashboards & visualizations | ✅ $24/user/month (free trial) |
| **CloudWatch** | Logging, monitoring, metrics | ✅ Free tier available |
| **SNS** | Email alerts & notifications | ✅ First 1K emails free |
| **IAM** | Security & access management | ✅ Always free |

**Estimated Monthly Cost**: $10-30 for this project volume (with AWS Free Tier)

---

## 📁 Repository Structure

```
sales-datawarehouse-project/
│
├── README.md                          # This file
├── LICENSE                            # MIT License
├── requirements.txt                   # Python dependencies
├── .gitignore                         # Git ignore patterns
│
├── data-generation/                   # 📂 Data Generation Scripts
│   ├── config.py                      # Configuration (volumes, dates, regions)
│   ├── generate_customers.py          # Customer master data generator
│   ├── generate_products.py           # Product catalog generator
│   ├── generate_sales_reps.py         # Sales representatives generator
│   ├── generate_transactions.py       # Transaction fact data generator
│   ├── master_generator.py            # Run all generators in sequence
│   └── README.md                      # Data generation documentation
│
├── generated-data/                    # 📂 Generated Sample Data (gitignored)
│   ├── customers/                     # Customer dimension data
│   ├── products/                      # Product dimension data
│   ├── sales-reps/                    # Sales rep dimension data
│   └── transactions/                  # Transaction fact data (partitioned)
│
├── aws-infrastructure/                # 📂 AWS Infrastructure as Code
│   ├── iam/
│   │   ├── glue-role-policy.json      # Glue service role policy
│   │   ├── lambda-role-policy.json    # Lambda execution role policy
│   │   └── stepfunctions-role-policy.json  # Step Functions role policy
│   │
│   ├── lambda-functions/              # Lambda function source code
│   │   ├── data-quality-checker/
│   │   │   └── lambda_function.py     # Validates incoming data
│   │   ├── etl-transformer/
│   │   │   ├── lambda_function.py     # Transforms raw → processed
│   │   │   └── requirements.txt       # pandas, pyarrow
│   │   └── report-generator/
│   │       └── lambda_function.py     # Generates HTML reports from Athena
│   │
│   ├── step-functions/
│   │   └── etl-state-machine.json     # Step Functions workflow definition
│   │
│   ├── glue/
│   │   ├── crawler-config.json        # Glue crawler configuration
│   │   └── etl-job.py                 # Optional Glue Spark job
│   │
│   ├── athena/
│   │   ├── create-database.sql        # Glue catalog database DDL
│   │   ├── sample-queries.sql         # Business intelligence queries
│   │   └── views/
│   │       ├── daily-sales-summary.sql
│   │       ├── product-performance.sql
│   │       └── rep-leaderboard.sql
│   │
│   ├── eventbridge/
│   │   ├── nightly-etl-rule.json      # Schedule ETL pipeline (2 AM)
│   │   └── daily-report-rule.json     # Schedule report generation (8 AM)
│   │
│   └── cloudformation/                # (Optional) Infrastructure as Code
│       ├── s3-buckets.yaml            # S3 bucket definitions
│       ├── iam-roles.yaml             # All IAM roles
│       ├── lambda-functions.yaml      # Lambda function resources
│       └── complete-stack.yaml        # Full stack template
│
├── docs/                              # 📂 Documentation
│   ├── architecture-diagram.png       # System architecture visual
│   ├── data-model-erd.png             # Entity relationship diagram
│   ├── setup-guide-cli.md             # AWS CLI setup instructions
│   ├── setup-guide-console.md         # AWS Console setup instructions
│   ├── DATASET_SUMMARY.md             # Generated data statistics
│   └── TROUBLESHOOTING.md             # Common issues & solutions
│
├── aws-proofs/                        # 📂 Project Evidence & Screenshots
│   ├── 01-iam-setup/
│   │   ├── iam-users.png              # IAM user creation proof
│   │   ├── iam-roles.png              # Service roles (Glue, Lambda, SFN)
│   │   └── iam-policies.png           # Attached policies
│   │
│   ├── 02-s3-data-lake/
│   │   ├── s3-bucket-structure.png    # Folder hierarchy
│   │   ├── s3-data-uploaded.png       # Uploaded data files
│   │   └── s3-lifecycle-policy.png    # Cost optimization rules
│   │
│   ├── 03-glue-catalog/
│   │   ├── glue-database.png          # Data catalog database
│   │   ├── glue-crawler-config.png    # Crawler settings
│   │   ├── glue-crawler-run.png       # Successful crawler execution
│   │   └── glue-tables.png            # Discovered tables
│   │
│   ├── 04-athena-queries/
│   │   ├── athena-workgroup.png       # Workgroup configuration
│   │   ├── query-daily-sales.png      # Daily revenue query result
│   │   ├── query-top-products.png     # Top 10 products query
│   │   └── query-rep-performance.png  # Sales rep ranking query
│   │
│   ├── 05-lambda-functions/
│   │   ├── lambda-list.png            # All Lambda functions
│   │   ├── quality-checker-code.png   # Code editor screenshot
│   │   ├── quality-checker-test.png   # Test execution result
│   │   ├── etl-transformer-config.png # Function configuration
│   │   └── report-generator-logs.png  # CloudWatch logs
│   │
│   ├── 06-step-functions/
│   │   ├── state-machine-definition.png   # Visual workflow graph
│   │   ├── execution-success.png      # Successful pipeline run
│   │   ├── execution-details.png      # Step-by-step execution trace
│   │   └── execution-history.png      # Multiple execution history
│   │
│   ├── 07-eventbridge-scheduling/
│   │   ├── nightly-etl-rule.png       # Scheduled ETL trigger
│   │   ├── daily-report-rule.png      # Scheduled report trigger
│   │   └── rule-targets.png           # Rule target configuration
│   │
│   ├── 08-quicksight-dashboards/
│   │   ├── dataset-connection.png     # Athena data source
│   │   ├── dashboard-overview.png     # Complete dashboard view
│   │   ├── chart-revenue-trend.png    # Line chart - revenue over time
│   │   ├── chart-top-products.png     # Bar chart - best sellers
│   │   ├── chart-payment-methods.png  # Pie chart - payment distribution
│   │   └── chart-rep-heatmap.png      # Heat map - rep performance
│   │
│   ├── 09-monitoring-alerting/
│   │   ├── cloudwatch-dashboard.png   # Custom metrics dashboard
│   │   ├── cloudwatch-alarms.png      # Configured alarms
│   │   ├── sns-topic.png              # SNS topic configuration
│   │   ├── sns-subscription.png       # Email subscription confirmation
│   │   └── alert-email-sample.png     # Sample alert email received
│   │
│   └── 10-cost-analysis/
│       ├── aws-cost-explorer.png      # Monthly cost breakdown
│       └── service-usage-report.png   # Service-wise usage metrics
│
├── sql-queries/                       # 📂 Reusable SQL Queries
│   ├── analytics/
│   │   ├── daily-revenue-summary.sql
│   │   ├── monthly-trend-analysis.sql
│   │   ├── customer-segmentation.sql
│   │   └── product-profitability.sql
│   │
│   └── data-quality/
│       ├── duplicate-check.sql
│       ├── null-value-check.sql
│       └── date-range-validation.sql
│
├── notebooks/                         # 📂 Jupyter Notebooks (Optional)
│   ├── data-exploration.ipynb         # Initial data analysis
│   ├── data-quality-report.ipynb      # Data quality metrics
│   └── performance-benchmarks.ipynb   # Query performance analysis
│
└── scripts/                           # 📂 Utility Scripts
    ├── upload-to-s3.sh                # Bulk S3 upload script
    ├── trigger-etl-manually.py        # Manual ETL pipeline trigger
    ├── download-athena-results.py     # Export query results
    └── cleanup-resources.sh           # Delete all AWS resources (careful!)
```

---

## 🚀 Quick Start

### Prerequisites

- **AWS Account** (Free Tier eligible)
- **Python 3.11+** installed locally
- **Git** for version control
- **Basic understanding** of AWS services

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/sales-datawarehouse-project.git
cd sales-datawarehouse-project
```

### Step 2: Generate Sample Data

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Generate sample data (10K customers, 500 products, 100K transactions)
cd data-generation
python master_generator.py

# This creates ~200MB of sample data in generated-data/ folder
```

### Step 3: Set Up AWS Infrastructure

**Option A: Using AWS Console (Recommended for Beginners)**

Follow the comprehensive guide: [`docs/setup-guide-console.md`](docs/setup-guide-console.md)

**Option B: Using AWS CLI (Faster for Experienced Users)**

Follow the CLI guide: [`docs/setup-guide-cli.md`](docs/setup-guide-cli.md)

### Step 4: Verify the Pipeline

1. **Check Glue Catalog**: AWS Console → Glue → Tables → Verify 4+ tables discovered
2. **Run Sample Queries**: Athena → Run queries from `sql-queries/analytics/`
3. **Trigger Pipeline**: Step Functions → sales-dw-etl-pipeline → Start execution
4. **View Dashboard**: QuickSight → Dashboards → Sales Performance Dashboard

---

## 📊 Data Model

### Dimensional Star Schema

```
                    ┌─────────────────┐
                    │   dim_date      │
                    │─────────────────│
                    │ date_key (PK)   │
                    │ full_date       │
                    │ year, month, day│
                    │ quarter         │
                    │ day_of_week     │
                    └────────┬────────┘
                             │
                             │
    ┌────────────────┐       │       ┌─────────────────┐
    │ dim_customer   │       │       │  dim_product    │
    │────────────────│       │       │─────────────────│
    │ customer_key   │       │       │ product_key     │
    │ customer_id    │       │       │ product_id      │
    │ customer_name  │       │       │ product_name    │
    │ segment        │       │       │ category        │
    │ region         │       │       │ subcategory     │
    │ lifetime_value │       │       │ unit_price      │
    └───────┬────────┘       │       └────────┬────────┘
            │                │                │
            │                │                │
            │       ┌────────▼────────┐       │
            └───────┤   fact_sales    ├───────┘
                    │─────────────────│
                    │ sale_id (PK)    │
                    │ date_key (FK)   │
                    │ customer_key(FK)│
                    │ product_key (FK)│
                    │ sales_rep_key(FK)│
                    │ quantity        │
                    │ total_amount    │
                    │ profit          │
                    │ profit_margin   │
                    └────────┬────────┘
                             │
                             │
                    ┌────────▼────────┐
                    │ dim_sales_rep   │
                    │─────────────────│
                    │ sales_rep_key   │
                    │ rep_id          │
                    │ rep_name        │
                    │ territory       │
                    │ manager_id      │
                    └─────────────────┘
```

### Data Volumes

| Table | Rows | Size | Partitioned? |
|-------|------|------|--------------|
| **dim_customer** | 10,000 | ~2 MB | No |
| **dim_product** | 500 | ~100 KB | No |
| **dim_sales_rep** | 50 | ~10 KB | No |
| **dim_date** | 730 (2 years) | ~50 KB | No |
| **fact_sales** | 100,000 | ~20 MB | Yes (by year/month) |

---

## 🛠️ ETL Pipeline Details

### Pipeline Stages

```
┌──────────────────────────────────────────────────────────────┐
│                    STEP FUNCTIONS WORKFLOW                    │
└──────────────────────────────────────────────────────────────┘

1️⃣  DataQualityCheck (Lambda)
    ├─ List files in S3 landing zone
    ├─ Validate file count, size, freshness
    ├─ Calculate quality score (0-100)
    └─ Pass/Fail decision
         │
         ▼
2️⃣  EvaluateQuality (Choice State)
    ├─ If quality_score >= 80 → Continue
    └─ If quality_score < 80  → FAIL pipeline
         │
         ▼
3️⃣  TransformAllTables (Parallel State)
    ├─ Branch 1: TransformCustomers (Lambda)
    ├─ Branch 2: TransformProducts (Lambda)
    ├─ Branch 3: TransformSalesReps (Lambda)
    └─ Branch 4: TransformTransactions (Lambda)
         │ (All branches run simultaneously)
         ▼
4️⃣  GenerateReport (Lambda)
    ├─ Query Athena for daily metrics
    ├─ Build HTML report
    ├─ Save to S3 reports/ folder
    └─ (Optional) Send email via SES
         │
         ▼
5️⃣  PipelineSucceeded ✅
```

### Lambda Functions

#### 1. Data Quality Checker (`data-quality-checker/`)

**Purpose**: Validates data before processing

**Checks**:
- Files exist in landing zone
- File sizes are adequate (> 1KB)
- Files are recent (uploaded within last 24 hours)
- No corrupt or zero-byte files

**Output**: Quality score (0-100) and detailed check results

#### 2. ETL Transformer (`etl-transformer/`)

**Purpose**: Cleanses and transforms raw data

**Transformations**:
- Normalize column names (lowercase, underscores)
- Remove duplicates
- Drop empty rows
- Convert data types
- Add audit columns (processed_at timestamp)
- Convert CSV → Parquet for efficiency

**Input**: S3 landing zone (CSV/Parquet)  
**Output**: S3 processed zone (Parquet, Snappy compressed)

#### 3. Report Generator (`report-generator/`)

**Purpose**: Creates automated business reports

**Features**:
- Queries Athena for daily/weekly metrics
- Generates HTML reports with CSS styling
- Saves reports to S3
- Email delivery via SNS/SES (optional)

**Metrics Included**:
- Total orders, revenue, profit
- Average order value
- Top products by revenue
- Sales rep performance rankings

---

## 📈 Sample Analytics Queries

### Daily Revenue Trend

```sql
SELECT 
    transaction_date,
    COUNT(*) AS num_orders,
    ROUND(SUM(total_amount), 2) AS daily_revenue,
    ROUND(AVG(total_amount), 2) AS avg_order_value,
    ROUND(SUM(profit), 2) AS daily_profit
FROM sales_datawarehouse.raw_transactions
WHERE transaction_date >= DATE_ADD('day', -30, CURRENT_DATE)
GROUP BY transaction_date
ORDER BY transaction_date DESC;
```

### Top 10 Products by Revenue

```sql
SELECT 
    t.product_id,
    p.product_name,
    p.category,
    COUNT(*) AS times_sold,
    SUM(t.quantity) AS units_sold,
    ROUND(SUM(t.total_amount), 2) AS total_revenue,
    ROUND(AVG(t.profit_margin), 2) AS avg_margin_pct
FROM sales_datawarehouse.raw_transactions t
LEFT JOIN sales_datawarehouse.raw_products p 
    ON t.product_id = p.product_id
GROUP BY t.product_id, p.product_name, p.category
ORDER BY total_revenue DESC
LIMIT 10;
```

### Sales Rep Leaderboard

```sql
SELECT 
    sales_rep_id,
    COUNT(*) AS total_orders,
    SUM(quantity) AS total_units,
    ROUND(SUM(total_amount), 2) AS total_sales,
    ROUND(SUM(profit), 2) AS total_profit,
    ROUND(AVG(profit_margin), 2) AS avg_margin_pct,
    RANK() OVER (ORDER BY SUM(total_amount) DESC) AS rank
FROM sales_datawarehouse.raw_transactions
WHERE YEAR(transaction_date) = YEAR(CURRENT_DATE)
GROUP BY sales_rep_id
ORDER BY total_sales DESC;
```

More queries available in [`sql-queries/analytics/`](sql-queries/analytics/)

---

## 📸 Screenshots & Proofs

All AWS setup proofs and dashboard screenshots are organized in the [`aws-proofs/`](aws-proofs/) folder:

### Key Screenshots

1. **IAM Setup** - User and role creation
2. **S3 Data Lake** - Folder structure with uploaded data
3. **Glue Catalog** - Crawler runs and discovered tables
4. **Athena Queries** - Sample query results
5. **Lambda Functions** - Code, configuration, test results
6. **Step Functions** - Visual workflow with successful execution
7. **EventBridge** - Scheduled automation rules
8. **QuickSight Dashboard** - Interactive charts and KPIs
9. **Monitoring** - CloudWatch alarms and SNS alerts
10. **Cost Analysis** - AWS Cost Explorer breakdown

> 📁 **View all proofs**: [aws-proofs/](aws-proofs/)

---

## 💰 Cost Optimization

### Built-in Cost Controls

1. **S3 Lifecycle Policies**
   - Raw data → Standard-IA after 30 days
   - Raw data → Glacier after 90 days
   - Athena results auto-delete after 7 days

2. **Lambda Optimization**
   - Right-sized memory allocation (512MB - 1024MB)
   - Efficient code with minimal execution time
   - Connection pooling for database access

3. **Athena Optimization**
   - Parquet format with Snappy compression (10x smaller than CSV)
   - Partitioning by date (reduces data scanned)
   - Column projection (select only needed columns)

4. **Glue Crawler**
   - On-demand execution (not continuous)
   - Runs only when new data arrives

5. **QuickSight**
   - SPICE import (in-memory) reduces Athena queries
   - Standard edition ($9/month) not Enterprise

### Estimated Monthly Cost Breakdown

| Service | Usage | Cost |
|---------|-------|------|
| **S3 Storage** | 1 GB data | $0.02 |
| **S3 Requests** | 10K PUT, 50K GET | $0.10 |
| **Lambda** | 100 invocations/day @ 512MB, 30s avg | $0.50 |
| **Glue Crawler** | 1 run/day, 5 min/run | $0.44 |
| **Athena** | 100 queries/day, 100 MB scanned each | $1.50 |
| **Step Functions** | 30 executions/month | $0.75 |
| **CloudWatch Logs** | 1 GB logs | $0.50 |
| **SNS** | 100 emails/month | FREE |
| **QuickSight** | 1 user Standard | $9.00 (after free trial) |
| **Total** | | **~$12-15/month** |

> 💡 **With AWS Free Tier**: First year costs ~$5-10/month

---

## 🐛 Troubleshooting

### Common Issues

#### Issue 1: Glue Crawler Fails

**Symptoms**: Crawler shows "Failed" status  
**Cause**: IAM role missing S3 permissions  
**Solution**:
```bash
# Verify GlueETLRole has AmazonS3FullAccess attached
# AWS Console → IAM → Roles → GlueETLRole → Permissions tab
```

#### Issue 2: Lambda Timeout

**Symptoms**: Lambda function times out after 3 seconds  
**Cause**: Default timeout too short for processing  
**Solution**:
```bash
# Increase timeout to 5-10 minutes
# Lambda → Configuration → General configuration → Timeout
```

#### Issue 3: Athena "HIVE_CANNOT_OPEN_SPLIT"

**Symptoms**: Query fails with Hive error  
**Cause**: Corrupted or inaccessible file in S3  
**Solution**:
```sql
-- Check for zero-byte files
SELECT "$path", "$file_size" 
FROM sales_datawarehouse.raw_transactions 
WHERE "$file_size" = 0;
```

#### Issue 4: QuickSight Cannot Access S3

**Symptoms**: Dataset refresh fails with access denied  
**Cause**: QuickSight not granted S3 bucket access  
**Solution**:
```bash
# QuickSight → Manage → Security & Permissions → 
# Add S3 bucket → Select your bucket
```

More troubleshooting guides: [`docs/TROUBLESHOOTING.md`](docs/TROUBLESHOOTING.md)

---

## 🧪 Testing

### Manual Tests

1. **Data Quality Check**
   ```bash
   # Test Lambda directly
   # Lambda Console → sales-dw-quality-checker → Test tab
   # Input: {"bucket": "your-bucket-name", "prefix": "landing/csv-uploads/"}
   ```

2. **ETL Transformer**
   ```bash
   # Upload test file to S3
   # Invoke Lambda with file path
   # Verify processed output in processed/ folder
   ```

3. **End-to-End Pipeline**
   ```bash
   # Step Functions → Start execution
   # Monitor each step in visual workflow
   # Check S3 for processed data and reports
   ```

### Automated Tests (Future Enhancement)

- Unit tests for Lambda functions (pytest)
- Integration tests for Step Functions workflow
- Data quality tests (Great Expectations)

---

## 🔐 Security Best Practices

### Implemented Security

✅ **IAM Least Privilege** - Each service has only required permissions  
✅ **S3 Bucket Encryption** - SSE-S3 encryption at rest  
✅ **S3 Block Public Access** - All public access blocked  
✅ **VPC Endpoints** - (Optional) Private connectivity for Lambda  
✅ **CloudTrail Logging** - Audit trail for all API calls  
✅ **Secrets Manager** - Store API keys and credentials securely  

### Additional Recommendations

- Enable MFA on root and IAM users
- Rotate access keys every 90 days
- Use AWS Config for compliance monitoring
- Enable GuardDuty for threat detection
- Implement data lifecycle policies

---

## 📚 Learning Resources

### AWS Documentation

- [AWS Glue Developer Guide](https://docs.aws.amazon.com/glue/)
- [Amazon Athena User Guide](https://docs.aws.amazon.com/athena/)
- [AWS Lambda Developer Guide](https://docs.aws.amazon.com/lambda/)
- [AWS Step Functions Guide](https://docs.aws.amazon.com/step-functions/)
- [Amazon QuickSight User Guide](https://docs.aws.amazon.com/quicksight/)

### Tutorials & Courses

- [AWS Serverless Data Analytics](https://aws.amazon.com/big-data/datalakes-and-analytics/)
- [Building Data Lakes on AWS](https://aws.amazon.com/big-data/datalakes-and-analytics/data-lakes/)
- [AWS Well-Architected Framework](https://aws.amazon.com/architecture/well-architected/)

---

## 🚀 Future Enhancements

### Phase 2 - Advanced Features

- [ ] **Real-time streaming** with Kinesis Data Streams
- [ ] **ML predictions** using SageMaker (customer churn, demand forecasting)
- [ ] **Data quality monitoring** with AWS Deequ or Great Expectations
- [ ] **CI/CD pipeline** with AWS CodePipeline for Lambda deployments
- [ ] **Infrastructure as Code** complete CloudFormation/Terraform templates
- [ ] **CDC (Change Data Capture)** from operational databases using DMS
- [ ] **Data mesh architecture** with multiple data domains
- [ ] **GraphQL API** layer using AWS AppSync
- [ ] **Natural language queries** using Amazon Q or Bedrock

### Phase 3 - Enterprise Features

- [ ] Multi-account setup with AWS Organizations
- [ ] Data governance with AWS Lake Formation
- [ ] Advanced security with KMS customer-managed keys
- [ ] Cost allocation tags and detailed billing analysis
- [ ] Disaster recovery with cross-region replication

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

### How to Contribute

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👤 Author

**Your Name**

- GitHub: [@yourusername](https://github.com/yourusername)
- LinkedIn: [Your LinkedIn](https://linkedin.com/in/yourprofile)
- Portfolio: [yourportfolio.com](https://yourportfolio.com)

---

## 🙏 Acknowledgments

- AWS documentation and sample code
- Faker library for realistic data generation
- pandas and pyarrow for efficient data processing
- The open-source community

---

## 📞 Support

If you have questions or need help:

1. Check the [Troubleshooting Guide](docs/TROUBLESHOOTING.md)
2. Open an [Issue](https://github.com/yourusername/sales-datawarehouse-project/issues)
3. Join the [Discussions](https://github.com/yourusername/sales-datawarehouse-project/discussions)

---

<div align="center">

**⭐ If this project helped you learn AWS serverless architecture, please star the repository! ⭐**

[![Star on GitHub](https://img.shields.io/github/stars/yourusername/sales-datawarehouse-project?style=social)](https://github.com/yourusername/sales-datawarehouse-project)

</div>

---

## 📊 Project Statistics

![Lines of Code](https://img.shields.io/badge/Lines%20of%20Code-2000+-blue)
![AWS Services](https://img.shields.io/badge/AWS%20Services-10-orange)
![Data Generated](https://img.shields.io/badge/Sample%20Data-200MB-green)
![Automated](https://img.shields.io/badge/Automation-100%25-brightgreen)

**Last Updated**: February 2024  
**Project Status**: ✅ Production Ready
