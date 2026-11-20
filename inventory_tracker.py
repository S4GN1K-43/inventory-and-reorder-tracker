import csv
import json
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# ==========================================
# 1. CONFIGURATION
# ==========================================

INVENTORY_FILE = "inventory.csv"
SALES_FILE = "monthly_sales.csv"
JSON_FILE = "inventory_summary.json"
CHART_DIR = "charts"


# ==========================================
# 2. ITEM CLASS (OOP)
# ==========================================

class Item:

    def __init__(self, item_id, item_name, category,
                 price, stock, monthly_sales, reorder_level):

        self.item_id = item_id
        self.item_name = item_name
        self.category = category
        self.price = float(price)
        self.stock = int(stock)
        self.monthly_sales = int(monthly_sales)
        self.reorder_level = int(reorder_level)

    def needs_reorder(self):
        return self.stock <= self.reorder_level

    def stock_value(self):
        return self.stock * self.price

    def __str__(self):
        return f"{self.item_name} - {self.stock} units"


# ==========================================
# 3. CSV FILE HANDLING
# ==========================================

def load_inventory(filename):

    inventory = []

    try:
        with open(filename, "r", newline="", encoding="utf-8") as file:

            reader = csv.DictReader(file)

            required = {
                "item_id", "item_name", "category", "price",
                "stock", "monthly_sales", "reorder_level"
            }

            if not required.issubset(reader.fieldnames or []):
                raise ValueError("Invalid CSV column headings.")

            seen_ids = set()

            for row in reader:

                item = Item(
                    row["item_id"],
                    row["item_name"],
                    row["category"],
                    row["price"],
                    row["stock"],
                    row["monthly_sales"],
                    row["reorder_level"]
                )

                if (not item.item_id or not item.item_name
                        or not item.category):
                    raise ValueError("Empty item information found.")

                if item.item_id in seen_ids:
                    raise ValueError("Duplicate item ID found.")

                if (item.price < 0 or item.stock < 0
                        or item.monthly_sales < 0
                        or item.reorder_level < 0):
                    raise ValueError("Negative inventory data found.")

                seen_ids.add(item.item_id)
                inventory.append(item)

    except FileNotFoundError:
        print("Inventory CSV file not found.")

    except (ValueError, TypeError, KeyError) as error:
        print("Invalid inventory data:", error)
        return []

    return inventory


def save_inventory(inventory):

    with open(INVENTORY_FILE, "w", newline="", encoding="utf-8") as file:

        fields = [
            "item_id", "item_name", "category", "price",
            "stock", "monthly_sales", "reorder_level"
        ]

        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()

        for item in inventory:
            writer.writerow({
                "item_id": item.item_id,
                "item_name": item.item_name,
                "category": item.category,
                "price": item.price,
                "stock": item.stock,
                "monthly_sales": item.monthly_sales,
                "reorder_level": item.reorder_level
            })


# ==========================================
# 4. INVENTORY FUNCTIONS
# ==========================================

def find_item(inventory, item_id):

    for item in inventory:
        if item.item_id.lower() == item_id.lower():
            return item

    return None


def add_stock(item, quantity):

    if isinstance(quantity, bool) or not isinstance(quantity, int):
        return False, "Quantity must be an integer."

    if quantity <= 0:
        return False, "Quantity must be positive."

    item.stock += quantity

    return True, f"{quantity} units added successfully."


def remove_stock(item, quantity):

    if isinstance(quantity, bool) or not isinstance(quantity, int):
        return False, "Quantity must be an integer."

    if quantity <= 0:
        return False, "Quantity must be positive."

    if quantity > item.stock:
        return False, "Insufficient stock! Stock-out prevented."

    item.stock -= quantity
    item.monthly_sales += quantity

    return True, f"{quantity} units sold successfully."


def get_reorder_items(inventory):

    return [item for item in inventory if item.needs_reorder()]


def display_inventory(inventory):

    print("\n" + "=" * 90)
    print("                    CURRENT INVENTORY")
    print("=" * 90)

    print(f"{'ID':<8}{'ITEM':<22}{'CATEGORY':<19}"
          f"{'PRICE':<10}{'STOCK':<9}{'SALES':<9}{'STATUS'}")

    print("-" * 90)

    for item in inventory:

        status = "REORDER" if item.needs_reorder() else "OK"

        print(
            f"{item.item_id:<8}"
            f"{item.item_name:<22}"
            f"{item.category:<19}"
            f"{item.price:<10.2f}"
            f"{item.stock:<9}"
            f"{item.monthly_sales:<9}"
            f"{status}"
        )

    print("=" * 90)


