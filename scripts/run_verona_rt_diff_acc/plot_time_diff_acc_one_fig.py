import pandas as pd
import matplotlib.pyplot as plt
import sys
import os
import glob

if len(sys.argv) != 2:
    print("Usage: python plot_time_diff_acc_one_fig.py <datetime_path>")
    sys.exit(1)

datetime_path = sys.argv[1]
base_dir = f'/users/Xuran/verona-rt/log/{datetime_path}'

accs = glob.glob(os.path.join(base_dir, 'acc_*'))

plt.figure(figsize=(12, 6))

colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k']

plot_data = []

for i, acc in enumerate(accs):
    csv_path = os.path.join(acc, 'run_time_diff_cores.csv')
    if not os.path.exists(csv_path):
        print(f"Warning: File not found: {csv_path}")
        continue

    df = pd.read_csv(csv_path)
    acc_val = float(os.path.basename(acc).split('_')[-1])
    plot_data.append((acc_val, df))

plot_data.sort(key=lambda x: x[0], reverse=True)


for i, (acc_val, df) in enumerate(plot_data):
    color = colors[i % len(colors)]
    plt.plot(df['cores'], df['time'], marker='o', linewidth=2, 
             markersize=6, label=f'acc: {acc_val}', color=color)

plt.title('Runtime vs Hardware threads for Different Account Numbers', fontsize=14)
# plt.title('Scheduler time vs Hardware threads for Different Account Numbers', fontsize=14)
# plt.title('Init scheduler time vs Hardware threads for Different Account Numbers', fontsize=14)
plt.xlabel('Hardware threads', fontsize=12)
plt.ylabel('Time Taken (ms)', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend()
plt.tight_layout()

output_path = os.path.join(base_dir, 'run_time_diff_cores_combined.png')
plt.savefig(output_path, dpi=300, bbox_inches='tight')
plt.close()