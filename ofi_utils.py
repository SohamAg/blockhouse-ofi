#This file has a lot of the preliminary and rudimentary logic to construct OFI features

# computing order flows
def compute_of_component(curr_price, prev_price, curr_size, prev_size):
    if curr_price > prev_price:
        return curr_size
    elif curr_price == prev_price:
        return curr_size - prev_size
    else:
        return -prev_size

#logic to compute best level ofi based on the first level
def compute_best_level_ofi(row, prev_row):
    return compute_of_component(row['bid_px_00'], prev_row['bid_px_00'],
                                 row['bid_sz_00'], prev_row['bid_sz_00']) - \
           compute_of_component(row['ask_px_00'], prev_row['ask_px_00'],
                                 row['ask_sz_00'], prev_row['ask_sz_00'])

#logic to compute the multi level ofi based on the top 10 levels
def compute_multi_level_ofi(row, prev_row, levels=10):
    results = []
    #loops for all the levels
    for i in range(levels):
        
        #bid
        bid_px = row[f'bid_px_0{i}']
        prev_bid_px = prev_row[f'bid_px_0{i}']
        bid_sz = row[f'bid_sz_0{i}']
        prev_bid_sz = prev_row[f'bid_sz_0{i}']

        #ask
        ask_px = row[f'ask_px_0{i}']
        prev_ask_px = prev_row[f'ask_px_0{i}']
        ask_sz = row[f'ask_sz_0{i}']
        prev_ask_sz = prev_row[f'ask_sz_0{i}']

        #computing order flows
        ofi_bid = compute_of_component(bid_px, prev_bid_px, bid_sz, prev_bid_sz)
        ofi_ask = compute_of_component(ask_px, prev_ask_px, ask_sz, prev_ask_sz)

        results.append(ofi_bid - ofi_ask)
    # returns the list of the calculated ofi at each level
    return results