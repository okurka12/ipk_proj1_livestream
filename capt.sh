##############
# IPK stream #
# 2024-03-08 #
##############

# general filter for tcpdump
GENERAL_FILTER="ip and (udp or icmp)"

# print this number of lines of each packet (each line is 16 bytes)
NUM=7

# tcpdump options
# -X ... print hexdump + ascii representation
# -l ... line buffered
TCPDUMP_OPTS="-X -l"

# grep options
GREP_OPTS="--color=auto -A $NUM -F"

CAPT_FILENAME=tcpdump.log

# only show packets to/from hostname on the terminal
HOST=localhost

if [ -f "$CAPT_FILENAME" ]; then
    echo -n "overwrite '$CAPT_FILENAME'? (y/n) "
    read OVERWRITE
    if [ $OVERWRITE != "y" ]; then
        exit
    fi
fi

# uncomment one of the below

# capture default interface
# sudo tcpdump $TCPDUMP_OPTS $GENERAL_FILTER | tee $CAPT_FILENAME | grep $GREP_OPTS $HOST

# capture loopback interface
sudo tcpdump $TCPDUMP_OPTS -i lo $GENERAL_FILTER | tee $CAPT_FILENAME | grep $GREP_OPTS $HOST
