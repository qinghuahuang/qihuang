__author__ = 'racheung'
import os
import re
import time
import DUT_EFR32

## WSK config
WSTK_CLI_port = "4901"
WSTK_DBG_port = "4902"
WSTK_DBG_Delimiter = "WSTK> "
CoEx1_IF_TYPE = "TELNET"
CoEx1_name = "CoEx1"
CoEx1_IP = "192.168.12.110"
#CoEx1_IP = "192.168.12.10"
CoEx1_COM = "COM7"
CoEx1_Baudrate = 115200
CoEx1_delimiter = "packet_src_dest_brd4151a_pta_master>"
Remote1_name = "Remote1"
Remote1_IP = "192.168.12.120"
#Remote1_IP = "192.168.12.20"
Remote1_delimiter = "packet_src_dest_brd4151a_pta_master>"
Network1_PANID = "0x1234" # unique PANID
Network1_pjoin = 60 # secs
Network1_payload = 75 # 75 is max value
Network1_interval = 95 #95 # ms
Network1_count = 105 # number of TX packets per trial
MAX_LEAVE_FORM_ATTEMPTS = 1
MAX_JOIN_ATTEMPTS = 20

#MAX_TEST_DURATION_MULTIPLE = 5
MAX_TEST_DURATION_MULTIPLE = 1
Network2_interval = 50 # ms
Network2_count = 100

ZIGBEE_PTA_OPTIONS_DEFAULT = 0x3D10 #old PTA options default
ZIGBEE_PTA_OPTIONS_LIST = [ZIGBEE_PTA_OPTIONS_DEFAULT]
##*********************************************************


ENABLE_COEX_CLI_LOG = 0
#ENABLE_COEX_CLI_LOG = 1

ENABLE_REMOTE_CLI_LOG = 0
#ENABLE_REMOTE_CLI_LOG = 1

#VERBOSE_TEST_RESULTS = 0
VERBOSE_TEST_RESULTS = 1

RESET_AT_START = 0
#RESET_AT_START = 1
################################################################################
## Start of helper functions
################################################################################
zb_coex_power = 13 # => -74dBm to Remote RX inputs
#zb_remote_power_list = [0 , 20]
#zb_remote_power_list = [9, 4, -1] # => -85dBm, -90dBm, and -95dBm to CoEx RX inputs
#zb_remote_power_list = [9] # => -85dBm to CoEx RX inputs
zb_remote_power_list = [3] # => -90dBm to CoEx RX inputs

###############################################################################
def setup_zigbee_PTA(reset, CoEx, Remote, pta_enable, pta_options):

    if reset:
        print "Resetting CoEx..."
        CoEx.dbg_query("target reset 1")
        CoEx.cli_query("plugin network-steering stop")
        CoEx.cli_query("network leave")
        print "Resetting Remote..."
        Remote.dbg_query("target reset 1")
        Remote.cli_query("plugin network-steering stop")
        Remote.cli_query("network leave")
    else:
        print "Insuring verbose on (even without reset)"
        #print "Resetting CoEx..."
        #CoEx.dbg_query("target reset 1")
        #time.sleep(1)
        #CoEx.cli_query("plugin network-steering stop")
        #print "Resetting Remote..."
        #Remote.dbg_query("target reset 1")
        #Remote.cli_query("plugin network-steering stop")
        CoEx.cli_query("debugprint all_on")
        Remote.cli_query("debugprint all_on")


    # hack for REQ/PRIORITY invert bug to insure no ZigBee traffic during halPtaSetState()
    print "CoEx network Leave..."
    CoEx.cli_query("network leave")
    print "Rmote network Leave..."
    Remote.cli_query("network leave")
    #time.sleep(1)

    if pta_enable[0]:
        print "Enabling CoEx PTA and options: " + hex(pta_options) + "..."
        #CoEx.cli_query("custom set-pta-options " + hex(pta_options))
        #CoEx.cli_query("custom set-pta-state 1")
        CoEx.cli_query("plugin coexistence set-pta-options " + hex(pta_options))
        CoEx.cli_query("plugin coexistence set-pta-state 1")
    else:
        print "Disabling CoEx PTA..."
        CoEx.cli_query("plugin coexistence set-pta-options " + hex(ZIGBEE_PTA_OPTIONS_DEFAULT))
        CoEx.cli_query("plugin coexistence set-pta-state 0")

    if pta_enable[1]:
        print "Enabling Remote PTA and options: " + hex(pta_options) + "..."
        Remote.cli_query("plugin coexistence set-pta-options " + hex(pta_options))
        Remote.cli_query("plugin coexistence set-pta-state 1")
    else:

        Remote.cli_query("plugin coexistence set-pta-options " + hex(ZIGBEE_PTA_OPTIONS_DEFAULT))
        Remote.cli_query("plugin coexistence set-pta-state 0")

