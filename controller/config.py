"""
   config values for learning
"""
from enum import Enum
import math
# Added by Hamed June 23, for adding BW and Latency theoretical values
import json


class QMode(Enum):
    SHORTEST_PATH = -1
    MULTI_ARMED_BANDIT_NO_WEIGHT = 1
    MULTI_ARMED_BANDIT_WITH_WEIGHT = 2
    Q_LEARNING = 3
    SARSA = 4
    TD_ZERO = 5


class ExplorationMode(Enum):
    CONSTANT_EPS = 0
    FALLING_EPS = 1
    SOFTMAX = 2
    UCB = 3


class BiasRL(Enum):
    SPF = 1
    RANDOM = 2


class ActionMode(Enum):
    ONE_FLOW = 1
    DIRECT_CHANGE = 2


class RewardMode(Enum):
    ONLY_LAT = 1
    LAT_UTILISATION = 2
    COMBINED = 3

"""Added by Maria 7/18/2022 for setting the epsilon values"""
class Epsilon(Enum):
    EPSILON_LATENCY = 0.005
    EPSILON_BANDWIDTH = 0.005
    EPSILON_PACKETLOSS = 0.005

"""Added by Maria 7/18/2022 for setting the weights for reward"""
# class WeightReward(Enum):
#     WEIGHT_LATENCY = 1
#     WEIGHT_BANDWIDTH = 1
#     WEIGHT_PACKETLOSS = 1

"""Added by Maria 7/27/2022 for setting the theoretical values for reward"""
class TrafficType():
    # latency values are in ms
    LATENCY_INTENSIVE = {'lat':20, 'bw':2000000, 'plr':0.08 }
    # BW values in BPS
    BANDWIDTH_INTENSIVE = {'lat':40, 'bw':3000000, 'plr':0.08 }
    PACKETLOSS_INTENSIVE = {'lat':40, 'bw':2000000, 'plr':0.02 }

class Config(object):
    ################### Learning ########################
    qMode = QMode.Q_LEARNING
    # qMode = QMode.SHORTEST_PATH
    alpha = 0.8
    gamma = 0.8
    epsilon = 0.05
    temperature = 0.00005
    # for UCB
    exploration_degree = 30

    # how long to wait until starting to gather new rewards
    delay_reward = 2

    # how many rewards are gathred before considering taking a new action
    measurements_for_reward = 1

    # duration to stay in one load level by iperf
    duration_iperf_per_load_level_minutes = 10

    # load level
    # load_levels = [10, 10]
    load_levels = [10]

    # number of iterations per measurement
    iterations = 30

    # init_value for softmax
    softmax_init_value = - 140
    # - float('inf')

    # Scaling amount
    scaling_amount = 4

    #
    exploration_mode = ExplorationMode.SOFTMAX

    # action mode
    action_mode = ActionMode.DIRECT_CHANGE

    # if LoadLevel Test Case
    reset_Q_test_flag = True

    # splitting up - each load level different log file
    split_up_load_levels_flag = True

    # if merging QTables when new flow joins
    merging_q_table_flag = False

    wait_between_load_lavel_change = False
    waiting_time = 0.5
    # if initialise with shortest path first or with a random selected path
    bias = BiasRL.RANDOM

    # where to save the logs
    log_path = '../logs'

    # how many rewards sould be taken until building an average for the saved reward
    savingRewardCounter = 1

    # style of reward
    # reward_mode = RewardMode.ONLY_LAT
    # reward_mode = RewardMode.LAT_UTILISATION
    #Added By Maria July 27, 2022 for new reward function
    reward_mode = RewardMode.COMBINED
    
    WeightReward={
        'embb': {
            'lat': 0.2,
            'bw': 0.6,
            'plr': 0.2
        },
        'urllc': {
            'lat': 0.45,
            'bw': 0.1,
            'plr': 0.45
        },
        'mmtc': {
            'lat': 0.34,
            'bw': 0.33,
            'plr': 0.33
        }
    }




    ################### Remote Controller ########################

    # update interval latency in seconds
    interval_update_latency = 1

    # sending to leanring module interval in seconds
    interval_communication_processes = 1

    # update interval flow and port statictics
    interval_controller_switch_latency = 0.5

    # maximum amount of possible paths
    max_possible_paths = 50
    # q array
    Q_array_path = "Q_array.json"
    number_of_actions = 9477

    ################## Mininet #########################

    # queue lenght
    queue_lenght = 30
    # size (bytes) packet iperf udp
    # size_iperf_pkt_bytes = 100
    # bandwith, in Mbit/s
    bw_max_dict = {1: {2: 4.0, 3: 3.0}, 2: {4: 4.0}, 3: {4: 3.0}}

    # Added by Hamed on June 23, 2022 - Links BW and Latency theoretical values
    # structure => srcid:{dstid:value} read from JSON file
    with open('../mininet/Scenario_Four_switches_two_ways_6_hosts.json') as json_file:
        data = json.load(json_file)

    bw_theoretical_dict=data["bw"]
    latency_theoretical_dict=data["lat"]
