import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from math import pi

NODES_FILE = "../LargeScopeQ2/Nodes.csv"
SKILLS_FILE = "Skills.txt"

# Below code is used to create the macro level heatmaps of the top 15 stepping stone occupations'
# skill vectors. Code is also used to create the macro radar charts for top 8 largest communities. 

# The code for heatmaps has been modified from https://matplotlib.org/stable/gallery/images_contours_and_fields/image_annotated_heatmap.html

# The code for radar charts has been modified from https://matplotlib.org/stable/gallery/specialty_plots/radar_chart.html 

def load_and_prep_data():
    # Load job nodes and skills data
    nodes_df = pd.read_csv(NODES_FILE)
    skills_df = pd.read_csv(SKILLS_FILE, delimiter="\t",
                            usecols=["O*NET-SOC Code", "Element ID", "Element Name", "Scale ID", "Data Value"])

    # Keep only importance scores
    skills_im = skills_df[skills_df["Scale ID"] == "IM"]

    # Drop jobs with no cluster assigned, then attach skills
    clusters_df = nodes_df[['Id', 'modularity_class']].dropna()
    merged_df = pd.merge(clusters_df, skills_im, left_on='Id', right_on='O*NET-SOC Code')

    # Average each skill per cluster
    cluster_skill_means = merged_df.groupby(
        ['modularity_class', 'Element Name'])['Data Value'].mean().reset_index()

    return cluster_skill_means

def plot_macro_heatmap(cluster_skill_means):
    # Reshape into a clusters x skills table
    heatmap_data = cluster_skill_means.pivot(
        index='modularity_class', columns='Element Name', values='Data Value').sort_index()

    plt.figure(figsize=(16, 10))
    sns.heatmap(heatmap_data, cmap="YlGnBu", cbar_kws={'label': 'Skill Importance (1-5)'})

    plt.title("Macro View: Skill Vector Signatures Across Career Communities", fontsize=16, pad=20)
    plt.ylabel("Community (LargeScopeQ2 Class)", fontsize=12)
    plt.xlabel("O*NET Skills", fontsize=12)
    plt.xticks(rotation=45, ha='right', fontsize=9)
    plt.yticks(rotation=0)
    plt.tight_layout()
    plt.savefig("Macro_Cluster_Heatmap.png", dpi=300)
    plt.close()

def prepare_domain_data(cluster_skill_means):
    # Map cluster numbers to industry names
    domain_mapping = {
        14: "Education",
        0:  "Community Service",
        6:  "Healthcare",
        2:  "Business",
        5:  "Clerks",
        12: "Protective Service",
        8:  "Arch & Engineering",
        15: "Labour Work",
        18: "Labour Work"
    }

    subset = cluster_skill_means[cluster_skill_means['modularity_class'].isin(domain_mapping.keys())].copy()
    subset['Domain'] = subset['modularity_class'].map(domain_mapping)

    # Average skills by domain and reshape into a domain x skill table
    domain_means = subset.groupby(['Domain', 'Element Name'])['Data Value'].mean().reset_index()
    return domain_means.pivot(index='Domain', columns='Element Name', values='Data Value').fillna(0)

def get_distinct_skills(radar_data):
    # Pick the 2 skills each domain scores highest relative to all others
    domains = radar_data.index.tolist()
    distinct_skills = []
    for domain in domains:
        other_mean = radar_data.loc[[d for d in domains if d != domain]].mean()
        top_2 = (radar_data.loc[domain] - other_mean).sort_values(ascending=False).head(2).index.tolist()
        distinct_skills.extend(top_2)
    return list(dict.fromkeys(distinct_skills))


# Code used to generate small radar charts
def plot_small_multiples_radar(cluster_skill_means):
    radar_data = prepare_domain_data(cluster_skill_means)
    domains = radar_data.index.tolist()
    skills = get_distinct_skills(radar_data)

    angles = [n / float(len(skills)) * 2 * pi for n in range(len(skills))]
    angles += angles[:1]

    colors = ['#17becf', '#9467bd', '#1f77b4', '#ff7f0e', '#000000', '#2ca02c', '#d62728', '#e377c2']

    # subplot_kw passes polar=True to every subplot: https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.subplots.html
    fig, axes = plt.subplots(2, 4, figsize=(22, 11), subplot_kw=dict(polar=True))

    for idx, domain in enumerate(domains):
        ax = axes.flatten()[idx]

        # Rotate chart so first axis starts at the top, going clockwise
        ax.set_theta_offset(pi / 2)
        ax.set_theta_direction(-1)

        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(skills, color='black', size=8)
        ax.set_yticks([1, 2, 3, 4, 5])
        ax.set_yticklabels(["1","2","3","4","5"], color="grey", size=7)
        ax.set_ylim(0, 5.2)

        values = radar_data.loc[domain, skills].values.flatten().tolist()
        values += values[:1]  # Close the polygon by repeating the first value

        ax.plot(angles, values, linewidth=2, color=colors[idx])
        ax.fill(angles, values, color=colors[idx], alpha=0.4)
        ax.set_title(domain, size=15, color=colors[idx], weight='bold', pad=25)

    plt.suptitle("Micro View: The Distinctive Skill Vectors of 8 Major Industries", size=22, weight='bold', y=1.05)
    plt.tight_layout()
    plt.savefig("Small_Multiples_Radar_8.png", dpi=300, bbox_inches='tight')
    plt.close()

# Code used to generate an unified radar chart
def plot_master_combined_radar(cluster_skill_means):
    radar_data = prepare_domain_data(cluster_skill_means)
    domains = radar_data.index.tolist()
    skills = get_distinct_skills(radar_data)

    angles = [n / float(len(skills)) * 2 * pi for n in range(len(skills))]
    angles += angles[:1]

    colors = ['#17becf', '#9467bd', '#1f77b4', '#ff7f0e', '#000000', '#2ca02c', '#d62728', '#e377c2']

    # plt.subplot(111, polar=True): https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.subplot.html
    plt.figure(figsize=(15, 15))
    ax = plt.subplot(111, polar=True)
    ax.set_theta_offset(pi / 2)
    ax.set_theta_direction(-1)
    plt.xticks(angles[:-1], skills, color='black', size=10)
    plt.yticks([1, 2, 3, 4, 5], ["1","2","3","4","5"], color="grey", size=8)
    plt.ylim(0, 5.2)

    for idx, domain in enumerate(domains):
        values = radar_data.loc[domain, skills].values.flatten().tolist()
        values += values[:1]  # Close the polygon by repeating the first value

        ax.plot(angles, values, linewidth=2.5, label=domain, color=colors[idx])
        ax.fill(angles, values, color=colors[idx], alpha=0.02)  # Low alpha avoids overlapping fills

    plt.title("Master Map: Intersecting Skill Boundaries of 8 Major Industries", size=20, pad=40, weight='bold')
    plt.legend(loc='upper right', bbox_to_anchor=(1.25, 1.1), fontsize=12)
    plt.tight_layout()
    plt.savefig("Master_Combined_Radar_8.png", dpi=300, bbox_inches='tight')
    plt.close()

# Run main program
if __name__ == "__main__":
    df = load_and_prep_data()
    plot_macro_heatmap(df)
    plot_small_multiples_radar(df)
    plot_master_combined_radar(df)