###############################################################################
def leave_form_network(src, dest, channel, src_txpwr, dest_txpwr, panid, pjoin):
    print "leave_form_network..."
    for leave_form in range(1,MAX_LEAVE_FORM_ATTEMPTS+1,1):
        # shut down any existing network
        src.cli_query("network leave")
        dest.cli_query("network leave")
        #time.sleep(1)
        CoexNetwork = "DOWN"
        CoexnodeId = "0xFFFF"
        result = src.cli_query("plugin network-creator form 0 " + panid + " " + str(src_txpwr) + " " +str(channel) )
        print result
        # stime.sleep(1)
        regexResultcoex = re.search(r'.*EMBER_NETWORK_(.*) (0x.*)\r.*', result)
        if regexResultcoex:
            CoexNetwork = regexResultcoex.group(1)
            print "CoexNetwork: " + CoexNetwork
            CoexnodeId = regexResultcoex.group(2)
            print "CoexnodeId: " + CoexnodeId
        src.cli_query("plugin network-creator-security open-network " )

        # join from dest
        network = "DOWN"
        nodeId = "0xFFFF"
        for join in range(1, MAX_JOIN_ATTEMPTS+1, 1):
            #dest.cli_query("net join " + str(channel) + " " + str(dest_txpwr) + " " + panid)
            dest.cli_query("network leave " )
            dest.cli_query("reset " )
            time.sleep(10) #(20)
            result = dest.cli_query("")
            print result
            regexResult = re.search(r'.*EMBER_NETWORK_(.*) (0x.*)\r.*', result)
            if regexResult:
                network = regexResult.group(1)
                print "Remotenetwork: " + network
                nodeId = regexResult.group(2)
                print "RemotenodeId: " + nodeId
                print "plugin network-creator-security close-network"
                src.cli_query("plugin network-creator-security close-network")
                break
        #CoexNetwork = "DOWN"
        #CoexnodeId = "0xFFFF"
        if network == "UP":
            result = src.cli_query("plugin stack-diagnostics info")
            print "plugin stack-diagnostics info"
            print result
            break

    if network != "UP":
        print "Unable to form " + src.name + "/" + dest.name + " network after " \
              + str(MAX_LEAVE_FORM_ATTEMPTS) + " leave/form attempts with " \
              + str(MAX_LEAVE_FORM_ATTEMPTS*MAX_JOIN_ATTEMPTS) + " total join attempts!"
 #       exit(-1)

# return list has following indexes
# 0: network status
# 1: dest nodeId
# 2: required leave/form loops
# 3: required join attempts required to form network
# 4: src  nodeID

    return [network, nodeId, str(leave_form), str((leave_form-1)*MAX_JOIN_ATTEMPTS + join), CoexnodeId]

###############################################################################
def setup_throughput_test(src, nodeId, payload, interval, count):
    src.cli_query("plugin throughput set-destination " + nodeId)
    src.cli_query("debugprint all_off")
    src.cli_query("plugin throughput set-packet-size " + str(payload))
    src.cli_query("plugin throughput set-inflight 1 ")
    src.cli_query("plugin throughput set-aps-ack-off")
    src.cli_query("plugin throughput set-interval " + str(interval))
    src.cli_query("plugin throughput set-count " + str(count))
