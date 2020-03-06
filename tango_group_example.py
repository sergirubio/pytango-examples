import tango
import time
import traceback

tg = tango.Group('power supplies')
tg.add('ska/ps/*')
devs = tg.get_device_list()
buffer = []
eis =  {}

proxies = dict((d,tango.DeviceProxy(d)) for d in devs)

def callback(event):
    try:
      print(time.time(),event.attr_name, event.err or event.attr_value.value)
      buffer.append((time.time(),event.attr_name, event if event.err else event.attr_value.value))
    except:
      traceback.print_exc()

def read_attributes():
    r = tg.read_attributes(('State','Current','Voltage'))
    vs = []
    for rr in r:
        vs.append((rr.dev_name(),rr.has_failed() or (rr.get_data().name,rr.get_data().value)))
    return vs

def subscribe_all():
    for d in devs:
        eis[d] = proxies[d].subscribe_event('State',tango.EventType.CHANGE_EVENT,callback)
    
def unsubscribe_all():
    for d,e in eis.items():
        proxies[d].unsubscribe_event(e)
    eis.clear()
        

    

