__author__ = 'racheung'
import os
import re
import csv
import time

ZB_CSV_FILENAME = "WiFi_ZigBee_Throughput_Test" # base filename, save in "data" subfolder
start_time_string = time.strftime("_%y%m%d_%H%M%S")

###############################################################################
IF_ZIGBEE_DIRECTION = "BI-DIRECTION"
ZIGBEE_DIRECTION_LIST = ["COEX->REMOTE","REMOTE->COEX"]
Network1 = ["n/a", "n/a", "n/a", "n/a", "n/a"]
Network2 = ["n/a", "n/a", "n/a", "n/a", "n/a"]
bt_results = [0,0,0]
Network1_count = 105
Network2_count = 99
Network1_iperf_active = Network1
Network2_iperf_active = Network2

Network1_iperf_inactive = Network1
Network2_iperf_inactive = Network2

Network1_results = [1e6, Network1_count, 0, Network1_count, 0, 0, Network1_count, 0, 0, Network1_count, 0, -1.0, -1.0, -1.0, -1.0, 1e6, Network1_count, 0, Network1_count, 0, 0, Network1_count, 0, 0, Network1_count, 0, -1.0, -1.0, -1.0, -1.0]
Network1_results_rssi = [0, 100, 100, 100.0, 0.0, 0, 100, 100, 100.0, 0.0]
Network1_results_counters = [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]
Network2_results = [1e6, Network2_count, 0, Network2_count, 0, 0, Network2_count, 0, 0, Network2_count, 0, -1.0, -1.0, -1.0, -1.0, 1e6, Network2_count, 0, Network2_count, 0, 0, Network2_count, 0, 0, Network2_count, 0, -1.0, -1.0, -1.0, -1.0]
Network2_results_rssi = [0, 100, 100, 100.0, 0.0,0, 100, 100, 100.0, 0.0]
Network2_results_counters = [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]
num_direction_results=2
###############################################################################
WiFi_iter  = 0
trial  = 0
time_string  = 0
wifi_dir  = 0
wifi_chan  = 0
wifi_bw  = 0
wifi_gi  = 0
wifi_mcs  = 0
wifi_coex_power  = 0
wifi_remote_power  = 0
associate_time  = 0
wifi_throughput  = 0
zigbee_direction  = "COEX->REMOTE"
zigbee_pta_options  = 0
zb_co_adj_far_text = 0
zb_coex_power  = 0
zb_remote_power  = 0
zb_chan_CoExSrc  = 0
Network1_payload  = 0
Network1_interval  = 0
Network1_count  = 0
# Network1_iperf_active[0]  = 0
# Network1_iperf_active[1]  = 0
# Network1_iperf_active[2]  = 0
# Network1_iperf_active[3]  = 0
# Network1_iperf_inactive[0]  = 0
# Network1_iperf_inactive[1]  = 0
# Network1_iperf_inactive[2]  = 0
# Network1_iperf_inactive[3]  = 0
# Network1_results[0]  = 0
# Network1_results[1]  = 0
# Network1_results[2]  = 0
# Network1_results[3]  = 0
# Network1_results[4]  = 0
# Network1_results[5]  = 0
# Network1_results[6]  = 0
# Network1_results[7]  = 0
# Network1_results[8]  = 0
# Network1_results[9]  = 0
# Network1_results[10]  = 0
zb_chan_CoExDest  = 0
Network2_payload  = 0
Network2_interval  = 0
Network2_count  = 0
# Network2_iperf_active[0]  = 0
# Network2_iperf_active[1]  = 0
# Network2_iperf_active[2]  = 0
# Network2_iperf_active[3]  = 0
# Network2_iperf_inactive[0]  = 0
# Network2_iperf_inactive[1]  = 0
# Network2_iperf_inactive[2]  = 0
# Network2_iperf_inactive[3]  = 0
# Network2_results[0]  = 0
# Network2_results[1]  = 0
# Network2_results[2]  = 0
# Network2_results[3]  = 0
# Network2_results[4]  = 0
# Network2_results[5]  = 0
# Network2_results[6]  = 0
# Network2_results[7]  = 0
# Network2_results[8]  = 0
# Network2_results[9]  = 0
# Network2_results[10]  = 0
enable_pta  = 0
zigbee_pwm_period  = 0
zigbee_pwm_dutycycle  = 0
n1_form_iperf_active  = 0
n2_form_iperf_active  = 0
# Network1_results[11]  = 0
# Network1_results[12]  = 0
# Network1_results[13]  = 0
# Network1_results[14]  = 0
# Network2_results[11]  = 0
# Network2_results[12]  = 0
# Network2_results[13]  = 0
# Network2_results[14]  = 0
# Network1_results_rssi[0]  = 0
# Network1_results_rssi[1]  = 0
# Network1_results_rssi[2]  = 0
# Network1_results_rssi[3]  = 0
# Network1_results_rssi[4]  = 0
# Network1_results_counters[0]  = 0
# Network1_results_counters[1]  = 0
# Network1_results_counters[2]  = 0
# Network1_results_counters[3]  = 0
# Network1_results_counters[4]  = 0
# Network1_results_counters[5]  = 0
# Network2_results_rssi[0]  = 0
# Network2_results_rssi[1]  = 0
# Network2_results_rssi[2]  = 0
# Network2_results_rssi[3]  = 0
# Network2_results_rssi[4]  = 0
# Network2_results_counters[0]  = 0
# Network2_results_counters[1]  = 0
# Network2_results_counters[2]  = 0
# Network2_results_counters[3]  = 0
# Network2_results_counters[4]  = 0
# Network2_results_counters[5]  = 0
asserts_per_trial  = 0
enable_bt = 0
#bt_results[0]  = 0
#bt_results[1]  = 0
#bt_results[2]  = 0
IPERF_TYPE = "IPERF2_UDP"
IPERF_ADDITIONAL_CLIENT_ARGUMENTS = ""
###############################################################################
print "\nCreating .csv files:"

