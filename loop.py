import time
import threading
import logging

from reward import RewardFunction


class Loop(object):
    def __init__(self, config):
        self.loop = 0
        self.config = config
        # how many consecutive loops with no activity
        self.inactive_for = 0
        # how many consecutive loops with activity
        self.active_for = 0
        # number of loops with no visible access points
        self.blind_for = 0
        # did deauth in this loop in the current channel?
        self.did_deauth = False
        # number of deauths in this loop
        self.deauths = 0
        # did associate in this loop in the current channel?
        self.did_associate = False
        # number of associations in this loop
        self.assocs = 0
        # number of assocs or deauths missed
        self.missed = 0
        # did get any handshake in this loop?
        self.did_handshakes = False
        # number of handshakes captured in this loop
        self.shakes = 0
        # number of channels hops
        self.hops = 0
        # number of seconds sleeping
        self.slept = 0
        # any activity at all during this loop?
        self.any_activity = False
        # when the current loop started
        self.loop_started = time.time()
        # last loop duration
        self.loop_duration = 0
        # https://www.metageek.com/training/resources/why-channels-1-6-11.html
        self.non_overlapping_channels = {1: 0, 6: 0, 11: 0}
        # observation vectors
        self._observation = {
            'aps_histogram': [0.0] * wifi.Channels,
            'sta_histogram': [0.0] * wifi.Channels,
        }
        self._observation_ready = threading.Event()
        self._loop_data = {}
        self._loop_data_ready = threading.Event()
        self._reward = RewardFunction()


    def observe(self, aps):
        num_aps = len(aps)
        if num_aps == 0:
            self.blind_for += 1
        else:
            self.blind_for = 0

        num_aps = len(aps) + 1e-10
        num_sta = sum(len(ap['clients']) for ap in aps) + 1e-10
        aps_per_chan = [0.0] * wifi.Channels
        sta_per_chan = [0.0] * wifi.Channels
        peers_per_chan = [0.0] * wifi.Channels

        for ap in aps:
            ch_idx = ap['channel'] - 1
            try:
                aps_per_chan[ch_idx] += 1.0
                sta_per_chan[ch_idx] += len(ap['clients'])
            except IndexError as e:
                logging.error("got data on channel %d, we can store %d channels" % (ap['channel'], wifi.Channels))

        # normalize
        aps_per_chan = [e / num_aps for e in aps_per_chan]
        sta_per_chan = [e / num_sta for e in sta_per_chan]
        
        self._observation = {
            'aps_histogram': aps_per_chan,
            'sta_histogram': sta_per_chan,
        }
        self._observation_ready.set()

    def track(self, deauth=False, assoc=False, handshake=False, hop=False, sleep=False, miss=False, inc=1):
        if deauth:
            self.num_deauths += inc
            self.did_deauth = True
            self.any_activity = True

        if assoc:
            self.num_assocs += inc
            self.did_associate = True
            self.any_activity = True

        if miss:
            self.num_missed += inc

        if hop:
            self.num_hops += inc
            # these two are used in order to determine the sleep time in seconds
            # before switching to a new channel ... if nothing happened so far
            # during this loop on the current channel, we will sleep less
            self.did_deauth = False
            self.did_associate = False

        if handshake:
            self.num_shakes += inc
            self.did_handshakes = True

        if sleep:
            self.num_slept += inc

    def next(self):
        if self.any_activity is False and self.did_handshakes is False:
            self.inactive_for += 1
            self.active_for = 0
        else:
            self.active_for += 1
            self.inactive_for = 0

        now = time.time()
     

        self.loop_duration = now - self.loop_started

        # cache the state of this loop for other threads to read
        self._loop_data = {
            'duration_secs': self.loop_duration,
            'slept_for_secs': self.num_slept,
            'blind_for_loops': self.blind_for,
            'inactive_for_loops': self.inactive_for,
            'active_for_loops': self.active_for,
            'missed_encounters': self.num_missed,
            'num_hops': self.num_hops,
            'num_deauths': self.num_deauths,
            'num_associations': self.num_assocs,
            'num_handshakes': self.num_shakes,
        }

        self._loop_data['reward'] = self._reward(self.loop + 1, self._loop_data)
        self._loop_data_ready.set()

        logging.info("[loop %d] duration=%s slept_for=%s blind=%d inactive=%d active=%d hops=%d missed=%d deauths=%d assocs=%d handshakes=%d  "
                     "reward=%s" % (
                         self.loop,
                         utils.secs_to_hhmmss(self.loop_duration),
                         utils.secs_to_hhmmss(self.num_slept),
                         self.blind_for,
                         self.inactive_for,
                         self.active_for,
                         self.num_hops,
                         self.num_missed,
                         self.num_deauths,
                         self.num_assocs,
                         self.num_shakes,
                        
                         self._loop_data['reward']))

        self.loop += 1
        self.loop_started = now
        self.did_deauth = False
        self.num_deauths = 0
        self.did_associate = False
        self.num_assocs = 0
        self.num_missed = 0
        self.did_handshakes = False
        self.num_shakes = 0
        self.num_hops = 0
        self.num_slept = 0
        self.any_activity = False
