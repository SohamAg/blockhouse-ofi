#Plot file
import matplotlib.pyplot as plt

def plot_feature(df, feature="integrated_ofi"):
    if feature not in df.columns:
        print(f"{feature}' was not found")
        return
    
    #Plotting logic to plot the OFI over time
    plt.figure(figsize=(12, 5))
    plt.plot(df['ts_event'], df[feature], label=feature, color='teal')
    plt.xlabel("Timestamp")
    plt.ylabel("OFI Value")
    plt.title(f"{feature} Over Time")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()
