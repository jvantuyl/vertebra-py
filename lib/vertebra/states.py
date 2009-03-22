
# States
start = st.start
auth = st.auth
run = st.run
done = st.done
abort = st.abort
denied = st.denied

# Messages
init = msg.init
ack = msg.ack
nack = msg.nack
data = msg.data
error = msg.error
final = msg.final

# Machines
class outcall_state(machine):
  start = start
  done = [done,abort,denied]
  trans = []