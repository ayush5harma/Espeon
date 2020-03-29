# Agent's pseudocode 
## main loop
# while True:
    ## ask bettercap for all visible access points and their clients
 #   aps = get_all_visible_access_points()
    ## loop each AP
  #  for ap in aps:
        ## send an association frame in order to grab the PMKID
   #     send_assoc(ap)
        ## loop each client station of the AP
    #    for client in ap.clients:
            ## deauthenticate the client to get its half or full handshake
     #       deauthenticate(client)

    # wait_for_loot()



class Agent():
