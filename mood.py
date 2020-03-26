

class Automata(object)
     def __init__(self,config);
     self._config = config
     self._loop = loop(config)
    
    def _on_miss(self, who):
        logging.info("it looks like %s is not in range anymore :/", who)
        
    def _on_error(self, who, e):
    # when we're trying to associate or deauth something that is not in range anymore
    # (if we are moving), we get the following error from bettercap:
    # error 400: 50:c7:bf:2e:d3:37 is an unknown BSSID or it is in the association skip list.
     if 'is an unknown BSSID' in str(e):
            self._on_miss(who)
        else:
            logging.error(e)
