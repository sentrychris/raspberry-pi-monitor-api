from fanshim import FanShim

fanshim = FanShim()

# Set fan status
def set_fan(action=False):
    if action == True:
        status = "Enabled"
    else:
        status = "Disabled"
    fanshim.set_fan(action)

    return status

# Get fan status
def get_fan():
    status = fanshim.get_fan()
    if status == 1:
        status = "Enabled"
    else:
        status = "Disabled"

    return status