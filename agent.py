import json
import os
import re
import logging
import _thread

#from ui.web.server import Server //web-ui
from automata import Automata
from bettercap import Client
from a2c.train import AsyncTrainer

    def start_monitor_mode(self):
        mon_iface = self._config['main']['iface']
        mon_start_cmd = self._config['main']['mon_start_cmd']

        self.start_advertising()

    def _wait_bettercap(self):
        while True:
            try:
                s = self.session()
                return
            except:
                logging.info("waiting for bettercap API to be available ...")
                time.sleep(1)

    def start(self):
        self.start_ai()
        self._wait_bettercap()
        self.setup_events()
        self.set_starting()
        self.start_monitor_mode()
        self.start_event_polling()
        self.next_loop()
        self.set_ready()

    def set_access_points(self, aps):
        self._access_points = aps
        return self._access_points

    def get_access_points(self):
        aps = []
        try:
            s = self.session()
            for ap in s['wifi']['aps']:
                if ap['encryption'] == '' or ap['encryption'] == 'OPEN':
                    continue
                        aps.append(ap)
        except Exception as e:
            logging.exception("error")

        aps.sort(key=lambda ap: ap['channel'])
        return self.set_access_points(aps)

    def get_total_aps(self):
        return self._tot_aps

    def get_aps_on_channel(self):
        return self._aps_on_channel

    def get_current_channel(self):
        return self._current_channel

    def get_access_points_by_channel(self):
        aps = self.get_access_points()
        channels = self._config['personality']['channels']
        grouped = {}

        # group by channel
        for ap in aps:
            ch = ap['channel']
            # if we're sticking to a channel, skip anything
            # which is not on that channel
            if channels and ch not in channels:
                continue

            if ch not in grouped:
                grouped[ch] = [ap]
            else:
                grouped[ch].append(ap)

        # sort by more populated channels
        return sorted(grouped.items(), key=lambda kv: len(kv[1]), reverse=True)

    def _find_ap_sta_in(self, station_mac, ap_mac, session):
        for ap in session['wifi']['aps']:
            if ap['mac'] == ap_mac:
                for sta in ap['clients']:
                    if sta['mac'] == station_mac:
                        return (ap, sta)
                return (ap, {'mac': station_mac, 'vendor': ''})
        return None
    def _update_counters(self):
        self._tot_aps = len(self._access_points)
        tot_stas = sum(len(ap['clients']) for ap in self._access_points)
        if self._current_channel == 0:
            self._view.set('aps', '%d' % self._tot_aps)
            self._view.set('sta', '%d' % tot_stas)
        else:
            self._aps_on_channel = len([ap for ap in self._access_points if ap['channel'] == self._current_channel])
            stas_on_channel = sum(
                [len(ap['clients']) for ap in self._access_points if ap['channel'] == self._current_channel])
            self._view.set('aps', '%d (%d)' % (self._aps_on_channel, self._tot_aps))
            self._view.set('sta', '%d (%d)' % (stas_on_channel, tot_stas))

    def _update_handshakes(self, new_shakes=0):
        if new_shakes > 0:
            self._loop.track(handshake=True, inc=new_shakes)

        tot = utils.total_unique_handshakes(self._config['bettercap']['handshakes'])
        txt = '%d (%d)' % (len(self._handshakes), tot)

        if self._last_cap is not None:
            txt += ' [%s]' % self._last_cap[:20]

        self._view.set('shakes', txt)

        if new_shakes > 0:
            self._view.on_handshakes(new_shakes)


            def _event_poller(self):
        self.run('events.clear')

        while True:
            time.sleep(1)

            new_shakes = 0

            logging.debug("polling events ...")

            try:
                s = self.session()
                self._update_uptime(s)
                self._update_counters()

                for h in [e for e in self.events() if e['tag'] == 'wifi.client.handshake']:
                    filename = h['data']['file']
                    sta_mac = h['data']['station']
                    ap_mac = h['data']['ap']
                    key = "%s -> %s" % (sta_mac, ap_mac)

                    if key not in self._handshakes:
                        self._handshakes[key] = h
                        new_shakes += 1
                        ap_and_station = self._find_ap_sta_in(sta_mac, ap_mac, s)
                        if ap_and_station is None:
                            logging.warning("!!! captured new handshake: %s !!!", key)
                            self._last_cap = ap_mac
                        else:
                            (ap, sta) = ap_and_station
                            self._last_cap = ap['hostname'] if ap['hostname'] != '' and ap[
                                'hostname'] != '<hidden>' else ap_mac
                            logging.warning(
                                "!!! captured new handshake on channel %d, %d dBm: %s (%s) -> %s [%s (%s)] !!!",
                                    ap['channel'],
                                    ap['rssi'],
                                    sta['mac'], sta['vendor'],
                                    ap['hostname'], ap['mac'], ap['vendor'])
                            plugins.on('handshake', self, filename, ap, sta)

            except Exception as e:
                logging.error("error: %s", e)

            finally:
                self._update_handshakes(new_shakes)
                
                
