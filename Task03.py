import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def load_data():
    iris = sns.load_dataset('iris')
    return iris


def explore_data(df):
    print("First 5 rows of the dataset:")
    print(df.head())

    print("\nSummary statistics:")
    print(df.describe())

    print("\nData types and missing values:")
    print(df.info())


def visualize_data(df):
    sns.set(style="whitegrid")
    print("\nCreating pairplot...")
    pairplot = sns.pairplot(df, hue='species', markers=["o", "s", "D"])
    pairplot.fig.suptitle('Pairplot of Iris Dataset', y=1.02)
    plt.show()

    print("\nCreating boxplot...")
    plt.figure(figsize=(12, 8))
    sns.boxplot(data=df)
    plt.title('Boxplot of Iris Dataset Features')
    plt.show()

    print("\nCreating violin plots...")
    for feature in df.columns[:-1]:
        plt.figure(figsize=(8, 6))
        sns.violinplot(x='species', y=feature, data=df)
        plt.title(f'Violin plot of {feature} by species')
        plt.show()


def main():
    print("Loading the dataset...")
    df = load_data()

    print("Exploring the dataset...")
    explore_data(df)

    print("Visualizing the dataset...")
    visualize_data(df)


if __name__ == '__main__':
    main()
