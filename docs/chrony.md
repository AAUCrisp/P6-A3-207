# NTP Server Configuration

To configure Chronyd as an NTP server, a few changes need to be made to the /etc/chronyd.conf file. This guide assumes the default Fedora config file is being used, the file should be broadly the same across distributions, but could differ slightly.

- First line: comment out *pool 2.fedora.pool.ntp.org iburst* by prepending a hash
  - This unhooks our server from the global ntp network and allows us to set our own system time
- Fifth line: comment out *sourcedir /run/chrony-dhcp* to prevent the server from syncing with the local network router.
- 23rd line: under "Allow NTP client access from local network" there are 2 options
  - First option is simply writing *allow* to allow any network client that can reach the server to query the time
  - Second option is writting *allow* followed by the IP and Subnet range of your local network such as: "192.168.1.0/24". This restricts time service to only those clients on your local network
- Uncomment the next line *local stratum 10*. This allows chronyd to serve time when the daemon has no connection to an upstream timeserver (very important for our local time only setup)

When all changes are made, restart chronyd either by rebooting, or running *systemctl restart chronyd*
This should be all the changes needed to create a functional local NTP server. If a firewall is enabled, make sure to open port 123 on each desired interface.

## NTP Client Configuration

After the NTP server has been configured, a quick change to the /etc/chronyd.conf is required in order to set our testbed chrony server as the one and only time source.

- First line: comment out *pool 2.fedora.pool.ntp.org iburst* by prepending a hash
  - replace with *server 192.168.1.107 iburst*
  - Server indicates a time server entry, the IP is the IP of the server (port 123 is assumed by default), and the *iburst* flag allows the computer to sync immediately if a change in time is detected, rather than drifting the clock slowly towards the correct value
- Second line: comment out *sourcedir /run/chrony-dhcp* to prevent the server from syncing with the local network router.

Everything else can be left as is, unless changes to logging behavior is desired
