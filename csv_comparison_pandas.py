import pandas as pd

class CSVComparisonTool:
    def __init__(self, file_a, file_b):
        self.file_a = file_a
        self.file_b = file_b
        self.df_a = pd.read_csv(file_a)
        self.df_b = pd.read_csv(file_b)

    def stage_one(self):
        # Initial comparison: check for identical rows
        identical = self.df_a[self.df_a.isin(self.df_b).all(axis=1)]
        return identical

    def stage_two(self):
        # Intermediate comparison: find different rows
        different = pd.concat([self.df_a, self.df_b]).drop_duplicates(keep=False)
        return different

    def stage_three(self):
        # Final output: summary of differences
        summary = {
            'identical': self.stage_one().shape[0],
            'different': self.stage_two().shape[0],
        }
        return summary

if __name__ == '__main__':
    file_a = 'path/to/first_file.csv'
    file_b = 'path/to/second_file.csv'
    tool = CSVComparisonTool(file_a, file_b)
    print("Identical rows:", tool.stage_one())
    print("Different rows:", tool.stage_two())
    print("Summary:", tool.stage_three())