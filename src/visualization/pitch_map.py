import matplotlib.pyplot as plt
import seaborn as sns


def plot_pitch_heatmap(zone_stats, save_path=None):

    heat_data = zone_stats.pivot_table(
        values="economy",
        index="zone"
    )

    plt.figure(figsize=(4, 6))
    sns.heatmap(heat_data, annot=True, cmap="coolwarm")

    plt.title("Pitch Zone Economy (Simulated)")
    plt.xlabel("")
    plt.ylabel("")

    if save_path:
        plt.savefig(save_path)
        print(f"📁 Heatmap saved at: {save_path}")
    else:
        plt.show()

    plt.close()