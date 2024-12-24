# pico-powermon
Wireless 12VDC power monitor based on Raspberry Pi Pico W

Easy way to see this output on the target (relaypi):
```
$ netcat -ul -p7312
```

Typical output:
```
pi@relaypi:~ $ netcat -ul -p7312
PowerMon GH_Rigrunner 1734995540 14.1
PowerMon GH_Rigrunner 1734995540 14.1
PowerMon GH_Rigrunner 1734995540 14.1
PowerMon GH_Rigrunner 1734995540 14.1
^C
pi@relaypi:~ $ 
```