# open Zigbee data file
zbcsv_full_path = os.path.join(os.getcwd(), "data", ZB_CSV_FILENAME + start_time_string + ".csv")

zb_header = False
if os.path.isfile(zbcsv_full_path):
    zb_header = True
print "Zibgee CSV File: " + zbcsv_full_path

with open(zbcsv_full_path, "ab", 0) as zbcsv_file:
    zb_spamwriter = csv.writer(zbcsv_file, dialect='excel')
    if not zb_header:
        zb_spamwriter.writerow(["Iperf Iteration"] \
                               + ["Trial"] \
                               + ["Date_Time"] \
                               + ["WiFi_Direction"] \
                               + ["WiFi_Channel"] \
                               + ["WiFi_Bandwidth"] \
                               + ["WiFi_Guard_Int"] \
                               + ["WiFi_MCS_Index"] \
                               + ["WiFi_AP_TX_Power"] \
                               + ["WiFi_STN_TX_Power"] \
                               + ["Reassociate_Time"] \
                               + ["WiFi_Target Throughput"] \
                               + ["ZB_Direction"] \
                               + ["ZB_PTA_Options"] \
                               + ["Freq Separation"] \
                               + ["ZB_CoEx_TX_Power"] \
                               + ["ZB_Remote_TX_Power"] \
                               + ["N1_Channel"] \
                               + ["N1_Payload"] \
                               + ["N1_Interval"] \
                               + ["N1_Count"] \
                               + ["N1_Status_iperf_active"] \
                               + ["N1_Dest_NodeId_iperf_active"] \
                               + ["N1_Leave_Form_Attempts_iperf_active"] \
                               + ["N1_Join_Attempts_iperf_active"] \
                               + ["N1_Status_iperf_inactive"] \
                               + ["N1_Dest_NodeId_iperf_inactive"] \
                               + ["N1_Leave_Form_Attempts_iperf_inactive"] \
                               + ["N1_Join_Attempts_iperf_inactive"] \
                               + ["N1_Duration"] \
                               + ["N1_Packets_Sent"] \
                               + ["N1_Packets_Received"] \
                               + ["N1_Messages_Sent"] \
                               + ["N1_MAC_TX_Ucast"] \
                               + ["N1_MAC_TX_Ucast_Retry"] \
                               + ["N1_MAC_TX_Ucast_Fail"] \
                               + ["N1_APS_TX_Ucast_Success"] \
                               + ["N1_APS_TX_Ucast_Retry"] \
                               + ["N1_APS_TX_Ucast_Fail"] \
                               + ["N1_CCA_Fail"] \
                               + ["N2_Channel"] \
                               + ["N2_Payload"] \
                               + ["N2_Interval"] \
                               + ["N2_Count"] \
                               + ["N2_Status_iperf_active"] \
                               + ["N2_Dest_NodeId_iperf_active"] \
                               + ["N2_Leave_Form_Attempts_iperf_active"] \
                               + ["N2_Join_Attempts_iperf_active"] \
                               + ["N2_Status_iperf_inactive"] \
                               + ["N2_Dest_NodeId_iperf_inactive"] \
                               + ["N2_Leave_Form_Attempts_iperf_inactive"] \
                               + ["N2_Join_Attempts_iperf_inactive"] \
                               + ["N2_Duration"] \
                               + ["N2_Packets_Sent"] \
                               + ["N2_Packets_Received"] \
                               + ["N2_Messages_Sent"] \
                               + ["N2_MAC_TX_Ucast"] \
                               + ["N2_MAC_TX_Ucast_Retry"] \
                               + ["N2_MAC_TX_Ucast_Fail"] \
                               + ["N2_APS_TX_Ucast_Success"] \
                               + ["N2_APS_TX_Ucast_Retry"] \
                               + ["N2_APS_TX_Ucast_Fail"] \
                               + ["N2_CCA_Fail"] \
                               + ["PTA_ENABLED"] \
                               + ["PWM_period(ms)"] \
                               + ["PWM_dutycycle(%)"] \
                               + ["N1_FORM_IPERF_ACTIVE"] \
                               + ["N2_FORM_IPERF_ACTIVE"] \
                               + ["N1_Latency_Min(ms)"] \
                               + ["N1_Latency_Max(ms)"] \
                               + ["N1_Latency_Mean(ms)"] \
                               + ["N1_Latency_Std(ms)"] \
                               + ["N2_Latency_Min(ms)"] \
                               + ["N2_Latency_Max(ms)"] \
                               + ["N2_Latency_Mean(ms)"] \
                               + ["N2_Latency_Std(ms)"] \
                               + ["N1_RSSI_Received"] \
                               + ["N1_RSSI_Min(dBm)"] \
                               + ["N1_RSSI_Max(dBm)"] \
                               + ["N1_RSSI_Mean(dBm)"] \
                               + ["N1_RSSI_Std(dBm)"] \
                               + ["N1_REQ_LOW_COUNT"] \
                               + ["N1_REQ_HIGH_COUNT"] \
                               + ["N1_DENIED_LOW_COUNT"] \
                               + ["N1_DENIED_HIGH_COUNT"] \
                               + ["N1_ABORT_LOW_COUNT"] \
                               + ["N1_ABORT_HIGH_COUNT"] \
                               + ["N2_RSSI_Received"] \
                               + ["N2_RSSI_Min(dBm)"] \
                               + ["N2_RSSI_Max(dBm)"] \
                               + ["N2_RSSI_Mean(dBm)"] \
                               + ["N2_RSSI_Std(dBm)"] \
                               + ["N2_REQ_LOW_COUNT"] \
                               + ["N2_REQ_HIGH_COUNT"] \
                               + ["N2_DENIED_LOW_COUNT"] \
                               + ["N2_DENIED_HIGH_COUNT"] \
                               + ["N2_ABORT_LOW_COUNT"] \
                               + ["N2_ABORT_HIGH_COUNT"] \
                               + ["ASSERTs in Trial"] \
                               + ["BT_ENABLED"] \
                               + ["BT_STATE"] \
                               + ["BT_DIRECTION"] \
                               + ["BT_CONNECT_ATTEMPTS"] \
                               + ["IPERF_TYPE"] \
                               + ["ADDED_IPERF_ARGS"])
        zbcsv_file.flush()
    CoEx_Network1_results = [9999, 105, 0, 105, 0, 0, 105, 0, 0, 105, 0, -1.0, -1.0, -1.0, -1.0]
    CoEx_Network1_results_rssi = [0, 100, 100, 100.0, 0.0]
    CoEx_Network1_results_counters = [-1, -1, -1, -1, -1, -1]

    CoEx_Network2_results = CoEx_Network1_results
    CoEx_Network2_results_rssi = CoEx_Network1_results_rssi
    CoEx_Network2_results_counters = CoEx_Network1_results_counters

    Remote_Network1_results = [666, 95, 1, 95, 1, 1, 95, 1, 1, 95, 1, -2.0, -2.0, -2.0, -2.0]
    Remote_Network1_results_rssi = [1, 90, 90, 90.0, 1.0]
    Remote_Network1_results_counters = [-2, -2, -2, -2, -2, -2]

    Remote_Network2_results = Remote_Network1_results
    Remote_Network2_results_rssi = Remote_Network1_results_rssi
    Remote_Network2_results_counters = Remote_Network1_results_counters

    #Network_results = [9999, 105, 0, 105, 0, 0, 105, 0, 0, 105, 0, -1.0, -1.0, -1.0, -1.0]
    #Network1_results_rssi = [0, 100, 100, 100.0, 0.0]
    #Network1_results_counters = [-1, -1, -1, -1, -1, -1]

    #///////////////////////////////////////////////

    end = time.time()
    print end

    print Network1
    # print Network1_results
    # print Network1_results_rssi
    # print Network1_results_counters
    print CoEx_Network1_results
    print CoEx_Network1_results_rssi
    print CoEx_Network1_results_counters

    print Remote_Network1_results
    print Remote_Network1_results_rssi
    print Remote_Network1_results_counters

    Network1_results = CoEx_Network1_results + Remote_Network1_results
    Network1_results_rssi = CoEx_Network1_results_rssi + Remote_Network1_results_rssi
    Network1_results_counters = CoEx_Network1_results_counters + Remote_Network1_results_counters

    print Network1_results
    print Network1_results_rssi
    print Network1_results_counters

    print Network2
    # print Network2_results
    # print Network2_results_rssi
    # print Network2_results_counters
    print CoEx_Network2_results
    print CoEx_Network2_results_rssi
    print CoEx_Network2_results_counters

    print Remote_Network2_results
    print Remote_Network2_results_rssi
    print Remote_Network2_results_counters

    Network2_results = CoEx_Network2_results + Remote_Network2_results
    Network2_results_rssi = CoEx_Network2_results_rssi + Remote_Network2_results_rssi
    Network2_results_counters = CoEx_Network2_results_counters + Remote_Network2_results_counters

    print Network2_results
    print Network2_results_rssi
    print Network2_results_counters
    print bt_results  # dummy

    #///////////////////////////////////////////////





    # print Network1
    print CoEx_Network1_results
    print CoEx_Network1_results_rssi
    print CoEx_Network1_results_counters

    print Remote_Network1_results
    print Remote_Network1_results_rssi
    print Remote_Network1_results_counters

    Network1_results = CoEx_Network1_results + Remote_Network1_results
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
    print IF_ZIGBEE_DIRECTION
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
                               + [Network1_results[j * (len(CoEx_Network1_results)) + 0]] \
                               + [Network1_results[j * (len(CoEx_Network1_results)) + 1]] \
                               + [Network1_results[j * (len(CoEx_Network1_results)) + 2]] \
                               + [Network1_results[j * (len(CoEx_Network1_results)) + 3]] \
                               + [Network1_results[j * (len(CoEx_Network1_results)) + 4]] \
                               + [Network1_results[j * (len(CoEx_Network1_results)) + 5]] \
                               + [Network1_results[j * (len(CoEx_Network1_results)) + 6]] \
                               + [Network1_results[j * (len(CoEx_Network1_results)) + 7]] \
                               + [Network1_results[j * (len(CoEx_Network1_results)) + 8]] \
                               + [Network1_results[j * (len(CoEx_Network1_results)) + 9]] \
                               + [Network1_results[j * (len(CoEx_Network1_results)) + 10]] \
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
                               + [Network2_results[j * (len(CoEx_Network2_results)) + 0]] \
                               + [Network2_results[j * (len(CoEx_Network2_results)) + 1]] \
                               + [Network2_results[j * (len(CoEx_Network2_results)) + 2]] \
                               + [Network2_results[j * (len(CoEx_Network2_results)) + 3]] \
                               + [Network2_results[j * (len(CoEx_Network2_results)) + 4]] \
                               + [Network2_results[j * (len(CoEx_Network2_results)) + 5]] \
                               + [Network2_results[j * (len(CoEx_Network2_results)) + 6]] \
                               + [Network2_results[j * (len(CoEx_Network2_results)) + 7]] \
                               + [Network2_results[j * (len(CoEx_Network2_results)) + 8]] \
                               + [Network2_results[j * (len(CoEx_Network2_results)) + 9]] \
                               + [Network2_results[j * (len(CoEx_Network2_results)) + 10]] \
                               + [enable_pta] \
                               + [zigbee_pwm_period] \
                               + [zigbee_pwm_dutycycle] \
                               + [n1_form_iperf_active] \
                               + [n2_form_iperf_active] \
                               + [Network1_results[j * (len(CoEx_Network1_results)) + 11]] \
                               + [Network1_results[j * (len(CoEx_Network1_results)) + 12]] \
                               + [Network1_results[j * (len(CoEx_Network1_results)) + 13]] \
                               + [Network1_results[j * (len(CoEx_Network1_results)) + 14]] \
                               + [Network2_results[j * (len(CoEx_Network2_results)) + 11]] \
                               + [Network2_results[j * (len(CoEx_Network2_results)) + 12]] \
                               + [Network2_results[j * (len(CoEx_Network2_results)) + 13]] \
                               + [Network2_results[j * (len(CoEx_Network2_results)) + 14]] \
                               + [Network1_results_rssi[j * (len(CoEx_Network1_results_rssi)) + 0]] \
                               + [Network1_results_rssi[j * (len(CoEx_Network1_results_rssi)) + 1]] \
                               + [Network1_results_rssi[j * (len(CoEx_Network1_results_rssi)) + 2]] \
                               + [Network1_results_rssi[j * (len(CoEx_Network1_results_rssi)) + 3]] \
                               + [Network1_results_rssi[j * (len(CoEx_Network1_results_rssi)) + 4]] \
                               + [Network1_results_counters[j * (len(CoEx_Network1_results_counters)) + 0]] \
                               + [Network1_results_counters[j * (len(CoEx_Network1_results_counters)) + 1]] \
                               + [Network1_results_counters[j * (len(CoEx_Network1_results_counters)) + 2]] \
                               + [Network1_results_counters[j * (len(CoEx_Network1_results_counters)) + 3]] \
                               + [Network1_results_counters[j * (len(CoEx_Network1_results_counters)) + 4]] \
                               + [Network1_results_counters[j * (len(CoEx_Network1_results_counters)) + 5]] \
                               + [Network2_results_rssi[j * (len(CoEx_Network2_results_rssi)) + 0]] \
                               + [Network2_results_rssi[j * (len(CoEx_Network2_results_rssi)) + 1]] \
                               + [Network2_results_rssi[j * (len(CoEx_Network2_results_rssi)) + 2]] \
                               + [Network2_results_rssi[j * (len(CoEx_Network2_results_rssi)) + 3]] \
                               + [Network2_results_rssi[j * (len(CoEx_Network2_results_rssi)) + 4]] \
                               + [Network2_results_counters[j * (len(CoEx_Network2_results_counters)) + 0]] \
                               + [Network2_results_counters[j * (len(CoEx_Network2_results_counters)) + 1]] \
                               + [Network2_results_counters[j * (len(CoEx_Network2_results_counters)) + 2]] \
                               + [Network2_results_counters[j * (len(CoEx_Network2_results_counters)) + 3]] \
                               + [Network2_results_counters[j * (len(CoEx_Network2_results_counters)) + 4]] \
                               + [Network2_results_counters[j * (len(CoEx_Network2_results_counters)) + 5]] \
                               + [asserts_per_trial] \
                               + [enable_bt] \
                               + [bt_results[0]] \
                               + [bt_results[1]] \
                               + [bt_results[2]] \
                               + [IPERF_TYPE] \
                               + [IPERF_ADDITIONAL_CLIENT_ARGUMENTS])

        zbcsv_file.flush()
