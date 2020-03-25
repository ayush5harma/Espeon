# state contains the information of the last loop
# n is the number of that last loop
loops = n + 1e-20 # 1e-20 is added to avoid a division by 0 //10 to the power -20 
encounters = max(state['num_deauths'] + state['num_associations'], state['num_handshakes']) + 1e-20
channels = wifi.Channels

# handshakes
h = state['num_handshakes'] / encounters
# small positive rewards the more active loops we have
a = .2 * (state['active'] / loops)
# ai should keep hopping on the widest channel spectrum
c = .1 * (state['hops'] / channels)
# small negative reward if we don't see access points for a while
b = -.3 * (state['blind'] / loops)
# small negative reward if we interact with things that are not in range anymore
m = -.3 * (state['missed'] / encounters)
# small negative reward for inactive loop
i = -.2 * (state['inactive'] / loops)

reward = h + a + c + b + i + m