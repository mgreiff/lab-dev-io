Useful notes on the BBB
=======================

To simplify installations and git operation on the BB, an internet connection
may be established when connecting the a Linux host computer (except for Fedora).
Run the following two commands on the BB

1. ``/sbin/route add default gw 192.168.7.1``
2. ``echo "nameserver 8.8.8.8" >> /etc/resolv.conf``

and then execute the following two commands on the Linux host

1. ``sudo iptables -A POSTROUTING -t nat -j MASQUERADE``
2. ``sudo echo 1 | sudo tee /proc/sys/net/ipv4/ip_forward > /dev/null``

Now a connection should be established and, and this can be checked with a
ping, such as `ping www.shipyourenemiesglitter.com``.

A useful command for transferring files to and from the device is the
secure copy command, which can be used in the following way

``scp root@192.168.7.2:<some file on the BB> <some directory on the host>``
