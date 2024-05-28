import pandas as pd
import matplotlib.pyplot as plt
import os

def plot_histogram_from_csv(csv_file):
    data = pd.read_csv(csv_file)
    data = data[data['changes'] > 0]  # Filter out zero changes
    sorted_data = data.sort_values(by='changes', ascending=False)

    plt.figure(figsize=(10, 6))
    plt.bar(sorted_data['account'], sorted_data['changes'], color='blue')
    plt.xlabel('Account')
    plt.ylabel('Number of Changes')
    plt.title('Storage Changes per Account for ' + os.path.basename(csv_file))
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.savefig(csv_file.replace('.csv', '.png'))  # Save the plot as a PNG file
    plt.close()

# Path to the assets directory
assets_dir = 'assets/'

# List all CSV files in the assets directory
csv_files = [os.path.join(assets_dir, f) for f in os.listdir(assets_dir) if f.endswith('.csv')]
for file in csv_files:
    plot_histogram_from_csv(file)
