import matplotlib.pyplot as plt


def plot_run_rate(df, save_path=None):
    
    # Aggregate runs per over
    run_rate = df.groupby("over")["runs"].sum().cumsum()

    plt.figure()
    plt.plot(run_rate.index, run_rate.values)

    plt.xlabel("Overs")
    plt.ylabel("Cumulative Runs")
    plt.title("Run Progression")

    # ✅ SAVE if path provided
    if save_path:
        plt.savefig(save_path)
        print(f"📁 Chart saved at: {save_path}")
    else:
        plt.show()

    plt.close()