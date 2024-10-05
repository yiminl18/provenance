import matplotlib.pyplot as plt

# Data for the plots
data = [
    {
        "baseline_name": "baseline3_reverse",
        "model_name": "gpt4o",
        "dataset_name": "civic",
        "cost": 2.45169,
        "compression_rate": 0.6714136334213016,
        "average_sentence_number": 6.566666666666666,
    },
    {
        "baseline_name": "baseline3_reverse",
        "model_name": "gpt4o",
        "dataset_name": "paper",
        "cost": 2.4607400000000004,
        "compression_rate": 0.545026451950468,
        "average_sentence_number": 3.7333333333333334,
    },
    {
        "baseline_name": "baseline3_reverse",
        "model_name": "gpt4o",
        "dataset_name": "notice",
        "cost": 1.8237400000000001,
        "compression_rate": 0.21334761287413337,
        "average_sentence_number": 1.1666666666666667,
    },
    {
        "baseline_name": "baseline2_greedy",
        "model_name": "gpt4o",
        "dataset_name": "civic",
        "cost": 4.2699050000000005,
        "compression_rate": 0.6714634267788677,
        "average_sentence_number": 16.033333333333335,
    },
    {
        "baseline_name": "baseline2_greedy",
        "model_name": "gpt4o",
        "dataset_name": "paper",
        "cost": 4.884745000000001,
        "compression_rate": 0.4903203302133597,
        "average_sentence_number": 15.666666666666666,
    },
    {
        "baseline_name": "baseline2_greedy",
        "model_name": "gpt4o",
        "dataset_name": "notice",
        "cost": 1.8942550000000002,
        "compression_rate": 0.17372188715404993,
        "average_sentence_number": 2.8666666666666667,
    }
]

# Define unique colors and markers for each baseline
baselines = list(set(d['baseline_name'] for d in data))
colors = ['blue', 'orange']
markers = ['o', 's']
baseline_styles = dict(zip(baselines, zip(colors, markers)))

# Plotting
plt.figure(figsize=(10, 6))

for entry in data:
    baseline = entry['baseline_name']
    dataset = entry['dataset_name']
    cost = entry['cost']
    compression_rate = entry['compression_rate']
    average_sentence_number = entry['average_sentence_number']
    
    # Calculate remaining index count
    remaining_index = average_sentence_number
    
    color, marker = baseline_styles[baseline]
    
    plt.scatter(cost, compression_rate, color=color, marker=marker, label=f"{baseline}", s=80, edgecolors='black')
    
    # Annotate the points with dataset name and coordinates
    plt.text(cost-0.02, compression_rate-0.02, f"({cost:.2f}, {compression_rate:.2f}) {dataset}, {average_sentence_number:.2f}", fontsize=8, ha='right')

# Set plot titles and labels
plt.title("Compression Rate vs Cost by Dataset and Baseline")
plt.xlabel("Cost")
plt.ylabel("Compression Rate")

# Set legend
plt.legend(loc='lower right', fontsize=8, title='Baseline (Dataset)', title_fontsize='10')

# Show plot
plt.grid(True, linestyle='--', alpha=0.5)
plt.tight_layout()
plt.savefig('test/output/provenance/cost_compression.png')