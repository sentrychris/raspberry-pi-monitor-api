import sys
import subprocess

interface = "wlan0"

def get_name(cell):
    return matching_line(cell,"ESSID:")[1:-1]

def get_quality(cell):
    quality = matching_line(cell,"Quality=").split()[0].split('/')
    return str(int(round(float(quality[0]) / float(quality[1]) * 100))).rjust(3)

def get_channel(cell):
    return matching_line(cell,"Channel:")

def get_signal_level(cell):
    return matching_line(cell,"Quality=").split("Signal level=")[1]

def get_encryption(cell):
    enc=""
    if matching_line(cell,"Encryption key:") == "off":
        enc="Open"
    else:
        for line in cell:
            matching = match(line,"IE:")
            if matching!=None:
                wpa=match(matching,"WPA Version ")
                if wpa!=None:
                    enc="WPA v."+wpa
        if enc=="":
            enc="WEP"
    return enc

def get_address(cell):
    return matching_line(cell,"Address: ")

rules = {
    "name": get_name,
    "quality": get_quality,
    "channel": get_channel,
    "encryption": get_encryption,
    "address": get_address,
    "signal": get_signal_level
}

def matching_line(lines, keyword):
    for line in lines:
        matching=match(line,keyword)
        if matching!=None:
            return matching
    return None

def match(line,keyword):
    line=line.lstrip()
    length=len(keyword)
    if line[:length] == keyword:
        return line[length:]
    else:
        return

def parse_cell(cell):
    parsed_cell={}
    for key in rules:
        rule=rules[key]
        parsed_cell.update({key:rule(cell)})
    return parsed_cell

def main():
    cells=[[]]
    parsed_cells=[]

    proc = subprocess.Popen(["iwlist", interface, "scan"], stdout=subprocess.PIPE, universal_newlines=True)
    out, err = proc.communicate()

    for line in out.split("\n"):
        cell_line = match(line,"Cell ")
        if cell_line != None:
            cells.append([])
            line = cell_line[-27:]
        cells[-1].append(line.rstrip())
        
    cells=cells[1:]

    for cell in cells:
        parsed_cells.append(parse_cell(cell))

    return parsed_cells

print(main())