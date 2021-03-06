#https://towardsdatascience.com/creating-a-custom-openai-gym-environment-for-stock-trading-be532be3910e
import logging
import gym
from gym import spaces
import numpy as np

import a2c.featurizer as featurizer
import a2c.reward as reward
from a2c.parameter import Parameter
#class CustomEnv(gym.Env):
# """Custom Environment that follows gym interface"""
#   metadata = {'render.modes': ['human']}
class Environment(gym.Env):
    metadata = {'render.modes': ['human']}
    params = [
        Parameter('min_rssi', min_value=-200, max_value=-50),#Received Signal Strength Indication
        Parameter('ap_ttl', min_value=30, max_value=600), #Access point time to live
        Parameter('sta_ttl', min_value=60, max_value=300),#client station time to live
      
        Parameter('recon_time', min_value=5, max_value=60),
        Parameter('max_inactive_scale', min_value=3, max_value=10),
        Parameter('recon_inactive_multiplier', min_value=1, max_value=3),
        Parameter('hop_recon_time', min_value=5, max_value=60),
        Parameter('min_recon_time', min_value=1, max_value=30),
        Parameter('max_interactions', min_value=1, max_value=25),
        Parameter('max_misses_for_recon', min_value=3, max_value=10),
        Parameter('excited_num_loops', min_value=5, max_value=30),
        Parameter('bored_num_loops', min_value=5, max_value=30),
        Parameter('sad_num_loops', min_value=5, max_value=30), #creature parameters
    ] 
#def __init__(self, arg1, arg2, ...):
#super(CustomEnv, self).__init__()
    
    def __init__(self, agent, loop):
        super(Environment, self).__init__()
        self._agent = agent
        self._loop = loop
        self._loop_num = 0
        self._loop_render = None
        
        self._supported_channels = agent.supported_channels()  #agent.py
        self._extended_spectrum = any(ch > 140 for ch in self._supported_channels) #in case of 5Ghz aps
        self._histogram_size, self._observation_shape = featurizer.describe(self._extended_spectrum) #featurizer.py

        Environment.params += [
            Parameter('_channel_%d' % ch, min_value=0, max_value=1, meta=ch + 1) for ch in
            range(self._histogram_size) if ch + 1 in self._supported_channels
        ] #adding parameters for 5Ghz aps
        #https://hackernoon.com/intuitive-rl-intro-to-advantage-actor-critic-a2c-4ff545978752
        self.last = {
            'reward': 0.0,
            'observation': None,
            'policy': None,
            'params': {},
            'state': None,
            'state_v': None
        } #for the last loop
## Define action and observation space
## They must be gym.spaces objects
   self.action_space = spaces.MultiDiscrete([p.space_size() for p in Environment.params if p.trainable])
    #- The multi-discrete action space consists of a series of discrete action spaces with different number of actions in eachs
    #- It is parametrized by passing an array of positive integers specifying number of actions for each discrete action space in this case p~params variable
        self.observation_space = spaces.Box(low=0, high=1, shape=self._observation_shape, dtype=np.float32)
        self.reward_range = reward.range 
 @staticmethod
    def policy_size():
        return len(list(p for p in Environment.params if p.trainable)) # returns length of parameters which are in environment and are set to change by train.py 

    @staticmethod
    #ai policy is set during training and is passed to the environment

    def policy_to_params(policy):
        num = len(policy)
        params = {}
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
# def step(self, action):
    # Execute one time step within the environment
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
#def reset(self):
    # Reset the state of the environment to an initial state    
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
#def render(self, mode='human', close=False):
    # Render the environment to the screen
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
