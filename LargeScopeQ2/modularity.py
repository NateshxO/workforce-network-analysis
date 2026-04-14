import pandas as pd

NODES_FILE = "Nodes.csv"
SKILLS_FILE = "Skills.txt"
IMPORTANCE_THRESHOLD = 3.0

# Below code is used to list out the importance skill vectors for each community exported from Gephi  

def analyze_cluster_skills():
    # Load job nodes and skills data
    nodes_df = pd.read_csv(NODES_FILE)
    skills_df = pd.read_csv(SKILLS_FILE, delimiter="\t",
                            usecols=["O*NET-SOC Code", "Element ID", "Element Name", "Scale ID", "Data Value"])

    # Keep only importance scores
    skills_im = skills_df[skills_df["Scale ID"] == "IM"]

    # Drop jobs with no cluster assigned, then attach skills to each job
    clusters_df = nodes_df[['Id', 'modularity_class']].dropna()
    merged_df = pd.merge(clusters_df, skills_im, left_on='Id', right_on='O*NET-SOC Code')

    # Average each skill per cluster
    cluster_skill_means = merged_df.groupby(
        ['modularity_class', 'Element ID', 'Element Name'])['Data Value'].mean().reset_index()

    # Sort clusters so they print in order
    clusters = sorted(cluster_skill_means['modularity_class'].unique())

    for cluster in clusters:
        # Filter down to just this cluster's skills
        cluster_data = cluster_skill_means[cluster_skill_means['modularity_class'] == cluster]

        # Sort skills from highest to lowest importance
        top_skills = cluster_data.sort_values(by='Data Value', ascending=False)

        # Count how many skills are above the threshold
        core_skills_count = (top_skills['Data Value'] > IMPORTANCE_THRESHOLD).sum()

        print(f"=== CLUSTER {int(cluster)} ===")
        print(f"Core Skills (Avg Importance > {IMPORTANCE_THRESHOLD}): {core_skills_count}")
        print("All 35 Skill Averages:")
        for _, row in top_skills.iterrows():
            print(f"  {row['Element Name']} ({row['Element ID']}): {row['Data Value']:.2f}")
        print("-" * 50)

if __name__ == "__main__":
    analyze_cluster_skills()