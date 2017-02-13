import os
import sys

print(os.getcwd())

datadir = "../data"

cf = open('comp_header.txt', 'r')
comp = (cf.read())

c = ''
os.chdir(datadir)



#for index, traceFile in enumerate(os.listdir(datadir)):
    traceFile = "dog_AP_trace_" + str(i) + ".csv"
    f = open(traceFile, 'r')
    print(traceFile)
    #if i == 5:
        #break

    c += '"experiment/ap_clamp:' + str(i) + '/name|value": "' + traceFile + '",\n'  #set Instance Name for Observation
    for index, line in enumerate(f):
        if index % 4 == 0:    #take every 4th
            t, v = line.split(sep=',')
            #mv = float(v) * 1000
            #ms = float(t) * 1000000
            c += '"experiment/ap_clamp:' + str(i) + '/any_event:' + str(index) + '/measurement_time|magnitude": ' + str(t) + ',\n'\
                + '"experiment/ap_clamp:' + str(i) + '/any_event:' + str(index) + '/measurement_time|unit": "s",' + '\n' \
                + '"experiment/ap_clamp:' + str(i) + '/any_event:' + str(index) + '/action_potential|magnitude": ' + str(v).rstrip('\n') + ',\n'\
                + '"experiment/ap_clamp:' + str(i) + '/any_event:' + str(index) + '/action_potential|unit": "V",' + '\n' \
                + '"experiment/ap_clamp:' + str(i) + '/any_event:' + str(index) + '/time": "2016-03-17T00:00:00.000Z",' + '\n'
            #if index > 9:
                #break

    #print(comp + c.rstrip(',\n') + '\n}')

t = comp + c.rstrip(',\n') + '\n}'
os.chdir("../src")
cc = open('humongous.txt', 'w')
cc.write(t)
cc.close()

'''
    c += '"experiment/ap_clamp:0/any_event:' + str(index) + '/measurement_time|magnitude": ' + str(t) + ',\n'\
        + '"experiment/ap_clamp:0/any_event:' + str(index) + '/measurement_time|unit": "s",' + '\n' \
        + '"experiment/ap_clamp:0/any_event:' + str(index) + '/action_potential|magnitude": ' + str(v).rstrip('\n') + ',\n'\
        + '"experiment/ap_clamp:0/any_event:' + str(index) + '/action_potential|unit": "V",' + '\n' \
        + '"experiment/ap_clamp:0/any_event:' + str(index) + '/time": "2016-02-03T00:00:00.000Z",' + '\n'
'''

'''
    c += '"experiment/ap_clamp:0/any_event:' + str(index) + '/measurement_time|magnitude": ' + str(t) + ',\n'\
        + '"experiment/ap_clamp:0/any_event:' + str(index) + '/measurement_time|unit": "1",' + '\n' \
        + '"experiment/ap_clamp:0/any_event:' + str(index) + '/action_potential|magnitude": ' + str(v).rstrip('\n') + ',\n'\
        + '"experiment/ap_clamp:0/any_event:' + str(index) + '/action_potential|unit": "1",' + '\n' \
        + '"experiment/ap_clamp:0/any_event:' + str(index) + '/time": "2016-02-03T00:00:00.000Z",' + '\n'
'''

