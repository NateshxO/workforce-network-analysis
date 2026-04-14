import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

NODES_FILE = "../LargeScopeQ2/Nodes.csv"
SKILLS_FILE = "Skills.txt"
TOP_N_BRIDGES = 40

# Below code is used to create bar chart of the 15 most shared skills among stepping stone occupations

def plot_transitionable_skills():
    # Load job nodes and skills data
    nodes_df = pd.read_csv(NODES_FILE)
    skills_df = pd.read_csv(SKILLS_FILE, delimiter="\t",
                            usecols=["O*NET-SOC Code", "Element ID", "Element Name", "Scale ID", "Data Value"])

    # Keep only importance scores
    skills_im = skills_df[skills_df["Scale ID"] == "IM"]

    # Handle two possible spellings of the column name
    bc_col = 'betweenesscentrality' if 'betweenesscentrality' in nodes_df.columns else 'betweennesscentrality'

    # Get the top N jobs by betweenness centrality
    top_bridges = nodes_df.sort_values(by=bc_col, ascending=False).head(TOP_N_BRIDGES)

    # Attach skill data to the top jobs
    bridge_skills = pd.merge(top_bridges[['Id', 'Label', bc_col]], skills_im,
                             left_on='Id', right_on='O*NET-SOC Code')

    # Average each skill across all top jobs, then take the top 15
    skill_means = bridge_skills.groupby('Element Name')['Data Value'].mean().reset_index()
    top_transition_skills = skill_means.sort_values(by='Data Value', ascending=False).head(15)

    plt.figure(figsize=(12, 8))
    ax = sns.barplot(x='Data Value', y='Element Name', data=top_transition_skills,
                     palette="viridis", edgecolor='black')

    plt.title("The 'Universal Translator' Profile:\nTop 15 Shared Skills Among High-Mobility Stepping Stone Jobs",
              fontsize=16, pad=20, weight='bold')
    plt.xlabel("Average Skill Importance (1 - 5 Scale)", fontsize=12)
    plt.ylabel("")

    # Add score labels to the end of each bar
    for p in ax.patches:
        plt.text(p.get_width() + 0.05, p.get_y() + p.get_height() / 2. + 0.1,
                 f'{p.get_width():.2f}', ha="left", fontsize=10)

    sns.despine(left=True, bottom=True)
    plt.xlim(0, 5.0)
    plt.tight_layout()
    plt.savefig("Highly_Transitionable_Skills.png", dpi=300)
    plt.close()

if __name__ == "__main__":
    plot_transitionable_skills()