# Scratch feature "Remote Network Connections" opens port 42001 on
# localhost and sends strings on broadcast events and global variable
# changes to that port. 
# This script listens on that port, reads 'count' chars and filters
# them.
# You can redirect the scratch port to another machine and run this
# script there. 
# ssh wrt -R 42001:172.17.129.6:42001


open_socket_nc() {
	nc localhost 42001 >fifo&
	exec 3<> fifo
	# try to connect
	if ! exec 3<> fifo; then
	  echo "`basename $0`: unable to connect to fifo"
	  exit 1
	fi
	echo "socket is open"
}
open_socket() {
	echo "trying to open socket"
	# try to connect
	if ! exec 3<> /dev/tcp/$HOST/$PORT; then
	  echo "`basename $0`: unable to connect to $HOST:$PORT"
	  exit 1
	fi
	echo "socket is open"
}
read_broadcast() {
	# ^@^@^@^Sbroadcast "Asuro-f"
	#  | | | |     |  |         |
	#  1 2 3 4     10 13        23
	dd bs=1 count=23 <&3 2> /dev/null
	# Using read -n1 instead of dd also works
	# for i in {1..23};do read -n1 c <&3; echo -n $c; done
}
filter() {
	sed -n 's/broadcast "Asuro-//p' | sed 's/"//'
}

flush() {
	dd bs=1 count=512  <&3 -of - 2> /dev/null
}

HOST=127.0.0.1
PORT=42001
TTY=/dev/ttyUSB0

echo Setting Asuro USB-IR Transceiver to 2400 Baud 8N1
stty -f $TTY 2400 -parity -cstopb

# If you have bash, use open_socket
# use open_socket_nc otherwise
open_socket

while cmd=$(read_broadcast | filter); do
	echo $cmd > $TTY
done
