import csv
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
input_dir = os.path.join(SCRIPT_DIR, 'data')
output_file = os.path.join(SCRIPT_DIR, 'formatted_output.csv')

def process_data():
    with open(output_file, 'w', newline='') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(['sales', 'date', 'region'])
        
        for filename in sorted(os.listdir(input_dir)):
            if filename.endswith('.csv') and filename.startswith('daily_sales_data'):
                filepath = os.path.join(input_dir, filename)
                with open(filepath, 'r') as infile:
                    reader = csv.DictReader(infile)
                    for row in reader:
                        if row['product'] == 'pink morsel':
                            price_str = row['price'].replace('$', '')
                            price = float(price_str)
                            quantity = int(row['quantity'])
                            sales = price * quantity
                            
                            writer.writerow([f"{sales:.2f}", row['date'], row['region']])
                print(f"Processed {filename}")
                
if __name__ == '__main__':
    process_data()
    print("All done!")