###############################################################################
def reduce_route_records(src, dest, remonodeId,CoexnodeID):
    # try to shut down "Route Record" packets
    src.cli_query("zcl global read 0 0")
    src.cli_query("send " + remonodeId + " 1 1")
    dest.cli_query("zcl global read 0 0")
    dest.cli_query("send " + CoexnodeID + " 1 1")

    src.cli_query("plugin concentrator stop")
    dest.cli_query("plugin concentrator stop")

###############################################################################
def get_throughput_test_results_backup(src, count, start, max_test_time_sec):

    stats = [1e4, count, 0, count, 0, 0, count, 0, 0, count, 0, -1.0, -1.0, -1.0, -1.0]

    #src.cli_query("custom verbose on")
    src.cli_query("debugprint all_on")
    while (time.time()-start) < max_test_time_sec:
        #result = src.cli_query("custom result") #plugin throughput print-result
        result = src.cli_query("plugin throughput print-result") #plugin throughput print-result
        print result
        regexResult = re.search(r'Test ended at (.*) ms: (.*) p.*, (.*) p.*\n.*sent: (.*) .*\n.*Failures: (.*) .*\n.*Ucast: (.*) .*\n.*Retry: (.*) .*\n.*Fail: (.*) .*\n.*Success: (.*) .*\n.*Retry: (.*) .*\n.*Fail: (.*) .*\n.*:(.*) .*\n.*:(.*) .*\n.*:(.*) .*\n.*:(.*) .*\n.*', result)
        if regexResult:
            stats[0] = int(regexResult.group(1))
            stats[1] = int(regexResult.group(2))
            stats[2] = int(regexResult.group(3))
            stats[3] = int(regexResult.group(4))
            stats[4] = int(regexResult.group(6))
            stats[5] = int(regexResult.group(7))
            stats[6] = int(regexResult.group(8))
            stats[7] = int(regexResult.group(9))
            stats[8] = int(regexResult.group(10))
            stats[9] = int(regexResult.group(11))
            stats[10] = int(regexResult.group(5)) # new CCA Failure count
            stats[11] = float(regexResult.group(12)) # new latency min(ms)
            stats[12] = float(regexResult.group(13)) # new latency max(ms)
            stats[13] = float(regexResult.group(14)) # new latency mean(ms)
            stats[14] = float(regexResult.group(15)) # new latency std(ms)
            break

    # make sure test is stopped, even if incomplete
    #src.cli_query("custom stop")
    src.cli_query("plugin throughput stop")

    if stats[0] == 1e6: # if test didn't finish, capture the partial results
        #result = src.cli_query("custom result")
        result = src.cli_query("plugin throughput print-result") #plugin throughput print-result
        print result
        regexResult = re.search(r'Test ended at (.*) ms: (.*) p.*, (.*) p.*\n.*sent: (.*) .*\n.*Failures: (.*) .*\n.*Ucast: (.*) .*\n.*Retry: (.*) .*\n.*Fail: (.*) .*\n.*Success: (.*) .*\n.*Retry: (.*) .*\n.*Fail: (.*) .*\n.*:(.*) .*\n.*:(.*) .*\n.*:(.*) .*\n.*:(.*) .*\n.*', result)
        if regexResult:
            stats[0] = int(regexResult.group(1))
            stats[1] = int(regexResult.group(2))
            stats[2] = int(regexResult.group(3))
            stats[3] = int(regexResult.group(4))
            stats[4] = int(regexResult.group(6))
            stats[5] = int(regexResult.group(7))
            stats[6] = int(regexResult.group(8))
            stats[7] = int(regexResult.group(9))
            stats[8] = int(regexResult.group(10))
            stats[9] = int(regexResult.group(11))
            stats[10] = int(regexResult.group(5)) # new CCA Failure count
            stats[11] = float(regexResult.group(12)) # new latency min(ms)
            stats[12] = float(regexResult.group(13)) # new latency max(ms)
            stats[13] = float(regexResult.group(14)) # new latency mean(ms)
            stats[14] = float(regexResult.group(15)) # new latency std(ms)

