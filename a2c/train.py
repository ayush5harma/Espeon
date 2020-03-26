import logging
import random
import threading

    def on_loop(self, data, training):
        best_r = False
        worst_r = False
        with self._lock:
            reward = data['reward']
            if reward < self.worst_reward:
                self.worst_reward = reward
                worst_r = True

            elif reward > self.best_reward:
                best_r = True
                self.best_reward = reward

            self.loops_lived += 1
            if training:
                self.loops_trained += 1

        self.save()
        
        if best_r:
            self._receiver.on_ai_best_reward(reward)
        elif worst_r:
            self._receiver.on_ai_worst_reward(reward)

    def load(self):

    def save(self):

class AsyncTrainer(object):

def set_training(self, training, for_loops=0):


    def is_training(self):
    def training_loops(self):
    def start_ai(self):
    def _save_ai(self):
    def on_ai_step(self):
        logging.info("[ai] saving model to %s ..." % self._nn_path)
    def on_ai_step(self):
        self._model.env.render() # gym environment renderer is called.

    
    def on_ai_policy(self, new_params):
        plugins.on('ai_policy', self, new_params)
        logging.info("[ai] setting new policy:")
        for name, value in new_params.items():
            if name in self._config['personality']:
                curr_value = self._config['personality'][name]
                if curr_value != value:
                    logging.info("[ai] ! %s: %s -> %s" % (name, curr_value, value))
                    self._config['personality'][name] = value
            else:
                logging.error("[ai] param %s not in personality configuration!" % name)
                
        self.run('set wifi.ap.ttl %d' % self._config['personality']['ap_ttl'])
        self.run('set wifi.sta.ttl %d' % self._config['personality']['sta_ttl'])
        self.run('set wifi.rssi.min %d' % self._config['personality']['min_rssi'])
        
    def on_ai_ready(self):
        

    def on_ai_best_reward(self, r):
        logging.info("[ai] best reward so far: %s" % r)
        

    def on_ai_worst_reward(self, r):
        logging.info("[ai] worst reward so far: %s" % r)
    
    def _ai_worker(self):
        self._model = ai.load(self._config, self, self._loop)

        if self._model:
            self.on_ai_ready()

            loops_per_episode = self._config['ai']['loops_per_episode']

            obs = None
            while True:
                self._model.env.render()
                # wheathe to renter in training mode or not
                if random.random() > self._config['ai']['laziness']:
                    logging.info("[ai] learning for %d loops ..." % loops_per_episode)
                    try:
                        self.set_training(True, loops_per_episode)
                        self._model.learn(total_timesteps=loops_per_episode, callback=self.on_ai_training_step)
                    except Exception as e:
                        logging.exception("[ai] error while training")
                    finally:
                        self.set_training(False)
                        obs = self._model.env.reset()
          # init the first time
                elif obs is None:
                    obs = self._model.env.reset()

                # run the inference
                action, _ = self._model.predict(obs)
                obs, _, _, _ = self._model.env.step(action)


