import os
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

def load_sales_data(output_dir, start_date, end_date):

    all_sales_data = []
    
    for filename in os.listdir(output_dir):
        file_path = os.path.join(output_dir, filename)
        
        if not os.path.isfile(file_path):
            continue
        
        with open(file_path, 'r') as f:
            for line in f:
                try:
                    date_time, product, sales = line.strip().split('|')
                    
                    log_datetime = datetime.strptime(date_time.strip(), '%Y/%m/%d %H')
                    
                    if start_date <= log_datetime <= end_date:
                        all_sales_data.append({
                            'date': log_datetime.date(), 
                            'product': product.strip(),
                            'sales': float(sales.strip())
                        })
                except (ValueError, IndexError):
                    continue
    
    df = pd.DataFrame(all_sales_data)
    return df

def generate_sales_dashboard(output_dir, start_date, end_date):
   
    start = datetime.strptime(start_date, '%Y-%m-%d')
    end = datetime.strptime(end_date, '%Y-%m-%d')
    
    df = load_sales_data(output_dir, start, end)
    
    if df.empty:
        print("No sales data found in the specified date range.")
        return
    
    plt.figure(figsize=(15, 10))
    plt.suptitle(f'Sales Dashboard Aharoud Ismail ({start_date} to {end_date})', fontsize=16)
    
    plt.subplot(2, 2, 1)
    product_sales = df.groupby('product')['sales'].sum().sort_values(ascending=False)
    product_sales.plot(kind='bar')
    plt.title('Total Sales by Product')
    plt.xlabel('Product')
    plt.ylabel('Total Sales')
    plt.xticks(rotation=45, ha='right')
    
    plt.subplot(2, 2, 2)
    daily_sales = df.groupby('date')['sales'].sum()
    daily_sales.plot(kind='line', marker='o')
    plt.title('Daily Total Sales')
    plt.xlabel('Date')
    plt.ylabel('Total Sales')
    plt.xticks(rotation=45, ha='right')
    
    plt.subplot(2, 2, 3)
    product_sales.plot(kind='pie', autopct='%1.1f%%')
    plt.title('Sales Distribution by Product')
    
    plt.subplot(2, 2, 4)
    summary_stats = pd.DataFrame({
        'Metric': [
            'Total Sales', 
            'Average Daily Sales', 
            'Top Product', 
            'Top Product Sales'
        ],
        'Value': [
            f"${df['sales'].sum():,.2f}", 
            f"${df.groupby('date')['sales'].sum().mean():,.2f}", 
            product_sales.index[0], 
            f"${product_sales.iloc[0]:,.2f}"
        ]
    })
    plt.axis('off')
    table = plt.table(cellText=summary_stats.values, 
                      colLabels=summary_stats.columns, 
                      loc='center', 
                      cellLoc='center')
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1.2, 1.5)
    
    plt.tight_layout()
    output_filename = f'sales_dashboard_{start_date}_to_{end_date}.png'
    plt.savefig(output_filename, dpi=300, bbox_inches='tight')
    print(f"Dashboard saved as {output_filename}")
    
    print("\nSales Summary:")
    print(f"Total Sales: ${df['sales'].sum():,.2f}")
    print(f"Number of Products: {df['product'].nunique()}")
    print("\nTop 5 Products by Sales:")
    print(product_sales.head())

if __name__ == "__main__":
    output_directory = "/home/ismail/folder/projects/big-data/backend/output"
    
    start_date = "2024-11-18"
    end_date = "2024-11-25"
    
    generate_sales_dashboard(output_directory, start_date, end_date)
