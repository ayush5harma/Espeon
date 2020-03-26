import subprocess

Channels = 140     # 2.4Ghz
ChannelsExt = 165  # 5Ghz


def freq_to_channel(freq):
    if freq <= 2472:
        return int(((freq - 2412) / 5) + 1)
    elif freq == 2484:
        return int(14)
    elif 5035 <= freq <= 5865:
        return int(((freq - 5035) / 5) + 7)
    else:
        return 0

def iface_channels(ifname):
    channels = []
    output = subprocess.getoutput("/sbin/iwlist %s freq" % ifname)
    for line in output.split("\n"):
        line = line.strip()
        if line.startswith("Channel "):
            channels.append(int(line.split()[1]))
    return channels