# return list has following indexes
# 0: duration
# 1: packets_sent
# 2: packets_received
# 3: messages_sent
# 4: mac_tx_ucast
# 5: mac_tx_ucast_retry
# 6: mac_tx_ucast_fail
# 7: aps_tx_ucast_success
# 8: aps_tx_ucast_retry
# 9: aps_tx_ucast_fail
#10: CCA_fail
#11: Latency min (ms)
#12: Latency max (ms)
#13: Latency mean(ms)
#14: Latency std (ms)
    return stats
###############################################################################
def get_throughput_test_results(src, count, start, max_test_time_sec):

    stats = [1e6, count, 0, count, 0, 0, count, 0, 0, count, 0, -1.0, -1.0, -1.0, -1.0]
    result_stats = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1.0, -1.0, -1.0, -1.0]
    counters_stats = [1e4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1.0, -1.0, -1.0, -1.0]

    #src.cli_query("custom verbose on")
    src.cli_query("debugprint all_on")
    while (time.time()-start) < max_test_time_sec:
        result_1 = src.cli_query("plugin throughput print-result")  # plugin throughput print-result
        result_2 = src.cli_query("plugin throughput print-counters")  # plugin throughput print-counters
        print result_1 + result_2
        print "________________________________________________________________"

    #src.cli_query("plugin throughput stop")
   # make sure test is stopped, even if incomplete
    if stats[0] == 1e6: # if test didn't finish, capture the partial results
        print "throughput stop start print result and counters......"

        result = src.cli_query("plugin throughput print-result")  # plugin throughput print-result
        print result
        result_t = result
        #print ("result_1:= %s" % result_1)
        result_2 = re.sub("\n", "", result_t, 0)
        print result_2
        regexResult_t= re.search(r'HROUGHPUT.*time(.*)ms.*messages:(.*)out of (.*)Pay.*Throughput:(.*) bit.*Throughput:(.*) bit.* time:(.*)ms.* time:(.*)ms.* time:(.*)ms.* time:(.*)ms',result_2)
        print ("regexResult_t= %s" % regexResult_t)

        time.sleep(0.5)
        result_r = src.cli_query("plugin throughput print-counters")  # plugin throughput print-counters
        print result_r
        regexResult_r = re.search(r'COUNTERS.*\n.*Failures: (.*).*\n.*Ucast: (.*).*\n.*Retry: (.*).*\n.*Fail: (.*).*\n.*Success: (.*).*\n.*Retry: (.*).*\n.*Fail: (.*)',result_r)
        print ("regexResult_r %s" % regexResult_r)
        if(regexResult_t and regexResult_r):
            result_stats[0] = int(regexResult_t.group(1))  # Total time
            #print ("Total time= %s" % result_stats[0])
            result_stats[1] = int(regexResult_t.group(2))  # recive
            #print "Recive= %s" % regexResult_t.group(2)
            result_stats[2] = int(regexResult_t.group(3))  # send
            #print "Send= %s" %regexResult_t.group(3)
            result_stats[3] = int(regexResult_t.group(4))  # Min packet send time
            #print "Payload Throughput= %s" % regexResult_t.group(4)
            result_stats[4] = int(regexResult_t.group(5))  # Min packet send time
            #print "Phy Throughput" + regexResult_t.group(5)
            result_stats[5] = int(regexResult_t.group(6))  # Max packet send time
            #print "Min Time" + regexResult_t.group(6)
            result_stats[6] = int(regexResult_t.group(7))  # Max packet send time
            #print "Max Time" + regexResult_t.group(7)
            result_stats[7] = int(regexResult_t.group(8))  # Avg Packet send time
            #print "Avg Time" + regexResult_t.group(8)
            result_stats[8] = int(regexResult_t.group(9))  # STD packet send time
            #print "STD time..." + regexResult_t.group(9)
            counters_stats[0] = int(regexResult_r.group(1))  # CCA Failures
            #print "CCA Failures " + regexResult_r.group(1)
            counters_stats[1] = int(regexResult_r.group(2))  # Mac Tx Ucast
            #print "Mac Tx Ucast " + regexResult_r.group(2)
            counters_stats[2] = int(regexResult_r.group(3))  # Mac Tx Ucast Retry
            #print "Mac Tx Ucast Retry " + regexResult_r.group(3)
            counters_stats[3] = int(regexResult_r.group(4))  # Mac Tx Ucast Fail
            #print "Mac Tx Ucast Fail " + regexResult_r.group(4)
            counters_stats[4] = int(regexResult_r.group(5))  # APS Tx Ucast Success
            #print "APS Tx Ucast Success " + regexResult_r.group(5)
            counters_stats[5] = int(regexResult_r.group(6))  # APS Tx Ucast Retry
            #print "APS Tx Ucast Retry " + regexResult_r.group(6)
            counters_stats[6] = int(regexResult_r.group(7))  # APS Tx Ucast Fail
            #print "APS TX Ucast Fail " + regexResult_r.group(7)
            stats[0] = result_stats[0]
            stats[1] = result_stats[2]
            stats[2] = result_stats[1]
            stats[3] = result_stats[1]
            stats[4] = counters_stats[1]
            stats[5] = counters_stats[2]
            stats[6] = counters_stats[3]
            stats[7] = counters_stats[4]
            stats[8] = counters_stats[5]
            stats[9] = counters_stats[6]
            stats[10] = counters_stats[0] # new CCA Failure count
            stats[11] = result_stats[5] # new latency min(ms)
            stats[12] = result_stats[6] # new latency max(ms)
            stats[13] = result_stats[7] # new latency mean(ms)
            stats[14] = result_stats[8] # new latency std(ms)
            print "++++++++++++++++++++++++++++++++++++++++++++++++"
            print ("stats[0]= %s" % stats[0])
            print "++++++++++++++++++++++++++++++++++++++++++++++++"
    src.cli_query("plugin throughput stop")
