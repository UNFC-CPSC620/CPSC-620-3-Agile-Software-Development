import pandas as pd
from pathlib import Path


# ============================================================
# 1. Load Dataset
# ============================================================

def load_data(file_path):
    """
    Load the NYC Airbnb dataset from a CSV file.

    Parameters:
        file_path (str or Path): Path to the CSV file.

    Returns:
        pd.DataFrame: Original Airbnb dataset.
    """

    file_path = Path(file_path)

    # Check whether the dataset exists
    if not file_path.is_file():
        raise FileNotFoundError(
            f"Dataset not found: {file_path}"
        )

    # Load CSV file
    df = pd.read_csv(file_path)

    # Check whether the dataset is empty
    if df.empty:
        raise ValueError(
            "The dataset is empty."
        )

    return df


# ============================================================
# 2. Clean Dataset
# ============================================================

def clean_data(df):
    """
    Clean and prepare the NYC Airbnb dataset.

    Cleaning steps:
    1. Validate required columns.
    2. Remove duplicate records.
    3. Convert numeric columns.
    4. Handle missing values.
    5. Remove invalid numeric values.
    6. Standardize categorical values.
    7. Reset the DataFrame index.

    Parameters:
        df (pd.DataFrame): Original Airbnb dataset.

    Returns:
        pd.DataFrame: Cleaned Airbnb dataset.
    """

    # Step 1: Validate input
    if not isinstance(df, pd.DataFrame):
        raise TypeError(
            "Input must be a pandas DataFrame."
        )

    required_columns = [
        "price",
        "room_type",
        "neighbourhood",
        "minimum_nights"
    ]

    missing_columns = [
        col for col in required_columns
        if col not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns}"
        )

    # Create a copy to protect the original dataset
    df = df.copy()

    # Step 2: Remove duplicate records
    df = df.drop_duplicates()

    # Step 3: Convert price to numeric
    df["price"] = (
        df["price"]
        .astype("string")
        .str.replace("$", "", regex=False)
        .str.replace(",", "", regex=False)
        .str.strip()
    )

    df["price"] = pd.to_numeric(
        df["price"],
        errors="coerce"
    )

    # Convert minimum_nights to numeric
    df["minimum_nights"] = pd.to_numeric(
        df["minimum_nights"],
        errors="coerce"
    )

    # Step 4: Standardize text fields
    df["room_type"] = (
        df["room_type"]
        .astype("string")
        .str.strip()
        .str.replace(r"\s+", " ", regex=True)
    )

    df["neighbourhood"] = (
        df["neighbourhood"]
        .astype("string")
        .str.strip()
    )

    # Replace empty strings with missing values
    df["room_type"] = df["room_type"].replace(
        "", pd.NA
    )

    df["neighbourhood"] = df["neighbourhood"].replace(
        "", pd.NA
    )

    # Remove records with missing required values
    df = df.dropna(
        subset=required_columns
    )

    # Step 5: Remove invalid numeric values
    df = df[
        (df["price"] > 0) &
        (df["minimum_nights"] > 0)
    ].copy()

    # Step 6: Standardize room type names
    df["room_type"] = (
        df["room_type"]
        .str.lower()
        .replace({
            "entire home/apt": "Entire home/apt",
            "private room": "Private room",
            "shared room": "Shared room",
            "hotel room": "Hotel room"
        })
    )

    # Step 7: Reset index
    df = df.reset_index(drop=True)

    return df


# ============================================================
# 3. Generate Data Summary
# ============================================================

def get_data_summary(df):
    """
    Generate basic summary statistics for the cleaned dataset.

    Parameters:
        df (pd.DataFrame): Cleaned Airbnb dataset.

    Returns:
        dict: Summary statistics.
    """

    if not isinstance(df, pd.DataFrame):
        raise TypeError(
            "Input must be a pandas DataFrame."
        )

    required_columns = [
        "price",
        "room_type"
    ]

    missing_columns = [
        col for col in required_columns
        if col not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns}"
        )

    # Handle empty datasets
    if df.empty:
        return {
            "total_listings": 0,
            "average_price": None,
            "median_price": None,
            "room_types": {}
        }

    # Generate summary statistics
    summary = {
        "total_listings": len(df),

        "average_price": round(
            float(df["price"].mean()), 2
        ),

        "median_price": round(
            float(df["price"].median()), 2
        ),

        "room_types": (
            df["room_type"]
            .value_counts()
            .to_dict()
        )
    }

    return summary


# ============================================================
# 4. Main Program
# ============================================================

def main():

    print("=== NYC Airbnb Data Summary Tool ===")

    # Step 1: Locate the dataset
    project_root = Path(__file__).resolve().parent.parent

    file_path = (
        project_root /
        "data" /
        "Airbnb_NYC.csv"
    )

    # Step 2: Load original dataset
    data = load_data(file_path)

    # Step 3: Clean dataset
    cleaned_data = clean_data(data)

    # Step 4: Generate summary
    summary = get_data_summary(cleaned_data)

    # Step 5: Display cleaning results
    print("\n=== Data Cleaning Results ===")

    print("Original listings:", len(data))

    print("Cleaned listings:", len(cleaned_data))

    removed_records = len(data) - len(cleaned_data)

    print("Removed records:", removed_records)

    # Step 6: Display summary statistics
    print("\n=== Summary Statistics ===")

    print(
        "Total listings:",
        summary["total_listings"]
    )

    print(
        "Average price:",
        summary["average_price"]
    )

    print(
        "Median price:",
        summary["median_price"]
    )

    # Step 7: Display room type distribution
    print("\n=== Room Type Distribution ===")

    for room_type, count in summary["room_types"].items():
        print(f"{room_type}: {count}")

    # Step 8: Validate cleaned dataset
    print("\n=== Data Validation ===")

    required_columns = [
        "price",
        "room_type",
        "neighbourhood",
        "minimum_nights"
    ]

    # Check missing values
    assert cleaned_data[required_columns].notna().all().all(), (
        "Missing values found in required columns."
    )

    # Check valid prices
    assert (cleaned_data["price"] > 0).all(), (
        "Invalid prices detected."
    )

    # Check valid minimum nights
    assert (cleaned_data["minimum_nights"] > 0).all(), (
        "Invalid minimum nights detected."
    )

    # Check duplicate records
    assert not cleaned_data.duplicated().any(), (
        "Duplicate records detected."
    )

    print("All basic data validation checks passed.")


# ============================================================
# 5. Run Program
# ============================================================

if __name__ == "__main__":
    main()