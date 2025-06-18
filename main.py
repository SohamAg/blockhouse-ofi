
#Brings it all together
import os
import pandas as pd
from ofi_feature_generator import compute_ofi_features
from ofi_cross_assets import compute_cross_asset_ofi
from plot import plot_feature

DATA_DIR = "data"
OUTPUT_DIR = "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# loading all the csvs. NOTE: we assume that all files are named in the format: "symbol.csv"
file_dict = {}
for filename in os.listdir(DATA_DIR):
    if filename.endswith(".csv"):
        symbol = filename.replace(".csv", "")
        path = os.path.join(DATA_DIR, filename)
        df = pd.read_csv(path)
        file_dict[symbol] = df

if "AAPL" not in file_dict:
    raise ValueError("AAPL.csv not found in data/")

# Computing OFI features for AAPL stock
aapl_df = compute_ofi_features(file_dict["AAPL"])

#Dropping non relavant columns
keep_cols = ['ts_event', 'symbol', 'best_level_ofi', 'integrated_ofi', 'multi_level_ofi']
# These are the length 10 vectors we get after computing ofi for all levels during multi-level. Currently I am not including them in the excel output
# keep_cols += [col for col in aapl_df.columns if col.startswith('ofi_level_')]
aapl_df_clean = aapl_df[keep_cols]


# Saving and plotting AAPL ofi features barring cross asset
aapl_df_clean.to_csv(os.path.join(OUTPUT_DIR, "AAPL_ofi_features.csv"), index=False)
plot_feature(aapl_df_clean, "best_level_ofi")
plot_feature(aapl_df_clean, "multi_level_ofi")
plot_feature(aapl_df_clean, "integrated_ofi")

# Logic to implement Cross Asset if and only if we have more than 2 files. Cross Asset requires data on more stocks
if len(file_dict) >= 2:
    cross_ofi_result = compute_cross_asset_ofi(file_dict)
    
    if cross_ofi_result is not None and not cross_ofi_result.empty:
        aapl_cross = pd.merge(aapl_df_clean, cross_ofi_result, on="ts_event", how="inner")
        aapl_cross.to_csv(os.path.join(OUTPUT_DIR, "AAPL_ofi_all_features.csv"), index=False)
        plot_feature(aapl_cross, "cross_asset_ofi")
    else:
        print("Cross-asset OFI for AAPL not returned.")
else:
    print("Only AAPL data available — skipping cross-asset OFI.")
