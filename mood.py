import logging
from a2c.loop import loop

# basic mood system
class Automata(object):
    def __init__(self, config, view):
        self._config = config                
        self._view = view                    
        self._loop = Loop(config)   #initializer

    def set_starting(self):
        self._view.on_starting()   
    
    def in_good_mood(self):
        return self._has_support_network_for(1.0) 

    def set_excited(self):
        logging.warning("%d loops with activity -> excited", self._loop.active_for)
        self._view.on_excited()

    def any_activity(self):
        return self._loop.any_activity

    def wait_for(self, t, sleeping=True):
        self._view.wait(t, sleeping)
        self._loop.track(sleep=True, inc=t)

    def _on_miss(self, who):
        logging.info("it looks like %s is not in range anymore :/", who)
        self._loop.track(miss=True)
        self._view.on_miss(who)

    def _on_error(self, who, e):
        # when we're trying to associate or deauth something that is not in range anymore
        # (if we are moving), we get the following error from bettercap:
        # error 400: 50:c7:bf:2e:d3:37 is an unknown BSSID or it is in the association skip list.
        if 'is an unknown BSSID' in str(e):
            self._on_miss(who)
        else:
            logging.error(e)

    def is_stale(self):
        return self._loop.num_missed > self._config['personality']['max_misses_for_recon']

    def next_loop(self):
        logging.debug("agent.next_loop()")

        was_stale = self.is_stale()
        did_miss = self._loop.num_missed

        self._loop.next()

    def set_angry(self, factor):
        self._view.on_angry()

    def set_bored(self):
        factor = self._loop.inactive_for / self._config['personality']['bored_num_loops']
        logging.warning("%d loops with no activity -> bored", self._loop.inactive_for)
            self._view.on_bored()

        # after X misses during a loop, set the status to angry
        if was_stale:
            factor = did_miss / self._config['personality']['max_misses_for_recon']
            if factor >= 2.0:
                self.set_angry(factor)
           
        # after X times being bored, the status is set to sad or angry
        elif self._loop.inactive_for >= self._config['personality']['sad_num_loops']:
            factor = self._loop.inactive_for / self._config['personality']['sad_num_loops']
            if factor >= 2.0:
                self.set_angry(factor)
            else:
                self._view.on_sad()
        # after X times being inactive, the status is set to bored
        elif self._loop.inactive_for >= self._config['personality']['bored_num_loops']:
            self.set_bored()
        # after X times being active, the status is set to happy / excited
        elif self._loop.active_for >= self._config['personality']['excited_num_loops']:
            self.set_excited()
