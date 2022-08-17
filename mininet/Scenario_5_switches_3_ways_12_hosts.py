from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSController
from mininet.node import CPULimitedHost, Host, Node
from mininet.node import OVSKernelSwitch, UserSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink, Intf
from _thread import start_new_thread
import os, stat
import json
import time
import csv
import requests
import sys
import math
sys.path.append("...")
sys.path.append("..")
sys.path.append("../controller")
sys.path.append(".")
print(os.getcwd())
print(sys.path.__str__())
from config import Config


#               s2
#  h11   10ms/     \10ms   h51
#     --   s1--s4--s5 --
#  h16    14ms\    /14ms   h56
#               s3

###################################################################
############### Scenario - 12 Hosts    ############################
###################################################################

def reset_load_level(loadLevel):
    requests.put('http://0.0.0.0:8080/simpleswitch/params/load_level', data=json.dumps({"load_level": loadLevel}))
    requests.put('http://0.0.0.0:8080/simpleswitch/params/reset_flag', data=json.dumps({"reset_flag": True}))

def reset_iteration(iteration):
    requests.put('http://0.0.0.0:8080/simpleswitch/params/iteration', data=json.dumps({"iteration": iteration}))
    requests.put('http://0.0.0.0:8080/simpleswitch/params/iteration_flag', data=json.dumps({"iteration_flag": True}))

def stop_controller():
    requests.put('http://0.0.0.0:8080/simpleswitch/params/stop_flag', data=json.dumps({"stop_flag": True}))

def startIperf(host1, host2, amount, port, timeTotal, loadLevel):
    #host2.cmd("iperf -s -u -p {} &".format(port))
    bw = float(amount) * (float(loadLevel) / float(10))
    print("Host {} to Host {} Bw: {}".format(host1.name, host2.name, bw))
    command = "iperf -c {} -u -p {} -t {} -b {}M &".format(host2.IP(), port, timeTotal, bw)
    host1.cmd(command)

def write_in_File(fileName, logs, loadlevel, iteration_split_up_flag, iteration):
    dir = logs + '/'
    if iteration_split_up_flag:
        dir = dir + str(iteration) + '/'
    with open('{}{}.csv'.format(dir, fileName), 'a') as csvfile:
        fileWriter = csv.writer(csvfile, delimiter=',')
        fileWriter.writerow([loadlevel, time.time()])

def clearingSaveFile(fileName, logs):
    dir = logs + '/'
    with open('{}{}.csv'.format(dir, fileName), 'w') as file:
        file.write("# loadlevel, timestamp \n")

def clearing_save_file_iterations(fileName, logs, iterations):
    # cleans it all up
    for iteration in range(iterations):
        dir = logs + '/' + str(iteration) + '/'
        if not os.path.exists(dir):
            os.makedirs(dir)
            # give folder rights
            os.chmod(dir, stat.S_IRWXO)
            os.chmod(dir, 777)
            os.chmod('{}{}.csv'.format(dir, fileName), 777)
        with open('{}{}.csv'.format(dir, fileName), 'w') as file:
            file.write("# loadlevel, timestamp \n")

def min_to_sec(min):
    return min * 60

