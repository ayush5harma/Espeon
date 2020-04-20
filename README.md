# Espeon -Raspberry pi pokemon that gamifies WiFi Hacking  

```
    ....                                    .....
           .+?77Gggg,                            .gggyTTTAe
          .dM@.` ``?TM8...                 ...WMM8!!!+++WM@
         .MIdNm,..`.``?7TAx              .uZT=!^^^:.qNMNId@
           dMMNe,....^^^:+dBC++vHMn....JMBI:^^^:J+jMMMMMnd9
           dRJMMNm.:^^:?+!```...^:?74Hf!^^^^:.?qMMMMMM#zMP
            ?BjMMMNe,.+?``..J,^^:^^JJWC```..JjMMMMMMMMB&T=
             jkVMMMNI+l  jk7WQs:^^:dM:..`..qNMMMMMMMMEJH:     .jQ,
               TSdMMMR.` ?SmQH$^:^^::^..?jMMMMMMMMMMkZ9`    .?! `Tn,
                `jWMMHx ```77:^:^:.....:jMMMMMMMMMUWC!      dl. .^d@.
                  .MMH8e. .^^:``.JgWWMI^^?MMMMMngd9!         dK^^::jN:
                 .kCOOdN:`^^:^..jMMNkC:^?z777CWC?!   .jQQo.  `jm:^^jM:
                dK:^^dMB:.^:^^?vWHY+::?j&.^^^:?W$   J2` `?S.. `9A+^:?Mr
               qZ1...dNs+dkz+^:^^:..JqkVWmc:^^`?Xp  dB....?jQ; .MI^^?Ml.
               MmZY9Gc7Y=ux+.^:J&gUMM0rrXM3u+^.jZY   `5A+^:?Tn,.TG+:^?dM
               ??`  ``   `!`XNNHUU0rrrOvdN:`jR+M$      ?dy^^?db. dK^:?dM
                             d#zrrrrZz:^?8a. .T!        ?Sx.^:d#`dK^^?dM
                            .dD`!!!!!^^:^?Mr             JB+.^?jWVC^:?dM
                           .MI^^^^^:^:^^:?Tn,             ,Ml^^??`.:?&VY
                           .MI.^:^:^^:^:^^?db.             ?d2^:``.^?Mr
                          .JVUz:^:?+`^^:^^:^?5+.            7Xx+...JdY!
                          J#ozz...dR^.`^:^^:^`?Xo..          d#C..^jN:
                          JN0rW#!?dK.``:^:^^:^:^?91i,       .Z= ^^jyY`
                          ?MkwZWHodK .:^^?ux^:^^:^`?Xn.    .M%...?dE
                           .MRrrdMM@^:^^:?MRjax+^:^^:d#..+J9::^:?MP
                           .HWyrwXM@^^:^jMM9?`` ``:^^?UkC?!^^^.JW:`
                             dHrrrH@:^^:JMk!```` .^^:^?Qc^:?ggZ=`
                              dNwrH@^:^dMNkc.  .^:^:^^?MMMMB:``
                             JZY+1W@:^:dMMMNe+.^^::^:jsY!
                             dHAgNr..?dMMMG&&.a&JJHMM$`
                              ?"""Xgmmv!  ?""""""=
                                   ```
```
A Deep Reinforcement Learning Minor Project  

## **Overview** :

We decided to create something new from the components we had at hand; the basis of this pet hacker is basically a Raspberry Pi  single board device.  

Espeon ingests network packets that wireless connection users send during new connection negotiation stage (process known as handshake)
This virtual pet does not select WPA keys independently.Instead, gets help from  neural networks with machine learning capabilities.  
  
## **Technicalities** :  

It is using an [LSTM with MLP feature extractor](https://stable-baselines.readthedocs.io/en/master/modules/policies.html#stable_baselines.common.policies.MlpLstmPolicy) as its policy network for the A2C agent.  
Python's [OpenAI gym](http://gym.openai.com/docs/ ) is used to create custom game environment for espeon.
## **Why it’s valuable to have an AI that wants to eat handshakes** :  

In order to understand why it’s valuable to have an AI that wants to eat handshakes, it’s helpful to understand a little bit about how handshakes are used in the WPA/WPA2 wireless protocol.

Before a client device that’s connecting to a wireless access point—say, for instance, your phone connecting to your home WiFi network—is able to securely transmit to and receive data from that access point, a process called the *4-Way Handshake* needs to happen in order for the WPA encryption keys to be generated. This process consists of the exchange of four packets (hence the “4” in “4-Way”) between the client device and the AP; these are used to derive session keys from the access point’s WiFi password. Once the packets have been successfully exchanged and the keys are generated, the client device is authenticated and can start sending and receiving data packets (now secured by encryption) to and from the wireless AP.  
So…what’s the catch? Well, these four packets can easily be “sniffed” by an attacker monitoring nearby (say, with espeon on a raspberry pi 😇). And once recorded, that attacker can use dictionary and/or bruteforce attacks to crack the handshakes and recover the original WiFi key. In fact, **successful recovery of the WiFi key doesn’t necessarily even need all four packets!** A half-handshake (containing only two of the four packets) can be cracked, too—and in some (most) cases, just a single packet is enough, even without clients.  
It uses 3 packet collection strategies:  
- **Deauthentication of detected client stations** - A deauthenticated device would need to reauthenticate to its access point by performing the 4-way handshake with its access point, and hence, providing our creature with another chance to access more crackable material.

- **Directly sending the association frames** to the wireless access points and try  prompting and forcing them to leak their PMKID.
-  **Passively collects handshakes**- if any device attempts to authenticate to an access point on the channel which the unit is monitoring at the same instance, the unite may eat the handshakes completely coincidentally, without attempting the first two methods

The handshakes eaten are saved into .pcap files which can be cracked with proper hardware and software.
