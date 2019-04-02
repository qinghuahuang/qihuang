__author__ = 'racheung'
import os
import re
import time



# Clear screen
os.system('cls')

start_time_string = time.strftime("_%y%m%d_%H%M%S")
full_test_start = time.time()


regexResult_t = None
result_stats = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1.0, -1.0, -1.0, -1.0]
counters_stats = [1e4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1.0, -1.0, -1.0, -1.0]
#stats = [1e4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1.0, -1.0, -1.0, -1.0]

result1= "Test ended at 18594 ms: 105 packets sent, 104 packets received\n\
Number of messages sent: 105\n\
CCA Failures: 0\n\
Mac Tx Ucast: 105\n\
Mac Tx Ucast Retry: 5\n\
Mac Tx Ucast Fail: 0\n\
APS Tx Ucast Success: 105\n\
APS Tx Ucast Retry: 0\n\
APS Tx Ucast Fail: 0\n\
Latency Min (ms): 10.15\n\
Latency Max (ms): 96.24\n\
Latency Mean(ms): 91.82\n\
Latency Std (ms): 14.11"

result2='''
THROUGHPUT
RESULTS
Total
time
20852
ms
Success
messages: 105
out
of
105
Payload
Throughput: 1007
bits / s
Phy
Throughput: 3021
bits / s
Min
packet
send
time: 52
ms
Max
packet
send
time: 55
ms
Avg
packet
send
time: 52
ms
STD
packet
send
time: 9
ms
'''




result3='''
COUNTERS
CCA Failures: 0 
Mac Tx Ucast: 10 
Mac Tx Ucast Retry: 0 
Mac Tx Ucast Fail: 0 
APS Tx Ucast Success: 10 
APS Tx Ucast Retry: 0 
APS Tx Ucast Fail: 0
'''
result4='''
COUNTERS
PTA Lo Pri Req: 0 
PTA Hi Pri Req: 41393 
PTA Lo Pri Denied: 0 
PTA Hi Pri Denied: 0 
PTA Lo Pri Tx Abrt: 0 
PTA Hi Pri Tx Abrt: 0 
'''

result5='''
THROUGHPUT RESULTS
Total time 20852 ms
Success messages: 105 out of 105
Payload Throughput: 1007 bits/s
Phy Throughput: 3021 bits/s
Min packet send time: 52 ms
Max packet send time: 54 ms
Avg packet send time: 52 ms
STD packet send time: 8 ms
'''

'''
print "result1:"
#print result1
#regexResult = re.search(r'Test ended at (.*) ms: (.*) p.*, (.*) p.*\n.*sent: (.*) .*\n.*Failures: (.*) .*\n.*Ucast: (.*) .*\n.*Retry: (.*) .*\n.*Fail: (.*) .*\n.*Success: (.*) .*\n.*Retry: (.*) .*\n.*Fail: (.*) .*\n.*:(.*) .*\n.*:(.*) .*\n.*:(.*) .*\n.*:(.*) .*\n.*', result1)
regexResult = re.search(r'Test ended at (.*) ms: (.*) p.*, (.*) p.*\n', result1)
#print "regexResult: "+ regexResult
if regexResult:
    result_stats[0] = int(regexResult.group(1)) #Total time
    #print "Total time "+regexResult.group(1)
    #print "received " + regexResult.group(2)
    #print "send " + regexResult.group(3)
    
    result_stats[1] = int(regexResult.group(2)) #recive
    print "Recive" + result_stats[1]
    result_stats[2] = int(regexResult.group(3)) #send
    print "Send" + result_stats[2]
    result_stats[3] = int(regexResult.group(4)) #Min packet send time
    print "Min Time" + result_stats[3]
    result_stats[4] = int(regexResult.group(5)) #Max packet send time
    print "Max Time" + result_stats[4]
    result_stats[5] = int(regexResult.group(6)) #Avg Packet send time
    print "Avg Time" + result_stats[5]
    result_stats[6] = int(regexResult.group(7)) #STD packet send time
    print "STD time..." + result_stats[6]
    '''
print result5
result = re.sub("\n", "", result5, 0)
#result = re.sub(r"\r", "", result, 0)
result =result
print result