# return list has following indexes
# 0: duration
# 1: packets_sent
# 2: packets_received
# 3: messages_sent
# 4: mac_tx_ucast
# 5: mac_tx_ucast_retry
# 6: mac_tx_ucast_fail
# 7: aps_tx_ucast_success
# 8: aps_tx_ucast_retry
# 9: aps_tx_ucast_fail
#10: CCA_fail
#11: Latency min (ms)
#12: Latency max (ms)
#13: Latency mean(ms)
#14: Latency std (ms)
    return stats

###############################################################################
def get_throughput_test_results_rssi(src, count):
    stats = [count, 100, 100, 100.0, 0.0]

    #src.cli_query("custom verbose on")
    #src.cli_query("debugprint all_on")
    #result = src.cli_query("custom result-rssi")
    #if VERBOSE_TEST_RESULTS:
    #    print result
    #regexResult = re.search(r'Number of messages received: (.*) *\n.*:(.*) .*\n.*:(.*) .*\n.*:(.*) .*\n.*:(.*) .*\n.*', result)
    #if regexResult:
    #    stats[0] = int(regexResult.group(1))
    #    stats[1] = int(regexResult.group(2))
    #    stats[2] = int(regexResult.group(3))
    #    stats[3] = float(regexResult.group(4))
    #    stats[4] = float(regexResult.group(5))

# return list has following indexes
# 0: packets_received
# 1: min RSSI of packets received
# 2: max RSSI of packets received
# 3: mean RSSI of packets received
# 4: std RSSI of packets received
    return stats

###############################################################################
def get_throughput_test_results_counters(src):
    stats = [-1, -1, -1, -1, -1, -1]
    src.cli_query("debugprint all_on")
    result = src.cli_query("plugin coexistence result-counters")
    if VERBOSE_TEST_RESULTS:
        print result
    regexResult = re.search(r'PTA Lo Pri Req: (.*) *\n.*:(.*) .*\n.*:(.*) .*\n.*:(.*) .*\n.*:(.*) .*\n.*:(.*) .*\n.*', result)
    if regexResult:
        stats[0] = int(regexResult.group(1))
        stats[1] = int(regexResult.group(2))
        stats[2] = int(regexResult.group(3))
        stats[3] = int(regexResult.group(4))
        stats[4] = int(regexResult.group(5))
        stats[5] = int(regexResult.group(6))

