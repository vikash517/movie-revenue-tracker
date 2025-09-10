import pandas as pd
import matplotlib.pyplot as plt

# Load movie revenue data
# Replace 'movie_revenue.csv' with your actual file name
DATA_FILE = 'movie_revenue.csv'

def load_data(file_path):
    return pd.read_csv(file_path)

def group_data(df):
    return df.groupby(['Movie', 'Region', 'ReleaseWeek']).agg({'Revenue': 'sum'}).reset_index()

def plot_revenue(grouped):
    plt.figure(figsize=(10,6))
    for movie in grouped['Movie'].unique():
        movie_data = grouped[grouped['Movie'] == movie]
        for region in movie_data['Region'].unique():
            region_data = movie_data[movie_data['Region'] == region]
            plt.plot(region_data['ReleaseWeek'], region_data['Revenue'], label=f"{movie} - {region}")
    plt.xlabel('Release Week')
    plt.ylabel('Revenue')
    plt.title('Box Office Collections by Movie & Region')
    plt.legend()
    plt.tight_layout()
    plt.show()

def plot_by_genre(df, genre):
    filtered = df[df['Genre'] == genre]
    grouped = group_data(filtered)
    plt.figure(figsize=(10,6))
    for movie in grouped['Movie'].unique():
        movie_data = grouped[grouped['Movie'] == movie]
        for region in movie_data['Region'].unique():
            region_data = movie_data[movie_data['Region'] == region]
            plt.plot(region_data['ReleaseWeek'], region_data['Revenue'], label=f"{movie} - {region}")
    plt.xlabel('Release Week')
    plt.ylabel('Revenue')
    plt.title(f'Box Office Collections by Movie & Region (Genre: {genre})')
    plt.legend()
    plt.tight_layout()
    plt.show()

def main():
    df = load_data(DATA_FILE)
    grouped = group_data(df)
    plot_revenue(grouped)
    # Example: plot_by_genre(df, 'Action')

if __name__ == "__main__":
    main()
