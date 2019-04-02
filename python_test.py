__author__ = 'xxxx'
import os
import re
import time


# Start of Main code
###############################################################################
# Clear screen
os.system('cls')

start_time_string = time.strftime("_%y%m%d_%H%M%S")
full_test_start = time.time()


start = time.time()

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

if IF_DIRECTION == ddddddddd":
    num_direction = 2
for j in range(num__direction):
    if IF_DIRECTION == "BI-DIRECTION":
        direction = DIRECTION_LIST[j]
    time_string = time.strftime("%m/%d/%y %H:%M:%S")
    spamwriter.writerow([WiFi_iter] \
                           + [trial] \
                           + [time_string] \
                           + [dir] \
                           + [chan] \
                           + [bw] \
                           + [gi] \
                           + [mcs] \
                           + [coex_power] \
                           + [remote_power] \
                           + [associate_time] \
                           + [throughput] \
                           + [direction] \
                           + [hex(pta_options)] \
                           + [co_adj_far_text]
                           + [coex_power] \
                           + [remote_power] \
                           + [chan_CoExSrc] \
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
                           + [results[0]] \
                           + [results[1]] \
                           + [results[2]] \
                           + [IPERF_TYPE] \
                           + [IPERF_ADDITIONAL_CLIENT_ARGUMENTS])

    csv_file.flush()
