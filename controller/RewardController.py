from config import RewardMode, Epsilon, Config
import random
from functions import logging

class RewardController:

    def __init__(self, traffic_type):

        self.reward_latency = 0
        self. reward_bandwidth = 0
        self.reward_packetloss = 0
        self.total_reward = 0
        self.type_of_traffic= traffic_type

        
        weight_type=Config.WeightReward[traffic_type]
        self.weight_latency = weight_type['lat']
        self.weight_bandwidth = weight_type['lat']
        self.weight_packetloss = weight_type['lat']



    """
    Calls the correct reward function based on the reward mode 
    @param reward_mode
    @param dict_measureent    
    @return:
    """
    def get_reward(self,reward_mode, dict_measurement):  
               
        if reward_mode == RewardMode.ONLY_LAT.value:
            self.reward_latency = Latency(dict_measurement).calculateReward()                    
        elif reward_mode == RewardMode.LAT_UTILISATION.value:
            self.reward_latency = Latency(dict_measurement).calculateReward()
            self.reward_bandwidth = Bandwidth(dict_measurement).calculateReward()
        elif reward_mode == RewardMode.COMBINED.value:
            self.reward_latency = Latency(dict_measurement) .calculateReward()
            self.reward_bandwidth = Bandwidth(dict_measurement).calculateReward()
            self.reward_packetloss = PacketLoss(dict_measurement) .calculateReward()
        
        return self.reward_latency, self.reward_bandwidth, self.reward_packetloss
    """
    Calculates total reward function based on the reward and their repective weights         
    @return:
    """
    def get_total_reward(self,reward_mode, dict_measurement):  
        
        self.get_reward(reward_mode, dict_measurement)
        total_reward = (self.weight_latency * self.reward_latency) + (self.weight_bandwidth * self.reward_bandwidth) + (self.weight_packetloss * self.reward_packetloss)
        # total_reward = (self.weight_latency * self.reward_latency) + (self.weight_packetloss * self.reward_packetloss)
        dict_return_rewards={'total_reward': total_reward, 'reward_latency':self.reward_latency, 'reward_bandwidth': self.reward_bandwidth, 'reward_packetloss':self.reward_packetloss}
        
        
        return dict_return_rewards


class Latency:

    def __init__(self, dict_measurement):
        self.l_max = dict_measurement['latency_max']
        self.l_flow = dict_measurement['latency_flow']
        self.epsilon = Epsilon.EPSILON_LATENCY

    def calculateReward(self):
        if self.l_flow < self.l_max:
           return abs(self.l_max - self.l_flow)/self.l_max
        elif self.l_max < self.l_flow < 2*(self.l_max):
            return -abs(self.l_max - self.l_flow)/self.l_max
        elif self.l_flow >= 2*(self.l_max):
            return -1
        elif self.l_flow == self.l_max:
            return self.epsilon
    
class Bandwidth:

    def __init__(self, dict_measurement):
        self.b_min = dict_measurement['bandwidth_min']
        self.b_flow = dict_measurement['bandwidth_flow']
        self.epsilon = Epsilon.EPSILON_BANDWIDTH

    def calculateReward(self):
        logging("self.b_flow", self.b_flow)
        logging("self.b_min", self.b_min)
        if self.b_flow >= 2*(self.b_min):
           return 1
        elif self.b_min < self.b_flow < 2*(self.b_min):
            return abs(self.b_min - self.b_flow)/self.b_min
        elif self.b_flow < self.b_min:
            return -abs(self.b_min - self.b_flow)/self.b_min
        elif self.b_flow == self.b_min:
            return self.epsilon

class PacketLoss:

    def __init__(self, dict_measurement):
        self.pl_max = dict_measurement['packetloss_max']
        self.pl_flow = dict_measurement['packetloss_flow']
        self.epsilon = Epsilon.EPSILON_PACKETLOSS

    def calculateReward(self):
        if self.pl_flow < self.pl_max:
           return abs(self.pl_max - self.pl_flow)/self.pl_max
        elif self.pl_max < self.pl_flow < 2*(self.pl_max):
            return -abs(self.pl_max - self.pl_flow)/self.pl_max
        elif self.pl_flow >= 2*(self.pl_max):
            return -1
        elif self.pl_flow == self.pl_max:
            return self.epsilon

