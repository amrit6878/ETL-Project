"""
Non-interactive version of master generator
"""

import sys
import time
import os

# Suppress input prompts by replacing input function
import builtins
original_input = builtins.input
builtins.input = lambda prompt='': 'n'

from generate_customers import generate_all_customers
from generate_products import generate_products
from generate_sales_reps import generate_sales_reps
from generate_transactions import generate_all_transactions

def main():
    print("=" * 60)
    print("SALES DATA WAREHOUSE - DATA GENERATION")
    print("=" * 60)
    print()
    
    start_time = time.time()
    
    try:
        # Step 1: Generate customers
        print("\n[1/4] GENERATING CUSTOMERS")
        print("-" * 60)
        generate_all_customers()
        
        # Step 2: Generate products
        print("\n[2/4] GENERATING PRODUCTS")
        print("-" * 60)
        generate_products()
        
        # Step 3: Generate sales reps
        print("\n[3/4] GENERATING SALES REPRESENTATIVES")
        print("-" * 60)
        generate_sales_reps()
        
        # Step 4: Generate transactions
        print("\n[4/4] GENERATING TRANSACTIONS")
        print("-" * 60)
        generate_all_transactions()
        
        elapsed_time = time.time() - start_time
        
        print("\n" + "=" * 60)
        print("✓ DATA GENERATION COMPLETE!")
        print("=" * 60)
        print(f"Total time: {elapsed_time:.2f} seconds ({elapsed_time/60:.2f} minutes)")
        print("\nGenerated data is in the 'generated-data' folder")
        
    except Exception as e:
        print(f"\n✗ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