#regexResult = re.search(r'THROUGHPUT.*\n.*time(.*).*messages: (.*) .*of (.*) \n .*\n .*\n.*time:(.*) .*\n.*:(.*) .*\.*:(.*) .*\n.*:(.*) .*\n.*',result)
#regexResult = re.search(r'*THROUGHPUT.*time(.*)ms*out*.*messages: (.*)out* .*of (.*) .*time:(.*) .*:(.*) .*:(.*) .*:(.*) ',result)
regexResult = re.search(r'HROUGHPUT.*time(.*)ms.*messages:(.*)out of (.*)Pay.*Throughput:(.*) bit.*Throughput:(.*) bit.* time:(.*)ms.* time:(.*)ms.* time:(.*)ms.* time:(.*)ms', result)
#regexResult = re.search(r'.*THROUGHPUT.*\n.*time(.*) ms\n.*messages:(.*)out of (.*).*\n.*Throughput:(.*) bit*.*\n.*Throughput:(.*) bit*.*\n.* time:(.*)ms\n.* time:(.*)ms\n.* time:(.*)ms\n.* time:(.*)ms\n', result)
#out of (.*).*Throughput:(.*) bit.*Throughput:(.*) bit.*time:(.*)ms.*time:(.*)ms*.*time:(.*)ms.*time:(.*)ms
print "regexResult=:%s " % regexResult
if regexResult:
    result_stats[0] = int(regexResult.group(1)) #Total time
    print "Total time="+regexResult.group(1)
    result_stats[1] = int(regexResult.group(2)) #recive
    print "Recive" + regexResult.group(2)
    result_stats[2] = int(regexResult.group(3)) #send
    print "Send" + regexResult.group(3)
    result_stats[3] = int(regexResult.group(4)) #Min packet send time
    print "Payload Throughput" + regexResult.group(4)
    result_stats[4] = int(regexResult.group(5))  # Min packet send time
    print "Phy Throughput" + regexResult.group(5)
    result_stats[5] = int(regexResult.group(6))  # Max packet send time
    print "Min Time" + regexResult.group(6)
    result_stats[5] = int(regexResult.group(7)) #Max packet send time
    print "Max Time" + regexResult.group(7)
    result_stats[6] = int(regexResult.group(8)) #Avg Packet send time
    print "Avg Time" + regexResult.group(8)
    result_stats[7] = int(regexResult.group(9)) #STD packet send time
    print "STD time..." + regexResult.group(9)

'''
#print result3
#regexResult = re.search(r'COUNT.*\n.*Failures: (.*) .*\n.*Ucast: (.*) .*\n.*Retry: (.*) .*\n.*Fail: (.*) .*\n.*Success: (.*) .*\n.*Retry: (.*) .*\n.*Fail: (.*) .*\n.*', result3)
regexResult = re.search(r'COUNTERS.*\n.*Failures: (.*).*\n.*Ucast: (.*).*\n.*Retry: (.*).*\n.*Fail: (.*).*\n.*Success: (.*).*\n.*Retry: (.*).*\n.*Fail: (.*)', result3) #.*\n.*Ucast: (.*) .*\n.*Retry: (.*) .*\n.*Fail: (.*) .*\n.*Success: (.*) .*\n.*Retry: (.*) .*\n.*Fail: (.*)
if regexResult:
    counters_stats[0] = int(regexResult.group(1)) #CCA Failures
    print "CCA Failures "+regexResult.group(1)
    counters_stats[1] = int(regexResult.group(2)) #Mac Tx Ucast
    print "Mac Tx Ucast " + regexResult.group(2)
    counters_stats[2] = int(regexResult.group(3)) #Mac Tx Ucast Retry
    print "Mac Tx Ucast Retry " + regexResult.group(3)
    counters_stats[3] = int(regexResult.group(4)) #Mac Tx Ucast Fail
    print "Mac Tx Ucast Fail " + regexResult.group(4)
    counters_stats[4] = int(regexResult.group(5)) #APS Tx Ucast Success
    print "APS Tx Ucast Success " + regexResult.group(5)
    counters_stats[5] = int(regexResult.group(6)) #APS Tx Ucast Retry
    print "APS Tx Ucast Retry " + regexResult.group(6)
    counters_stats[6] = int(regexResult.group(7)) #APS Tx Ucast Fail
    print "APS TX Ucast Fail " + regexResult.group(7)

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

print "stats[14] " + str(stats[14])


stats = [-1, -1, -1, -1, -1, -1]
regexResult = re.search(r'PTA Lo Pri Req: (.*) *\n.*:(.*) .*\n.*:(.*) .*\n.*:(.*) .*\n.*:(.*) .*\n.*:(.*) .*\n.*', result4)#
if regexResult:
    stats[0] = int(regexResult.group(1))
    print "PTA Lo Pri Req=" + regexResult.group(1)
    stats[1] = int(regexResult.group(2))
    print "PTA Hi Pri Req=" + regexResult.group(2)
    stats[2] = int(regexResult.group(3))
    print "PTA Lo Pri Denied=" + regexResult.group(3)
    stats[3] = int(regexResult.group(4))
    print "PTA Hi Pri Denied=" + regexResult.group(4)
    stats[4] = int(regexResult.group(5))
    print "PTA Lo Pri Tx Abrt=" + regexResult.group(5)
    stats[5] = int(regexResult.group(6))
    print "PTA Hi Pri Tx Abrt=" + regexResult.group(6)
'''