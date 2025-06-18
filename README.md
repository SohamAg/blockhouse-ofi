# Order Flow Imbalance (OFI) Feature Construction

This repository implements four key OFI features for analyzing order book dynamics, as outlined in the research paper _"Cross-Impact of Order Flow Imbalance in Equity Markets"_:

1. **Best-Level OFI**
2. **Multi-Level OFI**
3. **Integrated OFI (via PCA)**
4. **Cross-Asset OFI (via Lasso regression)**


## NOTE TO TESTERS

The Cross-Asset OFI feature requires data from at least two distinct stocks. Since only data for AAPL was provided, I duplicated the same dataset and renamed it as GOOG.csv + changed the symbols from AAPL -> GOOG to enable the computation. The repository expects all input files to follow the naming convention: SYMBOL.csv (e.g., AAPL.csv, GOOG.csv) and to be placed in the data/ folder.

The Cross-Asset OFI logic includes implementations of both Equation (8) and Equation (9) from the referenced paper. The default computation currently uses Equation (9), which incorporates integrated OFI via PCA. Equation (8), based on best-level OFI, is present but commented out and can be enabled if desired.

For Multi-Level OFI, I compute the OFI vector across all 10 depth levels and default to summing the values for aggregation under multi_level_ofi columns, as the paper does not specify a single standard for collapsing the vector. This does not change the veracity of the other implementations, such as integerated ofi, since they use the OFI vector directly.

Both Best-Level OFI and Integrated OFI are implemented according to the definitions and motivations provided in the paper.
