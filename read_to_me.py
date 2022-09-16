#!/usr/bin/env python3.8
import time
open('./hello.txt', 'w').write('{}'.format(time.time()))
import os
import sys
if len(sys.argv) != 2:
	print("Usage: read_to_me.py <filename>.epub")
	sys.exit(2)

os.system('''osascript -e 'display notification "Converting {}" with title "Read To Me"' '''.format(sys.argv[1]))