'''
    num_ZIGBEE_direction = 1
    print IF_ZIGBEE_DIRECTION
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
                               + [Network1_results[j * (len(CoEx_Network1_results)) + 0]] \
                               + [Network1_results[j * (len(CoEx_Network1_results)) + 1]] \
                               + [Network1_results[j * (len(CoEx_Network1_results)) + 2]] \
                               + [Network1_results[j * (len(CoEx_Network1_results)) + 3]] \
                               + [Network1_results[j * (len(CoEx_Network1_results)) + 4]] \
                               + [Network1_results[j * (len(CoEx_Network1_results)) + 5]] \
                               + [Network1_results[j * (len(CoEx_Network1_results)) + 6]] \
                               + [Network1_results[j * (len(CoEx_Network1_results)) + 7]] \
                               + [Network1_results[j * (len(CoEx_Network1_results)) + 8]] \
                               + [Network1_results[j * (len(CoEx_Network1_results)) + 9]] \
                               + [Network1_results[j * (len(CoEx_Network1_results)) + 10]] \
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
                               + [Network2_results[j * (len(CoEx_Network2_results)) + 0]] \
                               + [Network2_results[j * (len(CoEx_Network2_results)) + 1]] \
                               + [Network2_results[j * (len(CoEx_Network2_results)) + 2]] \
                               + [Network2_results[j * (len(CoEx_Network2_results)) + 3]] \
                               + [Network2_results[j * (len(CoEx_Network2_results)) + 4]] \
                               + [Network2_results[j * (len(CoEx_Network2_results)) + 5]] \
                               + [Network2_results[j * (len(CoEx_Network2_results)) + 6]] \
                               + [Network2_results[j * (len(CoEx_Network2_results)) + 7]] \
                               + [Network2_results[j * (len(CoEx_Network2_results)) + 8]] \
                               + [Network2_results[j * (len(CoEx_Network2_results)) + 9]] \
                               + [Network2_results[j * (len(CoEx_Network2_results)) + 10]] \
                               + [enable_pta] \
                               + [zigbee_pwm_period] \
                               + [zigbee_pwm_dutycycle] \
                               + [n1_form_iperf_active] \
                               + [n2_form_iperf_active] \
                               + [Network1_results[j * (len(CoEx_Network1_results)) + 11]] \
                               + [Network1_results[j * (len(CoEx_Network1_results)) + 12]] \
                               + [Network1_results[j * (len(CoEx_Network1_results)) + 13]] \
                               + [Network1_results[j * (len(CoEx_Network1_results)) + 14]] \
                               + [Network2_results[j * (len(CoEx_Network2_results)) + 11]] \
                               + [Network2_results[j * (len(CoEx_Network2_results)) + 12]] \
                               + [Network2_results[j * (len(CoEx_Network2_results)) + 13]] \
                               + [Network2_results[j * (len(CoEx_Network2_results)) + 14]] \
                               + [Network1_results_rssi[j * (len(CoEx_Network1_results_rssi)) + 0]] \
                               + [Network1_results_rssi[j * (len(CoEx_Network1_results_rssi)) + 1]] \
                               + [Network1_results_rssi[j * (len(CoEx_Network1_results_rssi)) + 2]] \
                               + [Network1_results_rssi[j * (len(CoEx_Network1_results_rssi)) + 3]] \
                               + [Network1_results_rssi[j * (len(CoEx_Network1_results_rssi)) + 4]] \
                               + [Network1_results_counters[j * (len(CoEx_Network1_results_counters)) + 0]] \
                               + [Network1_results_counters[j * (len(CoEx_Network1_results_counters)) + 1]] \
                               + [Network1_results_counters[j * (len(CoEx_Network1_results_counters)) + 2]] \
                               + [Network1_results_counters[j * (len(CoEx_Network1_results_counters)) + 3]] \
                               + [Network1_results_counters[j * (len(CoEx_Network1_results_counters)) + 4]] \
                               + [Network1_results_counters[j * (len(CoEx_Network1_results_counters)) + 5]] \
                               + [Network2_results_rssi[j * (len(CoEx_Network2_results_rssi)) + 0]] \
                               + [Network2_results_rssi[j * (len(CoEx_Network2_results_rssi)) + 1]] \
                               + [Network2_results_rssi[j * (len(CoEx_Network2_results_rssi)) + 2]] \
                               + [Network2_results_rssi[j * (len(CoEx_Network2_results_rssi)) + 3]] \
                               + [Network2_results_rssi[j * (len(CoEx_Network2_results_rssi)) + 4]] \
                               + [Network2_results_counters[j * (len(CoEx_Network2_results_counters)) + 0]] \
                               + [Network2_results_counters[j * (len(CoEx_Network2_results_counters)) + 1]] \
                               + [Network2_results_counters[j * (len(CoEx_Network2_results_counters)) + 2]] \
                               + [Network2_results_counters[j * (len(CoEx_Network2_results_counters)) + 3]] \
                               + [Network2_results_counters[j * (len(CoEx_Network2_results_counters)) + 4]] \
                               + [Network2_results_counters[j * (len(CoEx_Network2_results_counters)) + 5]] \
                               + [asserts_per_trial] \
                               + [enable_bt] \
                               + [bt_results[0]] \
                               + [bt_results[1]] \
                               + [bt_results[2]] \
                               + [IPERF_TYPE] \
                               + [IPERF_ADDITIONAL_CLIENT_ARGUMENTS])

        zbcsv_file.flush()
'''
