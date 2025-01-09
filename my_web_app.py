from flask import Flask, request, render_template
import pandas as pd

def find_and_sort_orders(df, min_value, max_value, sort_type=True):
    """
    Find and sort unique orders within a specified range of total values.

    Parameters:
        df (DataFrame): The input DataFrame containing sales transaction data.
        min_value (float): The minimum value of the order total range.
        max_value (float): The maximum value of the order total range.
        sort_type (bool): Sorting order, True for ascending, False for descending.

    Returns:
        DataFrame: A DataFrame containing OrderID and their total value, sorted based on `sort_type`.
    """
    # Calculate total value for each order
    order_totals = df.groupby('OrderID').apply(
        lambda x: (x['UnitPrice'] * x['Quantity'] * (1 - x['Discount'])).sum()
    ).reset_index(name='Sum')  # Rename the aggregated column to 'Sum'

    # Filter orders within the specified range
    filtered_orders = order_totals[
        (order_totals['Sum'] >= min_value) & (order_totals['Sum'] <= max_value)
    ]

    # Sort the orders based on the `sort_type`
    sorted_orders = filtered_orders.sort_values(by='Sum', ascending=sort_type)

    return sorted_orders

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def main():
    if request.method == "POST":
        # Lấy giá trị từ form
        min_value = float(request.form["min_value"])
        max_value = float(request.form["max_value"])
        sort_type = request.form["sort_type"]  # Lấy giá trị 'asc' hoặc 'desc'

        # Chuyển giá trị 'asc' hoặc 'desc' thành True hoặc False
        sort_type_bool = True if sort_type == "asc" else False

        # Đọc file dataset
        df = pd.read_csv('dataset/SalesTransactions.csv')

        # Gọi hàm để lọc và sắp xếp dữ liệu
        result = find_and_sort_orders(df, min_value, max_value, sort_type_bool)

        # Hiển thị kết quả trong HTML
        return render_template("orders_sort.html", tables=[result.to_html(classes='data')], titles=result.columns.values)

    # Nếu là GET, chỉ hiển thị form mà không có kết quả
    return render_template("orders_sort.html")

if __name__ == "__main__":
    app.run(host="localhost", port=9000, debug=True)
