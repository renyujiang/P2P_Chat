from applescript import tell

# set what command you want to run here
yourCommand = 'python /Users/renyujiang/Desktop/EC530/Assignments/P2P-Chat/print.py 123'

tell.app('Terminal', 'do script"' + yourCommand + '"', background=False)