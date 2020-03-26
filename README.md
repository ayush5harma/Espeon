# Espeon -Raspberry pi pokemon that gamifies WiFi Hacking
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
- **Deauthenticating the client stations it detects.**- A deauthenticated device must reauthenticate to its access point by re-performing the 4-Way Handshake with the AP, thereby giving espeon another chance to sniff the handshake packets and collect more crackable material.
- **Sending association frames directly- to the access points themselves** to try to force them to leak the PMKID.
-  **Passively collects handshakes**- if a device happens to be attempting to authenticate to an AP on the same channel that the unit just so happens to be monitoring at that time, espeon may eat  handshakes completely by chance (and not as the result of a deauthentication or PMKID attack).  

All the handshakes captured are saved into .pcap files.These handshakes can later be cracked with proper hardware and software.
