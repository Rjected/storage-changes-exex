import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import os

def plot_3d_histogram_from_csvs(csv_files):
    fig = plt.figure(figsize=(14, 10))
    ax = fig.add_subplot(111, projection='3d')

    xpos = []
    ypos = []
    zpos = []
    dx = []
    dy = []
    dz = []

    account_totals = {}
    block_numbers = []

    # First, accumulate changes for each account across all blocks to sort them
    for csv_file in csv_files:
        block_number = int(os.path.basename(csv_file).split('_')[1])  # Extract block number from filename
        block_numbers.append(block_number)
        data = pd.read_csv(csv_file)
        data = data[data['changes'] > 0]  # Filter out zero changes
        for row in data.itertuples(index=False):
            account = row.account
            if account not in account_totals:
                account_totals[account] = 0
            account_totals[account] += row.changes

    # Sort accounts by total changes
    sorted_accounts = sorted(account_totals, key=account_totals.get, reverse=True)
    account_mapping = {account: i for i, account in enumerate(sorted_accounts)}

    # Now plot data with sorted accounts
    for idx, csv_file in enumerate(csv_files):
        data = pd.read_csv(csv_file)
        data = data[data['changes'] > 0]  # Filter out zero changes
        for row in data.itertuples(index=False):
            account = row.account
            xpos_val = account_mapping[account]

            xpos.append(xpos_val)
            ypos.append(idx)
            zpos.append(0)
            dx.append(1)  # Width along account axis
            dy.append(1)  # Depth along block axis
            dz.append(row.changes)

    ax.bar3d(xpos, ypos, zpos, dx, dy, dz, color='b', zsort='average')
    ax.set_xlabel('Account Index')
    ax.set_ylabel('Block Index')
    ax.set_zlabel('Number of Changes')
    ax.set_xticklabels([])  # Remove X-axis labels

    ax.set_yticks(list(range(len(csv_files))))
    ax.set_yticklabels(block_numbers)

    plt.title('3D Histogram of Storage Changes Across Multiple Blocks')
    plt.tight_layout()
    plt.savefig('assets/storage_changes_3d.png')
    plt.close()

# Path to the assets directory
assets_dir = 'assets/'

# List all CSV files in the assets directory
csv_files = [os.path.join(assets_dir, f) for f in os.listdir(assets_dir) if f.endswith('.csv')]
csv_files.sort(key=lambda x: int(os.path.basename(x).split('_')[1]))  # Sorting by block number
plot_3d_histogram_from_csvs(csv_files)
