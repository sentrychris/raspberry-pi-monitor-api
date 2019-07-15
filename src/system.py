import os

temp = '/opt/vc/bin/vcgencmd measure_temp| sed "s/[^0-9.]//g"'
os.system(temp)