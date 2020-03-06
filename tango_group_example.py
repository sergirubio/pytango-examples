import tango
tg = tango.Group('power supplies')
tg.add('ska/ps/*')
devs = tg.get_device_list()
devs
buffer = []
eis =  []
def callback(event):
    print(time.time(),event.attr_name, event.err or event.attr_value.value)
    buffer.append(time.time(),event.attr_name, event.err or event.attr_value.value)
r = tg.read_attributes(('State','Current','Voltage'))
for rr in r:
    print(rr.dev_name(),rr.has_failed() or (rr.get_data().name,rr.get_data().value))