def stock_operations(inventory, operation):

    item_id = input("Enter Item ID: ").strip()
    item = find_item(inventory, item_id)

    if item is None:
        print("Item not found.")
        return

    try:
        quantity = int(input("Enter quantity: "))

        if operation == "in":
            success, message = add_stock(item, quantity)
        else:
            success, message = remove_stock(item, quantity)

        print(message)

        if success:
            save_inventory(inventory)

    except ValueError:
        print("Invalid input! Enter a whole number.")


# ==========================================
# 5. REORDER ALERTS
# ==========================================

def show_reorder_items(inventory):

    items = get_reorder_items(inventory)

    print("\nREORDER ALERTS")
    print("-" * 50)

    if not items:
        print("No items currently require reordering.")

    for item in items:
        print(
            f"{item.item_name}: {item.stock} units remaining "
            f"(Reorder level: {item.reorder_level})"
        )


# ==========================================
# 6. NUMPY STATISTICAL ANALYSIS
# ==========================================

def numpy_analysis(inventory):

    sales = np.array(
        [item.monthly_sales for item in inventory],
        dtype=float
    )

    stock = np.array(
        [item.stock for item in inventory],
        dtype=float
    )

    if len(sales) == 0:
        print("No data available.")
        return

    print("\nNUMPY STATISTICAL ANALYSIS")
    print("-" * 45)

    print("Total sales:", np.sum(sales))
    print("Average sales:", np.mean(sales))
    print("Maximum sales:", np.max(sales))
    print("Minimum sales:", np.min(sales))
    print("Sales standard deviation:", np.std(sales))

    print("Total current stock:", np.sum(stock))
    print("Average current stock:", np.mean(stock))

    print("Total inventory value:",
          sum(item.stock_value() for item in inventory))

    # Moving average of sales in current item order
    if len(sales) >= 3:
        moving_avg = np.convolve(
            sales, np.ones(3) / 3, mode="valid"
        )
        print("3-item moving averages:", moving_avg)


# ==========================================
# 7. PANDAS DATAFRAME
# ==========================================

def inventory_to_dataframe(inventory):

    data = []

    for item in inventory:

        data.append({
            "item_id": item.item_id,
            "item_name": item.item_name,
            "category": item.category,
            "price": item.price,
            "stock": item.stock,
            "monthly_sales": item.monthly_sales,
            "reorder_level": item.reorder_level,
            "stock_value": item.stock_value(),
            "needs_reorder": item.needs_reorder()
        })

    return pd.DataFrame(data)


# ==========================================
# 8. CATEGORY REPORT
# ==========================================

def category_report(df):

    report = df.groupby("category").agg(
        total_sales=("monthly_sales", "sum"),
        average_stock=("stock", "mean"),
        total_stock_value=("stock_value", "sum")
    ).reset_index()

    return report


# ==========================================
# 9. MONTHLY SALES REPORT
# ==========================================

def monthly_report():

    try:
        df = pd.read_csv(SALES_FILE)

        required = {"month", "item_id", "item_name", "category", "sales"}

        if not required.issubset(df.columns):
            print("Invalid monthly sales CSV format.")
            return

        if df.empty or df["month"].isna().any():
            print("Monthly sales data is empty or incomplete.")
            return

        if (df["sales"].isna().any()
                or (df["sales"] < 0).any()):
            print("Invalid sales values.")
            return

        report = df.groupby("month")["sales"].sum().reset_index()

        print("\nMONTHLY SALES REPORT")
        print(report)

        return report

    except FileNotFoundError:
        print("monthly_sales.csv not found.")


# ==========================================
# 10. JSON EXPORT
# ==========================================

def export_json(df):

    df.to_json(
        JSON_FILE,
        orient="records",
        indent=4
    )

    print("JSON report exported successfully:", JSON_FILE)


# ==========================================
# 11. REORDER THRESHOLD COMPARISON
# ==========================================

def compare_reorder_thresholds(df):

    results = []

    for threshold in [5, 10]:

        count = (df["stock"] <= threshold).sum()

        results.append({
            "threshold": threshold,
            "items_requiring_reorder": int(count)
        })

    result_df = pd.DataFrame(results)

    print("\nREORDER THRESHOLD COMPARISON")
    print(result_df.to_string(index=False))

    return result_df


# ==========================================
# 12. MATPLOTLIB VISUALISATIONS
# ==========================================

def plot_stock_levels(df):

    os.makedirs(CHART_DIR, exist_ok=True)

    plt.figure(figsize=(12, 6))

    plt.bar(df["item_name"], df["stock"], label="Current stock")

    plt.xlabel("Items")
    plt.ylabel("Quantity")
    plt.title("Current Inventory Stock Levels")

    plt.xticks(rotation=45, ha="right")
    plt.legend()
    plt.tight_layout()

    plt.savefig(os.path.join(CHART_DIR, "stock_levels.png"))
    plt.show()


