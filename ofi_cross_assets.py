# This is the cross asset file. I implemented this separately for reasons I mention in the README.md

import pandas as pd
import numpy as np
from sklearn.decomposition import PCA
from sklearn.linear_model import LassoCV
from ofi_utils import compute_multi_level_ofi, compute_best_level_ofi

def compute_cross_asset_ofi(file_dict):
    # Check to see whether there are enough files to calculate cross asset ofi
    if len(file_dict) < 2:
        print("Need ≥2 assets for cross-asset OFI.")
        return None

    target_symbol = list(file_dict.keys())[0]
    symbol_frames = {}

    # This implementation used the integerated ofi equation. 
    for symbol, df in file_dict.items():
        #Logic is similar to the previous computer integerated ofis
        df['ts_event'] = pd.to_datetime(df['ts_event'])
        multi_level_ofis = [compute_multi_level_ofi(df.iloc[i], df.iloc[i - 1]) for i in range(1, len(df))]
        ofi_matrix = np.array(multi_level_ofis)
        pca = PCA(n_components=1)
        integrated_ofi = pca.fit_transform(ofi_matrix).flatten()
        
        #Indexing the integerated ofi in the dataframe
        ofi_df = df.iloc[1:].copy().reset_index(drop=True)
        ofi_df[f'{symbol}_integrated_ofi'] = integrated_ofi
        symbol_frames[symbol] = ofi_df[['ts_event', f'{symbol}_integrated_ofi']]

    #merging the stocks' ofi with the timeframes
    merged = symbol_frames[list(symbol_frames.keys())[0]]
    for symbol in list(symbol_frames.keys())[1:]:
        merged = pd.merge(merged, symbol_frames[symbol], on='ts_event', how='inner')

    #Setting up the regularization
    X = merged[[col for col in merged.columns if target_symbol not in col and col != 'ts_event']].values
    y = merged[f'{target_symbol}_integrated_ofi'].values
    
    #Setting the model
    model = LassoCV(cv=5).fit(X, y)
    y_pred = model.predict(X)
    merged['cross_asset_ofi'] = np.abs(y_pred)

    # merged['symbol'] = target_symbol
    return merged[['ts_event', 'cross_asset_ofi']]

    # THis is the additional best level ofi equation implementation, primarily it only has the PCA part not implemented
    # symbol_frames = {}
    # for symbol, df in file_dict.items():
    #     df['ts_event'] = pd.to_datetime(df['ts_event'])
    #     best_ofis = [compute_best_level_ofi(df.iloc[i], df.iloc[i - 1]) for i in range(1, len(df))]
    #     ofi_df = df.iloc[1:].copy().reset_index(drop=True)
    #     ofi_df[f'{symbol}_best_ofi'] = best_ofis
    #     symbol_frames[symbol] = ofi_df[['ts_event', f'{symbol}_best_ofi']]

    # merged = symbol_frames[list(symbol_frames.keys())[0]]
    # for symbol in list(symbol_frames.keys())[1:]:
    #     merged = pd.merge(merged, symbol_frames[symbol], on='ts_event', how='inner')

    # X = merged[[col for col in merged.columns if target_symbol not in col]].values
    # y = merged[f'{target_symbol}_best_ofi'].values
    # model = LassoCV(cv=5).fit(X, y)
    # y_pred = model.predict(X)
    # merged['cross_asset_ofi'] = np.abs(y_pred)
    # merged['symbol'] = target_symbol
    # return merged[['symbol', 'ts_event', 'cross_asset_ofi']]
