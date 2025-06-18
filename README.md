# Order Flow Imbalance (OFI) Feature Construction

This repository implements four key OFI features for analyzing order book dynamics, as outlined in the research paper _"Cross-Impact of Order Flow Imbalance in Equity Markets"_:

1. **Best-Level OFI**
2. **Multi-Level OFI**
3. **Integrated OFI (via PCA)**
4. **Cross-Asset OFI (via Lasso regression)**


Folder Structure is as follows:

blockhouse-ofi/
│
├── data/                       # Input folder for order book CSVs (e.g., AAPL.csv, GOOG.csv)
│   └── AAPL.csv               # Example: Order book data for AAPL
|   └── GOOG.csv               # Example: This is the exact same order book as before, just with the symbol changed to GOOG
│
├── output/                     # All generated feature CSVs and plots are saved here
│   ├── AAPL_ofi_features.csv   # Best, Multi-Level, Integrated OFI features for AAPL
│   ├── AAPL_ofi_all_features.csv  # Includes cross-asset OFI if available
│
├── ofi_utils.py                # Core utility functions for OFI calculations (level-wise, etc.)
├── ofi_feature_generator.py    # Handles feature computation for AAPL: best, multi, integrated OFI
├── ofi_cross_assets.py         # Computes Cross-Asset OFI using Lasso regression + PCA
├── plot.py                     # Utility for visualizing OFI features
├── main.py                     # Entry point: loads files, computes features, saves and plots results
│
├── requirements.txt            # Python dependencies
└── README.md                   # Documentation and setup instructions

## NOTE TO TESTERS

The cross-asset ofi requires the data for more than 1 stock. Since only the data for AAPL was provided, I used the same data given to also make GOOG.csv, only with the symbol name changed. The repo also assumes the nomenclature of "symbol.csv" for the data files. Additionally, the cross-asset implementation has Equation (8), as well as (9), the latter of which is the current default implementation.