def plot_sales(df):

    os.makedirs(CHART_DIR, exist_ok=True)

    plt.figure(figsize=(12, 6))

    plt.bar(df["item_name"], df["monthly_sales"])

    plt.xlabel("Items")
    plt.ylabel("Units sold")
    plt.title("Monthly Sales by Item")

    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()

    plt.savefig(os.path.join(CHART_DIR, "monthly_sales.png"))
    plt.show()


def plot_category_sales(df):

    os.makedirs(CHART_DIR, exist_ok=True)

    category_data = df.groupby("category")["monthly_sales"].sum()

    plt.figure(figsize=(10, 6))

    category_data.plot(kind="bar")

    plt.xlabel("Category")
    plt.ylabel("Total sales")
    plt.title("Category-wise Sales")

    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()

    plt.savefig(os.path.join(CHART_DIR, "category_sales.png"))
    plt.show()


def plot_monthly_sales():

    report = monthly_report()

    if report is None or report.empty:
        return

    plt.figure(figsize=(9, 5))

    plt.plot(
        report["month"],
        report["sales"],
        marker="o"
    )

    plt.xlabel("Month")
    plt.ylabel("Total sales")
    plt.title("Monthly Sales Trend")

    plt.tight_layout()

    plt.savefig(os.path.join(CHART_DIR, "monthly_sales_trend.png"))
    plt.show()


# ==========================================
# 13. TESTING
# ==========================================

def run_tests(inventory):

    print("\nRUNNING TEST CASES")
    print("-" * 50)

    item = find_item(inventory, "I001")

    if item is None:
        print("Test item unavailable.")
        return

    original_stock = item.stock

    # Test 1: Negative stock-in
    print("Test 1:", add_stock(item, -5))

    # Test 2: Zero stock-out
    print("Test 2:", remove_stock(item, 0))

    # Test 3: Excessive stock-out
    print("Test 3:", remove_stock(item, item.stock + 100))

    # Test 4: Valid stock-in
    print("Test 4:", add_stock(item, 5))

    # Test 5: Valid stock-out
    print("Test 5:", remove_stock(item, 2))

    # Restore original values
    item.stock = original_stock
    save_inventory(inventory)

    print("Test completed. Original stock restored.")


# ==========================================
# 14. MENU-DRIVEN MAIN PROGRAM
# ==========================================

def main():

    inventory = load_inventory(INVENTORY_FILE)

    if not inventory:
        print("No valid inventory loaded. Check inventory.csv.")
        return

    while True:

        print("\n")
        print("=" * 48)
        print("       INVENTORY & REORDER TRACKER")
        print("=" * 48)

        print("1. View inventory")
        print("2. Add stock")
        print("3. Remove stock / Record sale")
        print("4. Show reorder alerts")
        print("5. NumPy statistical analysis")
        print("6. Pandas category report")
        print("7. Monthly sales report")
        print("8. Export JSON report")
        print("9. Compare reorder thresholds")
        print("10. Display stock chart")
        print("11. Display sales chart")
        print("12. Display category chart")
        print("13. Display monthly trend")
        print("14. Run test cases")
        print("0. Exit")

        print("=" * 48)

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            display_inventory(inventory)

        elif choice == "2":
            stock_operations(inventory, "in")

        elif choice == "3":
            stock_operations(inventory, "out")

        elif choice == "4":
            show_reorder_items(inventory)

        elif choice == "5":
            numpy_analysis(inventory)

        elif choice == "6":
            df = inventory_to_dataframe(inventory)
            print("\nCATEGORY REPORT")
            print(category_report(df).to_string(index=False))

        elif choice == "7":
            monthly_report()

        elif choice == "8":
            df = inventory_to_dataframe(inventory)
            export_json(df)

        elif choice == "9":
            df = inventory_to_dataframe(inventory)
            compare_reorder_thresholds(df)

        elif choice == "10":
            plot_stock_levels(inventory_to_dataframe(inventory))

        elif choice == "11":
            plot_sales(inventory_to_dataframe(inventory))

        elif choice == "12":
            plot_category_sales(inventory_to_dataframe(inventory))

        elif choice == "13":
            plot_monthly_sales()

        elif choice == "14":
            run_tests(inventory)

        elif choice == "0":
            print("Thank you for using Inventory Tracker!")
            break

        else:
            print("Invalid choice! Please try again.")


# ==========================================
# 15. PROGRAM EXECUTION
# ==========================================

if __name__ == "__main__":
    main()