# return list has following indexes
#0: PTA Req Low Priority counter
#1: PTA Req High Priority counter
#2: PTA Grant Denied Low Priority counter
#3: PTA Grant Denied High Priority counter
#4: PTA TX Abort Low Priority counter
#5: PTA TX Abort High Priority counter
    return stats

###############################################################################
def restart_route_records(src, dest):
    src.cli_query("plugin concentrator start")
    dest.cli_query("plugin concentrator start")

##############################################################################
def set_zb_pwm(src, pwm_period, pwm_dutycycle, priority):
    print "set pwm period=%dms"%(pwm_period)+", dutycycle=%d%%"%(pwm_dutycycle)
    cmd = "plugin coexistence set-pwm-state %d %d %d 0"%(pwm_period*2, pwm_dutycycle, priority)
    src.cli_query(cmd)

##############################################################################


# Start of Main code
###############################################################################
# Clear screen
os.system('cls')

start_time_string = time.strftime("_%y%m%d_%H%M%S")
full_test_start = time.time()

dest1_power = 13

zb_chan_CoExSrc =24

print "Connecting to CoEx1..."
CoEx1 = DUT_EFR32.DUT_EFR32(CoEx1_name, CoEx1_IP, CoEx1_delimiter, WSTK_CLI_port, WSTK_DBG_Delimiter, WSTK_DBG_port, ENABLE_COEX_CLI_LOG, start_time_string, 6)

print "Connecting to Remote1..."
Remote1 = DUT_EFR32.DUT_EFR32(Remote1_name, Remote1_IP, Remote1_delimiter, WSTK_CLI_port, WSTK_DBG_Delimiter,WSTK_DBG_port, ENABLE_REMOTE_CLI_LOG, start_time_string, 6)


src1 = CoEx1
src1_power = zb_coex_power
dest1 = Remote1

'''
#setup_zigbee_PTA(RESET_AT_START, CoEx1, Remote1, [1,0], ZIGBEE_PTA_OPTIONS_DEFAULT)

#set_zb_pwm(CoEx1, 0, 0, 0) #turn off pwm

'''

#setup_zigbee_PTA(not enable_pta or RESET_COEX, CoEx1, Remote1, [enable_pta,0], zigbee_pta_options)
#set_zb_pwm(CoEx1, zigbee_pwm_period, zigbee_pwm_dutycycle, 1)

print "Leave/Form Network1 with CoEx1/Remote1..."
Network1 = leave_form_network(CoEx1, dest1, zb_chan_CoExSrc, src1_power, dest1_power, Network1_PANID, Network1_pjoin)

#setup_zigbee_PTA(not enable_pta or RESET_COEX, CoEx1, Remote1, [enable_pta,0], zigbee_pta_options)
print "setup_CoEx_throughput_test...NODEID="+ Network1[1]
setup_throughput_test(src1, Network1[1], Network1_payload, Network1_interval, Network1_count)
print "setup_Remote_throughput_test... NODEID="+ Network1[4]
setup_throughput_test(dest1, Network1[4], Network1_payload, Network1_interval, Network1_count)

#print ("CoEx--->Remote...")
#reduce_route_records(src1, dest1, Network1[1], Network1[4])
#print ("Remote--->CoEx...")
#reduce_route_records(dest1, src1, Network1[4], Network1[1])


min_test_time_sec = float(max(Network1_interval*Network1_count,Network2_interval*Network2_count))/1000
max_test_time_sec = min_test_time_sec * MAX_TEST_DURATION_MULTIPLE

start = time.time()

src1.cli_query("plugin coexistence reset-counters")
print ("CoEx plugin throughput start...")
src1.cli_query("plugin throughput start")




dest1.cli_query("plugin coexistence reset-counters")
print ("Rmote plugin throughput start...")
dest1.cli_query("plugin throughput start")

#Network1_results =get_test_results(result_t, result_r)    #
CoEx_Network1_results= get_throughput_test_results(src1, Network1_count, start, max_test_time_sec)
CoEx_Network1_results_rssi = get_throughput_test_results_rssi(dest1, Network1_count)
CoEx_Network1_results_counters = get_throughput_test_results_counters(src1)

