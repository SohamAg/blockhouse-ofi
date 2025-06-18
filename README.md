# Order Flow Imbalance (OFI) Feature Construction

This repository implements four key OFI features for analyzing order book dynamics, as outlined in the research paper _"Cross-Impact of Order Flow Imbalance in Equity Markets"_:

1. **Best-Level OFI**
2. **Multi-Level OFI**
3. **Integrated OFI (via PCA)**
4. **Cross-Asset OFI (via Lasso regression)**


Folder Structure is as follows:

blockhouse-ofi/
├── data/ # Input CSV files (e.g., AAPL.csv, GOOG.csv)
├── output/ # Output CSVs and plots
├── main.py # Main script to run all OFI feature extraction
├── ofi_feature_generator.py # Best, Multi-Level, and Integrated OFI logic
├── ofi_cross_assets.py # Cross-Asset OFI logic (Equation 9 from paper)
├── ofi_utils.py # Utility functions for OFI calculations
├── plot.py # Plotting utilities for features
├── README.md # Documentation and instructions
├── requirements.txt # Python dependencies
└── .gitignore # Files to exclude from version control

## NOTE TO TESTERS

The cross-asset ofi requires the data for more than 1 stock. Since only the data for AAPL was provided, I used the same data given to also make GOOG.csv, only with the symbol name changed. The repo also assumes the nomenclature of "symbol.csv" for the data files. Additionally, the cross-asset implementation has Equation (8), as well as (9), the latter of which is the current default implementation.
