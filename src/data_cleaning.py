import pandas as pd


def load_data(file_path):
    """
    Load the NYC Airbnb dataset from a CSV file.

    Parameters:
        file_path (str): Path to the CSV file.

    Returns:
        pd.DataFrame: Original dataset.
    """
    return pd.read_csv(file_path)


def clean_data(df):
    """
    Clean and prepare the NYC Airbnb dataset.

    Cleaning steps:
    1. Remove duplicate records.
    2. Convert price and minimum_nights to numeric.
    3. Remove records with missing required values.
    4. Remove invalid prices and minimum nights.
    5. Standardize room type names.

    Returns:
        pd.DataFrame: Cleaned dataset.
    """

    df = df.copy()

    # Remove duplicate records
    df = df.drop_duplicates()

    # Convert price to numeric
    df["price"] = (
        df["price"]
        .astype("string")
        .str.replace("$", "", regex=False)
        .str.replace(",", "", regex=False)
    )

    df["price"] = pd.to_numeric(
        df["price"], errors="coerce"
    )

    # Convert minimum nights to numeric
    df["minimum_nights"] = pd.to_numeric(
        df["minimum_nights"], errors="coerce"
    )

    # Remove records with missing required values
    df = df.dropna(
        subset=[
            "price",
            "room_type",
            "neighbourhood",
            "minimum_nights"
        ]
    )

    # Remove invalid values
    df = df[
        (df["price"] > 0) &
        (df["minimum_nights"] > 0)
    ].copy()

    # Standardize room type names
    df["room_type"] = (
        df["room_type"]
        .astype("string")
        .str.strip()
        .str.lower()
        .replace({
            "entire home/apt": "Entire home/apt",
            "private room": "Private room",
            "shared room": "Shared room"
        })
    )

    return df


def get_data_summary(df):
    """
    Generate basic summary statistics.

    Returns:
        dict: Summary of cleaned Airbnb listings.
    """

    return {
        "total_listings": len(df),
        "average_price": round(df["price"].mean(), 2),
        "median_price": round(df["price"].median(), 2),
        "room_types": df["room_type"].value_counts().to_dict()
    }


if __name__ == "__main__":

    # Step 1: Load dataset
    data = load_data("data/Airbnb_NYC.csv")

    # Step 2: Clean dataset
    cleaned_data = clean_data(data)

    # Step 3: Generate summary
    summary = get_data_summary(cleaned_data)

    # Step 4: Display results
    print("=== NYC Airbnb Data Summary Tool ===")

    print("\nOriginal listings:", len(data))
    print("Cleaned listings:", len(cleaned_data))
    print("Removed records:", len(data) - len(cleaned_data))

    print("\n=== Summary Statistics ===")
    print("Total listings:", summary["total_listings"])
    print("Average price:", summary["average_price"])
    print("Median price:", summary["median_price"])

    print("\n=== Room Type Distribution ===")

    for room_type, count in summary["room_types"].items():
        print(f"{room_type}: {count}")