#!/usr/sbin/python3


for i in range(1,15):
    #stanza=f"PINS['GPIO{i:02}']=\nPINS['GPIO{i:02}']['name']=''\nPINS['GPIO{i:02}']['channel'] = {i}\n\n"
    stanza=f"PINS['GPIO{i:02}']['type'] = 'digital'\n\n"
    print(stanza)