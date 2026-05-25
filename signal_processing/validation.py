import pandas as pd
import numpy as np

data = {
    'Trial': [1, 2, 3, 4, 5],
    'Manual_Count_10s': [16, 15, 15, 15, 16],
    'Algorithm_Total_28s': [40, 43, 42, 40, 45],
    'Algorithm_10s_est': [
        round(40*(10/28), 1),
        round(43*(10/28), 1),
        round(42*(10/28), 1),
        round(40*(10/28), 1),
        round(45*(10/28), 1)
    ]
}

df = pd.DataFrame(data)
df['Accuracy_%'] = round(
    (1 - abs(df['Manual_Count_10s'] - df['Algorithm_10s_est']) / 
     df['Manual_Count_10s']) * 100, 1)
df['Error_%'] = round(100 - df['Accuracy_%'], 1)

print("Peak Detection Accuracy Validation")
print("=" * 55)
print(df.to_string(index=False))
print("=" * 55)
print(f"Mean Accuracy: {df['Accuracy_%'].mean():.1f}%")
print(f"Mean Error:    {df['Error_%'].mean():.1f}%")
print(f"Best Trial:    Trial {df.loc[df['Accuracy_%'].idxmax(), 'Trial']} ({df['Accuracy_%'].max()}%)")
print(f"Worst Trial:   Trial {df.loc[df['Accuracy_%'].idxmin(), 'Trial']} ({df['Accuracy_%'].min()}%)")

df.to_csv('../results/experiment_1/peak_accuracy_validation.csv', index=False)
print("\nSaved to results/experiment_1/peak_accuracy_validation.csv")