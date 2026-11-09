# BoQ Data Quality Gate 🏗️📊

An automated data validation and quality scoring pipeline built for construction commercial operations, cost control, and BIM/VDC data governance. 

## The Problem
In mega-projects and regional construction operations, subcontractor Bill of Quantities (BoQ) submissions often arrive riddled with silent errors: negative quantities, missing work descriptions, unstandardized classification codes, and corrupted data types. Manually reviewing these spreadsheets wastes hours of engineering and cost-control time.

## The Solution
This tool acts as an automated data quality gate. It ingests raw subcontractor CSV/Excel sheets, enforces strict structural schemas programmatically using `Pandera`, computes an objective **Data Quality Score (0-100)**, and outputs a clean exception log for instant subcontractor correction.

---

## Tech Stack
* **Language:** Python 3.10+
* **Environment:** WSL2 / Ubuntu Linux
* **Data Processing:** `pandas`
* **Schema Validation:** `pandera`

---

## How It Works

1. **Schema Enforcement:** Defines strict rules for item codes (regex pattern matching), mandatory descriptions, allowed engineering units (`m3`, `m2`, `ton`, etc.), and numeric boundaries (`>= 0` for quantities and rates).
2. **Lazy Validation:** Evaluates the entire dataframe to capture *all* violations simultaneously rather than failing on the first error.
3. **Automated Scoring & Logging:** Calculates a data quality penalty ratio and exports an audit-ready `boq_validation_error_log.csv` file.

---

## Quick Start (Local Execution)

1. Clone the repository:
   ```bash
   git clone [https://github.com/3adoshka/boq-data-quality-gate.git](https://github.com/3adoshka/boq-data-quality-gate.git)
   cd boq-data-quality-gate
