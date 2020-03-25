import logging
import gym
from gym import spaces
import numpy as np

import featurizer as featurizer
import reward as reward
from parameter import Parameter


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

   