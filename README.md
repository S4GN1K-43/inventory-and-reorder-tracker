# Inventory and Reorder Tracker

A Python-based inventory management system developed as part of the **Python Laboratory (OEC382)** project at the **Institute of Engineering & Management (IEM), Saltlake**.

## Project Overview

The Inventory and Reorder Tracker is designed to simplify inventory management by maintaining stock records, tracking stock additions and removals, identifying items that need replenishment, and generating inventory and sales reports.

The project uses Python programming concepts and libraries to perform data handling, statistical analysis, reporting, and graphical visualisation.

## Features

- **View Inventory:** Display all available inventory items.
- **Add Stock:** Increase the quantity of an existing item.
- **Remove Stock:** Reduce stock quantities and record stock issues.
- **Reorder Alerts:** Identify items whose current stock reaches or falls below their reorder level.
- **NumPy Analysis:** Perform statistical calculations on inventory data.
- **Pandas Reports:** Generate category-wise inventory summaries.
- **Monthly Sales Report:** Analyse monthly sales records.
- **JSON Export:** Export inventory records into JSON format.
- **Reorder Threshold Comparison:** Compare inventory against different stock thresholds.
- **Data Visualisation:** Generate stock, sales, category and monthly trend charts.
- **Testing:** Run built-in test cases to check program functionality.

## Technologies Used

- Python 3
- NumPy
- Pandas
- Matplotlib
- CSV
- JSON

## Project Structure

```text
inventory-and-reorder-tracker/
│
├── inventory_tracker.py
├── inventory.csv
├── monthly_sales.csv
├── requirements.txt
├── README.md
│
├── docs/
│   └── project-report.pdf
│
└── screenshots/
```

## Dataset Information

### inventory.csv

The inventory dataset contains 12 electronics-related items.

| Column        | Description                |
| ------------- | -------------------------- |
| item_id       | Unique item identification |
| item_name     | Name of the inventory item |
| category      | Item category              |
| price         | Unit price                 |
| stock         | Current available quantity |
| monthly_sales | Monthly sales quantity     |
| reorder_level | Minimum stock threshold    |

### monthly_sales.csv

This file contains monthly sales records for January to April.

| Column    | Description                |
| --------- | -------------------------- |
| month     | Sales month                |
| item_id   | Unique item identification |
| item_name | Name of the item           |
| category  | Item category              |
| sales     | Quantity sold              |

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/S4GN1K-43/inventory-and-reorder-tracker.git
```

### 2. Navigate to the project directory

```bash
cd inventory-and-reorder-tracker
```

### 3. Install the required libraries

```bash
pip install -r requirements.txt
```

### 4. Run the program

```bash
python inventory_tracker.py
```

Make sure both CSV files are present in the same working directory as the Python program.

## Reorder Logic

The application checks the stock quantity against the item's individual reorder level.

**Condition:**

```python
if stock <= reorder_level:
    print("REORDER REQUIRED")
```

For example, if Raspberry Pi has 5 units in stock and its reorder level is 5, the system generates a reorder alert.

## Sample Inventory Statistics

Based on the initial demonstration dataset:

| Metric                | Value |
| --------------------- | ----: |
| Total inventory items |    12 |
| Total available stock |   197 |
| Total monthly sales   |   222 |
| Average monthly sales |  18.5 |
| Highest monthly sales |    35 |
| Lowest monthly sales  |     6 |

## Team Members

| Name              | Roll No. |
| ----------------- | -------: |
| Sagnik Biswas     |      145 |
| Sagnik Das        |      141 |
| Subhrajyoti Ghosh |      143 |
| Saptarshi Mistry  |      158 |
| Suman Chattaraj   |      144 |

**Department:** Electronics and Communications Engineering
**Institution:** Institute of Engineering & Management, Saltlake
**Course:** Python Laboratory (OEC382)
**Academic Session:** 2026–2027

## Future Improvements

- Graphical user interface (GUI)
- Database integration
- Barcode-based inventory tracking
- Supplier management
- Automated low-stock notifications
- Inventory forecasting

## Acknowledgement

We sincerely thank our project guides and the faculty members of the Department of Electronics and Communications Engineering for their guidance and support throughout the development of this project.

---

**Developed as an academic Python Laboratory project at IEM Saltlake.**

