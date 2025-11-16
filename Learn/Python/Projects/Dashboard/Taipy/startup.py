import data_load as data
import logging

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[logging.StreamHandler(),  # Output to console
                              logging.FileHandler('../app.log')]) # Output to a file

# Generate 100,000 rows of data with random order_date and save to CSV
csv_data=data.generate(100_000, r"C:\temp\sales_data.csv")