import polars as pl


def compare_csvs(file_a: str, file_b: str) -> None:
    df_a = pl.read_csv(file_a)
    df_b = pl.read_csv(file_b)

    # Compare shapes
    if df_a.shape != df_b.shape:
        print(f"Different number of rows/columns: {df_a.shape} vs {df_b.shape}")

    # Compare columns
    if set(df_a.columns) != set(df_b.columns):
        print(f"Different columns: {set(df_a.columns)} vs {set(df_b.columns)}")

    # Compare data
    comparison = df_a.frame_equal(df_b)
    if comparison:
        print("CSV files are equal.")
    else:
        print("CSV files are not equal.")


if __name__ == '__main__':
    # Example usage
    compare_csvs('file_a.csv', 'file_b.csv')