def four_switches_network():
    net = Mininet(topo=None,
                  build=False,
                  ipBase='10.0.0.0/8', link=TCLink)

    queue_lenght = Config.queue_lenght

    bw_max_dict = Config.bw_max_dict

    # linkarray
    linkArray = []
    split_up_load_levels_flag = Config.split_up_load_levels_flag
    logs = Config.log_path
    # importante! the load levels for measurements
    loadLevels = Config.load_levels
    print("LoadLevel: {}".format(loadLevels))
    timeTotal = min_to_sec(Config.duration_iperf_per_load_level_minutes)
    controllerIP = '127.0.0.1'
    fileName = 'timestamp_changing_load_levels_mininet'
    info('*** Adding controller\n')
    c0 = net.addController(name='c0',
                           controller=RemoteController,
                           ip=controllerIP,
                           protocol='tcp',
                           port=6633)


    info('*** Add switches\n')
    s1 = net.addSwitch('s1', cls=OVSKernelSwitch)
    s2 = net.addSwitch('s2', cls=OVSKernelSwitch)
    s3 = net.addSwitch('s3', cls=OVSKernelSwitch)
    s4 = net.addSwitch('s4', cls=OVSKernelSwitch)
    s5 = net.addSwitch('s5', cls=OVSKernelSwitch)

    info( '*** Add hosts\n')
    h11 = net.addHost('h11', cls=Host, ip='10.0.0.11', defaultRoute=None)
    h12 = net.addHost('h12', cls=Host, ip='10.0.0.12', defaultRoute=None)
    h13 = net.addHost('h13', cls=Host, ip='10.0.0.13', defaultRoute=None)
    h14 = net.addHost('h14', cls=Host, ip='10.0.0.14', defaultRoute=None)
    h15 = net.addHost('h15', cls=Host, ip='10.0.0.15', defaultRoute=None)
    h16 = net.addHost('h16', cls=Host, ip='10.0.0.16', defaultRoute=None)

    h51 = net.addHost('h51', cls=Host, ip='10.0.0.51', defaultRoute=None)
    h52 = net.addHost('h52', cls=Host, ip='10.0.0.52', defaultRoute=None)
    h53 = net.addHost('h53', cls=Host, ip='10.0.0.53', defaultRoute=None)
    h54 = net.addHost('h54', cls=Host, ip='10.0.0.54', defaultRoute=None)
    h55 = net.addHost('h55', cls=Host, ip='10.0.0.55', defaultRoute=None)
    h56 = net.addHost('h56', cls=Host, ip='10.0.0.56', defaultRoute=None)

    

    info('*** Add links\n')
    # linkArray.append(net.addLink(s1, s2, delay='9ms',use_tbf = True, bw=20, max_queue_size=queue_lenght, latency_ms = 10000000, burst = 1000000))
    # linkArray.append(net.addLink(s2, s5, delay='9ms',use_tbf = True, bw=20, max_queue_size=queue_lenght, latency_ms = 10000000, burst = 1000000))
    # linkArray.append(net.addLink(s1, s3, delay='9ms',use_tbf = True, bw=10, max_queue_size=queue_lenght, latency_ms = 10000000, burst = 1000000))
    # linkArray.append(net.addLink(s3, s5, delay='9ms',use_tbf = True, bw=10, max_queue_size=queue_lenght, latency_ms = 10000000, burst = 1000000))
    # linkArray.append(net.addLink(s1, s4, delay='30ms',use_tbf = True, bw=5, max_queue_size=queue_lenght, latency_ms = 10000000, burst = 1000000))
    # linkArray.append(net.addLink(s4, s5, delay='30ms',use_tbf = True, bw=5, max_queue_size=queue_lenght, latency_ms = 10000000, burst = 1000000))


    linkArray.append(net.addLink(s1, s2, delay='3ms',use_tbf = True, bw=4, max_queue_size=queue_lenght, latency_ms = 10000000, burst = 1000000))
    linkArray.append(net.addLink(s2, s5, delay='3ms',use_tbf = True, bw=4, max_queue_size=queue_lenght, latency_ms = 10000000, burst = 1000000))
    linkArray.append(net.addLink(s1, s3, delay='3ms',use_tbf = True, bw=3, max_queue_size=queue_lenght, latency_ms = 10000000, burst = 1000000))
    linkArray.append(net.addLink(s3, s5, delay='3ms',use_tbf = True, bw=3, max_queue_size=queue_lenght, latency_ms = 10000000, burst = 1000000))
    linkArray.append(net.addLink(s1, s4, delay='10ms',use_tbf = True, bw=2, max_queue_size=queue_lenght, latency_ms = 10000000, burst = 1000000))
    linkArray.append(net.addLink(s4, s5, delay='10ms',use_tbf = True, bw=2, max_queue_size=queue_lenght, latency_ms = 10000000, burst = 1000000))




    
    net.addLink(h11, s1)
    net.addLink(h12, s1)
    net.addLink(h13, s1)
    net.addLink(h14, s1)
    net.addLink(h15, s1)
    net.addLink(h16, s1)

    net.addLink(h51, s5)
    net.addLink(h52, s5)
    net.addLink(h53, s5)
    net.addLink(h54, s5)
    net.addLink(h55, s5)
    net.addLink(h56, s5)

    info('*** Starting network\n')
    net.build()
    info('*** Starting controllers\n')
    for controller in net.controllers:
        controller.start()

    info('*** Starting switches\n')
    net.get('s1').start([c0])
    net.get('s2').start([c0])
    net.get('s3').start([c0])
    net.get('s4').start([c0])
    net.get('s5').start([c0])


    iterations = Config.iterations
    if iterations > 1:
        iteration_split_up_flag = True
    else:
        iteration_split_up_flag = False

    # erasing previous file
    if not split_up_load_levels_flag:
        if iteration_split_up_flag:
            clearing_save_file_iterations(fileName, logs, iterations)
        else:
            clearingSaveFile(fileName, logs)

    time.sleep(15)
    # incrementing the load
    for iteration in range(iterations):
        i = 0
        clearing_save_file_iterations(fileName, logs, iterations)
        for loadLevel in loadLevels:
            # iperf threads
            # if the load levels are not split up -> write the load level change
            if split_up_load_levels_flag:
                reset_load_level(loadLevel)
            if not split_up_load_levels_flag:
                write_in_File(fileName, logs, loadLevel, iteration_split_up_flag, iteration)
            # send load level
            print("(Re)starting iperf -- loadLevel:  {}".format(loadLevel))
            start_new_thread(startIperf, (h11, h51, 3.75, 5001, timeTotal, loadLevel))
            start_new_thread(startIperf, (h12, h52, 2.75, 5001, timeTotal, loadLevel))
            start_new_thread(startIperf, (h13, h53, 2.75, 5001, timeTotal, loadLevel))
            # start_new_thread(startIperf, (h14, h54, 1.75, 5001, timeTotal, loadLevel)) # change
            # start_new_thread(startIperf, (h15, h55, 1.75, 5001, timeTotal, loadLevel)) # change
            # start_new_thread(startIperf, (h16, h56, 1.75, 5001, timeTotal, loadLevel)) # change
            i = i + 1
            time.sleep(timeTotal)
            # waiting additional 2 sec to reset states
            if Config.wait_between_load_lavel_change:
                time.sleep(Config.waiting_time)

        # last load level past
        if not split_up_load_levels_flag:
            write_in_File(fileName, logs, -1, iteration_split_up_flag, iteration)
        if iteration_split_up_flag and iteration < iterations - 1:
            reset_iteration(iteration + 1)
            time.sleep(1)
    stop_controller()
    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')

four_switches_network()
