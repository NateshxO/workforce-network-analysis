# Imports
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

NODES_FILE = "Nodes.csv"
SKILLS_FILE = "Skills.txt"
TOP_N_BRIDGES = 15
TOP_N_SKILLS = 10

# Below code has been modified from https://matplotlib.org/stable/gallery/images_contours_and_fields/image_annotated_heatmap.html
# to create heatmaps

def plot_bridge_skill_heatmap():
    # Load the files
    try:
        nodes_df = pd.read_csv(NODES_FILE)
        skills_df = pd.read_csv(SKILLS_FILE, delimiter="\t",
                                usecols=["O*NET-SOC Code", "Element ID", "Element Name", "Scale ID", "Data Value"])
    except FileNotFoundError as e:
        print(f"Error: {e}")
        return

    # Keep only importance scores
    skills_im = skills_df[skills_df["Scale ID"] == "IM"]

    # Handle two possible spellings of the column name
    bc_col = 'betweenesscentrality' if 'betweenesscentrality' in nodes_df.columns else 'betweennesscentrality'

    # Get the top N jobs by betweenness centrality and add a rank number to each name
    top_bridges = nodes_df.sort_values(by=bc_col, ascending=False).head(TOP_N_BRIDGES)
    top_bridges['Ranked_Label'] = [f"{i+1}. {label}" for i, label in enumerate(top_bridges['Label'])]

    # Attach skill data to the top jobs
    bridge_skills = pd.merge(top_bridges[['Id', 'Ranked_Label', bc_col]], skills_im, left_on='Id', right_on='O*NET-SOC Code')

    # Find the top N skills by average importance across all top jobs
    skill_means = bridge_skills.groupby('Element Name')['Data Value'].mean().reset_index()
    top_transition_skills = skill_means.sort_values(by='Data Value', ascending=False).head(TOP_N_SKILLS)['Element Name'].tolist()

    # Keep only the top skills, then reshape into a jobs x skills table
    heatmap_data = bridge_skills[bridge_skills['Element Name'].isin(top_transition_skills)]
    pivot_df = heatmap_data.pivot(index='Ranked_Label', columns='Element Name', values='Data Value')

    # Preserve rank order so rank 1 is at the top
    # pivot(): https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.pivot.html
    pivot_df = pivot_df.loc[top_bridges['Ranked_Label']]

    # Draw and save the heatmap (# plt.figure, title, labels, ticks adapted from ClassW7L7.ipynb (class notes))
    plt.figure(figsize=(14, 10))
    ax = sns.heatmap(
        pivot_df,
        annot=True,
        fmt=".1f",
        linewidths=1.0,
        linecolor='white',
        cbar_kws={'label': 'Skill Importance (1-5)'}
    )

    plt.title(f"The Anatomy of a Stepping Stone:\nTop {TOP_N_BRIDGES} Ranked Bridge Occupations vs. Required Skill Vectors",
              fontsize=16, pad=20, weight='bold')
    plt.ylabel("Occupations (Ranked by Betweenness Centrality)", fontsize=12, weight='bold')
    plt.xlabel("Highly Transitionable 'Universal' Skills", fontsize=12, weight='bold')
    plt.xticks(rotation=45, ha='right', fontsize=10)
    plt.yticks(rotation=0, fontsize=10)

    plt.tight_layout()
    plt.savefig("Ranked_Bridge_Heatmap_Professional.png", dpi=300)
    print("Done. Chart saved.")

# Run Algorithm
if __name__ == "__main__":
    plot_bridge_skill_heatmap()