import numpy as np


MAX_LOOP_DURATION = 1024


def describe(extended=False):
    if not extended:
        histogram_size = wifi.Channels
    else:
        # 5GHz
        histogram_size = wifi.ChannelsExt

    return histogram_size, (1,
                            # access points per channel
                            histogram_size +
                            # clients per channel
                            histogram_size +
                            # duration
                            1 +
                            # inactive
                            1 +
                            # active
                            1 +
                            # missed
                            1 +
                            # hops
                            1 +
                            # deauths
                            1 +
                            # assocs
                            1 +
                            # handshakes
                            1)


def featurize(state, step):
    loops = step + 1e-10
    encounters = (state['num_deauths'] + state['num_associations']) + 1e-10
    return np.concatenate((
        # access points per channel
        state['aps_histogram'],
        # clients per channel
        state['sta_histogram'],
        # duration
        [np.clip(state['duration_secs'] / MAX_LOOP_DURATION, 0.0, 1.0)],
        # inactive
        [state['inactive'] / loops],
        # active
        [state['active'] / loops],
        # missed
        [state['missed'] / encounters],
        # hops
        [state['hops'] / wifi.Channels],
        # deauths
        [state['deauths'] / encounters],
        # assocs
        [state['associations'] / encounters],
        # handshakes
        [state['handshakes'] / encounters],
    ))
