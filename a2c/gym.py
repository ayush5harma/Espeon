import logging
import gym
from gym import spaces
import numpy as np

import a2c.featurizer as featurizer
import a2c.reward as reward
from a2c.parameter import Parameter


class Environment(gym.Env):
    metadata = {'render.modes': ['human']} 
    params = [
        Parameter('min_rssi', min_value=-200, max_value=-50),
        Parameter('ap_ttl', min_value=30, max_value=600),
        Parameter('sta_ttl', min_value=60, max_value=300),

        Parameter('recon_time', min_value=5, max_value=60),
        Parameter('max_inactive_scale', min_value=3, max_value=10),
        Parameter('recon_inactive_multiplier', min_value=1, max_value=3),
        Parameter('hop_recon_time', min_value=5, max_value=60),
        Parameter('min_recon_time', min_value=1, max_value=30),
        Parameter('max_interactions', min_value=1, max_value=25),
        Parameter('max_misses_for_recon', min_value=3, max_value=10),
        Parameter('excited_num_epochs', min_value=5, max_value=30),
        Parameter('bored_num_epochs', min_value=5, max_value=30),
        Parameter('sad_num_epochs', min_value=5, max_value=30),
    ]

    #https://hackernoon.com/intuitive-rl-intro-to-advantage-actor-critic-a2c-4ff545978752
    Environment.params += [
            Parameter('_channel_%d' % ch, min_value=0, max_value=1, meta=ch + 1) for ch in
            range(self._histogram_size) if ch + 1 in self._supported_channels
        ]

        self.last = {
            'reward': 0.0,
            'observation': None,
            'policy': None,
            'params': {},
            'state': None,
            'state_v': None
        }

   self.action_space = spaces.MultiDiscrete([p.space_size() for p in Environment.params if p.trainable])
        self.observation_space = spaces.Box(low=0, high=1, shape=self._observation_shape, dtype=np.float32)
        self.reward_range = reward.range

 @staticmethod
    def policy_size():
        return len(list(p for p in Environment.params if p.trainable))

    @staticmethod
    def policy_to_params(policy):
        num = len(policy)
        params = {}

        assert len(Environment.params) == num

        channels = []

        for i in range(num):
            param = Environment.params[i]

            if '_channel' not in param.name:
                params[param.name] = param.to_param_value(policy[i])
            else:
                has_chan = param.to_param_value(policy[i])
                # print("%s policy:%s bool:%s" % (param.name, policy[i], has_chan))
                chan = param.meta
                if has_chan:
                    channels.append(chan)

        params['channels'] = channels

        return params
def _next_loop(self):
        logging.debug("[ai] waiting for loop to finish ...")
        return self._loop.wait_for_loop_data()

    def _apply_policy(self, policy):
        new_params = Environment.policy_to_params(policy)
        self.last['policy'] = policy
        self.last['params'] = new_params
        self._agent.on_ai_policy(new_params)

    def step(self, policy):
        # create the parameters from the policy and update
        # update them in the algorithm
        self._apply_policy(policy)
        self._loop_num += 1

        # wait for the algorithm to run with the new parameters
        state = self._next_loop()

        self.last['reward'] = state['reward']
        self.last['state'] = state
        self.last['state_v'] = featurizer.featurize(state, self._loop_num)

        self._agent.on_ai_step()

        return self.last['state_v'], self.last['reward'], not self._agent.is_training(), {}
    
    def reset(self):
        # logging.info("[ai] resetting environment ...")
        self._loop_num = 0
        state = self._next_loop()
        self.last['state'] = state
        self.last['state_v'] = featurizer.featurize(state, 1)
        return self.last['state_v']
    def _render_histogram(self, hist):
        for ch in range(self._histogram_size):
            if hist[ch]:
                logging.info("      CH %d: %s" % (ch + 1, hist[ch]))

    def render(self, mode='human', close=False, force=False):
        # when using a vectorialized environment, render gets called twice
        # avoid rendering the same data
        if self._last_render == self._loop_num:
            return

        if not self._agent.is_training() and not force:
            return

        self._last_render = self._loop_num

        logging.info("[ai] --- training loop %d/%d ---" % (self._loop_num, self._agent.training_loops()))
        logging.info("[ai] REWARD: %f" % self.last['reward'])

        logging.debug("[ai] policy: %s" % ', '.join("%s:%s" % (name, value) for name, value in self.last['params'].items()))

        logging.info("[ai] observation:")
        for name, value in self.last['state'].items():
            if 'histogram' in name:
                logging.info("    %s" % name.replace('_histogram', ''))
                self._render_histogram(value)
