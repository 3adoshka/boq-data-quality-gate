import pandas as pd
import pandera.pandas as pa
from pandera import Column, Check, DataFrameSchema
import sys

# 1. Define the Strict Data Quality Schema
boq_schema = DataFrameSchema({
    "item_code": Column(str, Check.str_matches(r"^[A-Z0-9_\-\.]+$"), nullable=False, description="Standardized classification code"),
    "description": Column(str, nullable=False, description="Work item description"),
    "unit": Column(str, Check.isin(["m3", "m2", "m", "ton", "pcs", "ls"]), nullable=False, description="Valid engineering unit"),
    "quantity": Column(float, Check.ge(0), nullable=False, description="Quantity must be numeric and >= 0"),
    "unit_rate": Column(float, Check.ge(0), nullable=False, description="Unit rate must be numeric and >= 0")
}, strict=True)

def run_boq_validation(csv_path: str):
    print(f"[*] Ingesting subcontractor sheet: {csv_path}...")
    try:
        df = pd.read_csv(csv_path)
    except Exception as e:
        print(f"[!] Critical Error: Failed to load CSV file. Details: {e}")
        sys.exit(1)
        
    total_rows = len(df)
    if total_rows == 0:
        print("[!] Error: The uploaded BoQ sheet is empty.")
        return

    print(f"[*] Total line items loaded: {total_rows}")
    print("[*] Running Pandera schema validation gate...")

    try:
        validated_df = boq_schema.validate(df, lazy=True)
        print("\n[SUCCESS] BoQ passed all validation checks cleanly! Data quality score: 100/100.")
        
    except pa.errors.SchemaErrors as err:
        print("\n[!] VALIDATION FAILED: Data corruption detected in subcontractor submission.")
        print("-" * 60)
        
        failure_cases = err.failure_cases
        error_count = len(failure_cases)
        
        penalty_ratio = min(error_count / (total_rows * len(boq_schema.columns)), 1.0)
        quality_score = max(0, int(100 * (1 - penalty_ratio)))
        
        print(f"DATA QUALITY SCORE: {quality_score} / 100")
        print(f"Total Schema Violations Found: {error_count}\n")
        
        print("--- Detailed Exception Log ---")
        print(failure_cases[['column', 'check', 'failure_case', 'index']])
        print("-" * 60)
        
        failure_cases.to_csv("boq_validation_error_log.csv", index=False)
        print("[*] Generated export: 'boq_validation_error_log.csv' for automated subcontractor correction.")

if __name__ == "__main__":
    target_file = sys.argv[1] if len(sys.argv) > 1 else "dirty_subcontractor_boq.csv"
    run_boq_validation(target_file)
def calculate_boq_health_score(total_rows, total_errors):
    """Calculates a percentage health score for the bill of quantities dataset."""
    if total_rows <= 0:
        return 100.0
    score = max(0.0, ((total_rows - total_errors) / total_rows) * 100.0)
    print(f"[*] BoQ Data Quality Health Score: {score:.2f}% (Errors: {total_errors}/{total_rows})")
    return score
