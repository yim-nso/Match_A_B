import pandas as pd
import numpy as np
from typing import Tuple, Dict
import os


class CSVComparisonToolPandas:
    """
    CSV Comparison Tool using Pandas for 3-stage matching
    Stage 1: Compare A & B using HouseNumber, FirstName, Lastname, Relationship = 01
    Stage 2: Compare UnMatch_A & B using HouseNumber
    Stage 3: Compare UnMatch_B & A using HouseNumber, FirstName, Lastname, Relationship = 02-16 or Blank
    """
    
    def __init__(self, file_a: str, file_b: str, output_dir: str = './output'):
        """Initialize with CSV files"""
        self.file_a = file_a
        self.file_b = file_b
        self.output_dir = output_dir
        self.df_a = None
        self.df_b = None
        
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        self._load_and_clean_data()
    
    def _load_and_clean_data(self):
        """Load CSV files and apply cleaning (trim, case-insensitive, blank handling)"""
        print("[Pandas] Loading CSV files...")
        self.df_a = pd.read_csv(self.file_a)
        self.df_b = pd.read_csv(self.file_b)
        
        print(f"[Pandas] File A rows: {len(self.df_a)}, File B rows: {len(self.df_b)}")
        
        # Clean data: trim spaces and convert to lowercase
        self._clean_dataframe(self.df_a)
        self._clean_dataframe(self.df_b)
    
    def _clean_dataframe(self, df: pd.DataFrame):
        """Clean dataframe: trim strings, convert to lowercase"""
        for col in df.columns:
            if df[col].dtype == 'object':
                # Fill NaN with empty string, trim spaces, convert to lowercase
                df[col] = df[col].fillna('').astype(str).str.strip().str.lower()
    
    def _normalize_key(self, value: str) -> str:
        """Normalize key value: fill blank, trim, lowercase"""
        if pd.isna(value) or value == '':
            return ''
        return str(value).strip().lower()
    
    def _stage_one_comparison(self) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        """
        Stage 1: Compare A & B using HouseNumber, FirstName, Lastname, Relationship = 01
        """
        print("\n[Pandas] === Stage 1: Comparing A & B ===\n")
        print("Criteria: HouseNumber + FirstName + Lastname + (Relationship = '01')")
        
        # Filter records with Relationship = '01'
        df_a_stage1 = self.df_a[self.df_a.get('Relationship', '') == '01'].copy()
        
        # Create comparison key
        df_a_stage1['match_key'] = (
            df_a_stage1['HouseNumber'].astype(str) + '|' +
            df_a_stage1['FirstName'].astype(str) + '|' +
            df_a_stage1['Lastname'].astype(str)
        )
        
        df_b_key = (
            self.df_b['HouseNumber'].astype(str) + '|' +
            self.df_b['FirstName'].astype(str) + '|' +
            self.df_b['Lastname'].astype(str)
        )
        
        # Find matches and unmatches
        match_mask = df_a_stage1['match_key'].isin(df_b_key)
        match_a = df_a_stage1[match_mask].drop('match_key', axis=1)
        unmatch_a = df_a_stage1[~match_mask].drop('match_key', axis=1)
        
        print(f"Matches: {len(match_a)}, Unmatches: {len(unmatch_a)}")
        
        return match_a, unmatch_a, self.df_b
    
    def _stage_two_comparison(self, unmatch_a: pd.DataFrame, df_b: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        Stage 2: Compare UnMatch_A & B using HouseNumber
        """
        print("\n[Pandas] === Stage 2: Comparing UnMatch_A & B ===\n")
        print("Criteria: HouseNumber only")
        
        # Create comparison key using HouseNumber
        unmatch_a['house_key'] = unmatch_a['HouseNumber'].astype(str)
        df_b_key = df_b['HouseNumber'].astype(str)
        
        # Find matches and unmatches
        match_mask = unmatch_a['house_key'].isin(df_b_key)
        match_b = unmatch_a[match_mask].drop('house_key', axis=1)
        unmatch_b = unmatch_a[~match_mask].drop('house_key', axis=1)
        
        print(f"Matches: {len(match_b)}, Unmatches: {len(unmatch_b)}")
        
        return match_b, unmatch_b
    
    def _stage_three_comparison(self, unmatch_b: pd.DataFrame, df_b: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        Stage 3: Compare UnMatch_B & B using HouseNumber, FirstName, Lastname, Relationship = 02-16 or Blank
        """
        print("\n[Pandas] === Stage 3: Comparing UnMatch_B & B ===\n")
        print("Criteria: HouseNumber + FirstName + Lastname + (Relationship = '02-16' or Blank)")
        
        # Filter records from B with Relationship = 02-16 or Blank
        df_b_stage3 = df_b[
            (df_b.get('Relationship', '').astype(str).str.strip() == '') |
            (df_b.get('Relationship', '').astype(str).isin(['02', '03', '04', '05', '06', '07', '08', '09', '10', 
                                                             '11', '12', '13', '14', '15', '16']))
        ].copy()
        
        # Create comparison key
        unmatch_b_key = (
            unmatch_b['HouseNumber'].astype(str) + '|' +
            unmatch_b['FirstName'].astype(str) + '|' +
            unmatch_b['Lastname'].astype(str)
        )
        
        df_b_stage3['match_key'] = (
            df_b_stage3['HouseNumber'].astype(str) + '|' +
            df_b_stage3['FirstName'].astype(str) + '|' +
            df_b_stage3['Lastname'].astype(str)
        )
        
        # Find matches and unmatches
        match_mask = unmatch_b_key.isin(df_b_stage3['match_key'])
        match_c = unmatch_b[match_mask]
        unmatch_c = unmatch_b[~match_mask]
        
        print(f"Matches: {len(match_c)}, Unmatches: {len(unmatch_c)}")
        
        return match_c, unmatch_c
    
    def run_comparison(self) -> Dict[str, str]:
        """Run all 3 stages and export results"""
        print("\n" + "="*60)
        print("CSV COMPARISON TOOL - PANDAS VERSION")
        print("="*60)
        
        # Stage 1
        match_a, unmatch_a, df_b = self._stage_one_comparison()
        
        # Stage 2
        match_b, unmatch_b = self._stage_two_comparison(unmatch_a, df_b)
        
        # Stage 3
        match_c, unmatch_c = self._stage_three_comparison(unmatch_b, self.df_b)
        
        # Export results
        output_files = {
            'Match_A': os.path.join(self.output_dir, 'Match_A.csv'),
            'UnMatch_A': os.path.join(self.output_dir, 'UnMatch_A.csv'),
            'Match_B': os.path.join(self.output_dir, 'Match_B.csv'),
            'UnMatch_B': os.path.join(self.output_dir, 'UnMatch_B.csv'),
            'Match_C': os.path.join(self.output_dir, 'Match_C.csv'),
            'UnMatch_C': os.path.join(self.output_dir, 'UnMatch_C.csv'),
        }
        
        print("\n" + "="*60)
        print("EXPORTING RESULTS")
        print("="*60)
        
        match_a.to_csv(output_files['Match_A'], index=False)
        print(f"✓ Exported {len(match_a)} records to {output_files['Match_A']}")
        
        unmatch_a.to_csv(output_files['UnMatch_A'], index=False)
        print(f"✓ Exported {len(unmatch_a)} records to {output_files['UnMatch_A']}")
        
        match_b.to_csv(output_files['Match_B'], index=False)
        print(f"✓ Exported {len(match_b)} records to {output_files['Match_B']}")
        
        unmatch_b.to_csv(output_files['UnMatch_B'], index=False)
        print(f"✓ Exported {len(unmatch_b)} records to {output_files['UnMatch_B']}")
        
        match_c.to_csv(output_files['Match_C'], index=False)
        print(f"✓ Exported {len(match_c)} records to {output_files['Match_C']}")
        
        unmatch_c.to_csv(output_files['UnMatch_C'], index=False)
        print(f"✓ Exported {len(unmatch_c)} records to {output_files['UnMatch_C']}")
        
        # Print summary
        print("\n" + "="*60)
        print("SUMMARY")
        print("="*60)
        total_matched = len(match_a) + len(match_b) + len(match_c)
        total_unmatched = len(unmatch_c)
        print(f"Total Matched: {total_matched}")
        print(f"Total Unmatched: {total_unmatched}")
        print(f"Total Processed: {total_matched + total_unmatched}")
        print("="*60)
        
        return output_files


if __name__ == '__main__':
    # Example usage
    file_a = 'data_A.csv'
    file_b = 'data_B.csv'
    
    tool = CSVComparisonToolPandas(file_a, file_b)
    output_files = tool.run_comparison()