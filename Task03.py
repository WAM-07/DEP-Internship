import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def load_data():
    """
    Load the Iris dataset using seaborn's built-in dataset.

    Returns:
        pandas.DataFrame: The Iris dataset.
    """
    iris = sns.load_dataset('iris')
    return iris


def explore_data(df):
    """
    Perform basic exploration of the dataset.

    Args:
        df (pandas.DataFrame): The dataset to explore.
    """
    # Display the first few rows of the dataset
    print("First 5 rows of the dataset:")
    print(df.head())

    # Display summary statistics
    print("\nSummary statistics:")
    print(df.describe())

    # Display data types and check for missing values
    print("\nData types and missing values:")
    print(df.info())


def visualize_data(df):
    """
    Visualize the dataset using various plots.

    Args:
        df (pandas.DataFrame): The dataset to visualize.
    """
    # Set the seaborn style
    sns.set(style="whitegrid")

    # Pairplot to visualize relationships between variables
    print("\nCreating pairplot...")
    pairplot = sns.pairplot(df, hue='species', markers=["o", "s", "D"])
    pairplot.fig.suptitle('Pairplot of Iris Dataset', y=1.02)
    plt.show()

    # Boxplot to show the distribution of features
    print("\nCreating boxplot...")
    plt.figure(figsize=(12, 8))
    sns.boxplot(data=df)
    plt.title('Boxplot of Iris Dataset Features')
    plt.show()

    # Violin plots to show distribution of features by species
    print("\nCreating violin plots...")
    for feature in df.columns[:-1]:  # Exclude the species column
        plt.figure(figsize=(8, 6))
        sns.violinplot(x='species', y=feature, data=df)
        plt.title(f'Violin plot of {feature} by species')
        plt.show()


def main():
    """
    Main function to execute the data analysis workflow.
    """
    # Load the dataset
    print("Loading the dataset...")
    df = load_data()

    # Explore the dataset
    print("Exploring the dataset...")
    explore_data(df)

    # Visualize the dataset
    print("Visualizing the dataset...")
    visualize_data(df)


if __name__ == '__main__':
    main()
