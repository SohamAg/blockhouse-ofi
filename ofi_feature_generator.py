#THis is the file that generates the ofi features, primarily used in main
import pandas as pd
from sklearn.decomposition import PCA
from ofi_utils import compute_best_level_ofi, compute_multi_level_ofi

#Function that compute the ofi features apart from cross-asset. Details why cross asset is not included here are in the README.md
def compute_ofi_features(df):
    #Changing into datetime pandas timestamp. Helpful for plotting and showcasing extracted features
    df['ts_event'] = pd.to_datetime(df['ts_event'])
    
    best_ofi, multi_ofi = [], []

    #Finding best ofi and multi ofi for all timestamps
    for i in range(1, len(df)):
        row, prev = df.iloc[i], df.iloc[i - 1]
        best_ofi.append(compute_best_level_ofi(row, prev))
        multi_ofi.append(compute_multi_level_ofi(row, prev))

    # Reindexing to start from row 1 since formula requires current and previous time stamp
    df_out = df.iloc[1:].copy().reset_index(drop=True)
    
    #Loading the calculated features into a csv
    df_out['best_level_ofi'] = best_ofi
    for i in range(10):
        df_out[f'ofi_level_{i}'] = [vec[i] for vec in multi_ofi]

    #Logic to implement integerated_ofi using PCA
    pca = PCA(n_components=1)
    ofi_matrix = df_out[[f'ofi_level_{i}' for i in range(10)]].values
    df_out['integrated_ofi'] = pca.fit_transform(ofi_matrix)
    
    #Saving the sum of all the values for multi level, please read README.md
    df_out['multi_level_ofi'] = ofi_matrix.sum(axis=1)
    return df_out