Remote_Network1_results = get_throughput_test_results( dest1, Network1_count, start,max_test_time_sec)
Remote_Network1_results_rssi = get_throughput_test_results_rssi(src1, Network1_count)
Remote_Network1_results_counters = get_throughput_test_results_counters(dest1)

# print Network1
print CoEx_Network1_results
print CoEx_Network1_results_rssi
print CoEx_Network1_results_counters

print Remote_Network1_results
print Remote_Network1_results_rssi
print Remote_Network1_results_counters

Network1_results =  CoEx_Network1_results + Remote_Network1_results
Network1_results_rssi = CoEx_Network1_results_rssi + Remote_Network1_results_rssi
Network1_results_counters = CoEx_Network1_results_counters + Remote_Network1_results_counters

Network2_results = Network1_results
Network2_results_rssi = Network1_results_rssi
Network2_results_counters = Network1_results_counters


print Network1_results
print Network1_results_rssi
print Network1_results_counters

print Network2_results
print Network2_results_rssi
print Network2_results_counters

num_ZIGBEE_direction = 1

if IF_ZIGBEE_DIRECTION == "BI-DIRECTION":
    num_ZIGBEE_direction = 2
for j in range(num_ZIGBEE_direction):
    if IF_ZIGBEE_DIRECTION == "BI-DIRECTION":
        zigbee_direction = ZIGBEE_DIRECTION_LIST[j]
    time_string = time.strftime("%m/%d/%y %H:%M:%S")
    zb_spamwriter.writerow([WiFi_iter] \
                           + [trial] \
                           + [time_string] \
                           + [wifi_dir] \
                           + [wifi_chan] \
                           + [wifi_bw] \
                           + [wifi_gi] \
                           + [wifi_mcs] \
                           + [wifi_coex_power] \
                           + [wifi_remote_power] \
                           + [associate_time] \
                           + [wifi_throughput] \
                           + [zigbee_direction] \
                           + [hex(zigbee_pta_options)] \
                           + [zb_co_adj_far_text]
                           + [zb_coex_power] \
                           + [zb_remote_power] \
                           + [zb_chan_CoExSrc] \
                           + [Network1_payload] \
                           + [Network1_interval] \
                           + [Network1_count] \
                           + [Network1_iperf_active[0]] \
                           + [Network1_iperf_active[1]] \
                           + [Network1_iperf_active[2]] \
                           + [Network1_iperf_active[3]] \
                           + [Network1_iperf_inactive[0]] \
                           + [Network1_iperf_inactive[1]] \
                           + [Network1_iperf_inactive[2]] \
                           + [Network1_iperf_inactive[3]] \
                           + [Network1_results[j*(len(CoEx_Network1_results))+0]] \
                           + [Network1_results[j*(len(CoEx_Network1_results))+1]] \
                           + [Network1_results[j*(len(CoEx_Network1_results))+2]] \
                           + [Network1_results[j*(len(CoEx_Network1_results))+3]] \
                           + [Network1_results[j*(len(CoEx_Network1_results))+4]] \
                           + [Network1_results[j*(len(CoEx_Network1_results))+5]] \
                           + [Network1_results[j*(len(CoEx_Network1_results))+6]] \
                           + [Network1_results[j*(len(CoEx_Network1_results))+7]] \
                           + [Network1_results[j*(len(CoEx_Network1_results))+8]] \
                           + [Network1_results[j*(len(CoEx_Network1_results))+9]] \
                           + [Network1_results[j*(len(CoEx_Network1_results))+10]] \
                           + [zb_chan_CoExDest] \
                           + [Network2_payload] \
                           + [Network2_interval] \
                           + [Network2_count] \
                           + [Network2_iperf_active[0]] \
                           + [Network2_iperf_active[1]] \
                           + [Network2_iperf_active[2]] \
                           + [Network2_iperf_active[3]] \
                           + [Network2_iperf_inactive[0]] \
                           + [Network2_iperf_inactive[1]] \
                           + [Network2_iperf_inactive[2]] \
                           + [Network2_iperf_inactive[3]] \
                           + [Network2_results[j*(len(CoEx_Network2_results))+0]] \
                           + [Network2_results[j*(len(CoEx_Network2_results))+1]] \
                           + [Network2_results[j*(len(CoEx_Network2_results))+2]] \
                           + [Network2_results[j*(len(CoEx_Network2_results))+3]] \
                           + [Network2_results[j*(len(CoEx_Network2_results))+4]] \
                           + [Network2_results[j*(len(CoEx_Network2_results))+5]] \
                           + [Network2_results[j*(len(CoEx_Network2_results))+6]] \
                           + [Network2_results[j*(len(CoEx_Network2_results))+7]] \
                           + [Network2_results[j*(len(CoEx_Network2_results))+8]] \
                           + [Network2_results[j*(len(CoEx_Network2_results))+9]] \
                           + [Network2_results[j*(len(CoEx_Network2_results))+10]] \
                           + [enable_pta] \
                           + [zigbee_pwm_period] \
                           + [zigbee_pwm_dutycycle] \
                           + [n1_form_iperf_active] \
                           + [n2_form_iperf_active] \
                           + [Network1_results[j*(len(CoEx_Network1_results))+11]] \
                           + [Network1_results[j*(len(CoEx_Network1_results))+12]] \
                           + [Network1_results[j*(len(CoEx_Network1_results))+13]] \
                           + [Network1_results[j*(len(CoEx_Network1_results))+14]] \
                           + [Network2_results[j*(len(CoEx_Network2_results))+11]] \
                           + [Network2_results[j*(len(CoEx_Network2_results))+12]] \
                           + [Network2_results[j*(len(CoEx_Network2_results))+13]] \
                           + [Network2_results[j*(len(CoEx_Network2_results))+14]] \
                           + [Network1_results_rssi[j*(len(CoEx_Network1_results_rssi))+0]] \
                           + [Network1_results_rssi[j*(len(CoEx_Network1_results_rssi))+1]] \
                           + [Network1_results_rssi[j*(len(CoEx_Network1_results_rssi))+2]] \
                           + [Network1_results_rssi[j*(len(CoEx_Network1_results_rssi))+3]] \
                           + [Network1_results_rssi[j*(len(CoEx_Network1_results_rssi))+4]] \
                           + [Network1_results_counters[j*(len(CoEx_Network1_results_counters))+0]] \
                           + [Network1_results_counters[j*(len(CoEx_Network1_results_counters))+1]] \
                           + [Network1_results_counters[j*(len(CoEx_Network1_results_counters))+2]] \
                           + [Network1_results_counters[j*(len(CoEx_Network1_results_counters))+3]] \
                           + [Network1_results_counters[j*(len(CoEx_Network1_results_counters))+4]] \
                           + [Network1_results_counters[j*(len(CoEx_Network1_results_counters))+5]] \
                           + [Network2_results_rssi[j*(len(CoEx_Network2_results_rssi))+0]] \
                           + [Network2_results_rssi[j*(len(CoEx_Network2_results_rssi))+1]] \
                           + [Network2_results_rssi[j*(len(CoEx_Network2_results_rssi))+2]] \
                           + [Network2_results_rssi[j*(len(CoEx_Network2_results_rssi))+3]] \
                           + [Network2_results_rssi[j*(len(CoEx_Network2_results_rssi))+4]] \
                           + [Network2_results_counters[j*(len(CoEx_Network2_results_counters))+0]] \
                           + [Network2_results_counters[j*(len(CoEx_Network2_results_counters))+1]] \
                           + [Network2_results_counters[j*(len(CoEx_Network2_results_counters))+2]] \
                           + [Network2_results_counters[j*(len(CoEx_Network2_results_counters))+3]] \
                           + [Network2_results_counters[j*(len(CoEx_Network2_results_counters))+4]] \
                           + [Network2_results_counters[j*(len(CoEx_Network2_results_counters))+5]] \
                           + [asserts_per_trial] \
                           + [enable_bt] \
                           + [bt_results[0]] \
                           + [bt_results[1]] \
                           + [bt_results[2]] \
                           + [IPERF_TYPE] \
                           + [IPERF_ADDITIONAL_CLIENT_ARGUMENTS])

    zbcsv_file.flush()
