# NTP Server Configuration

To configure Chronyd as an NTP server, a few changes need to be made to the /etc/chronyd.conf file. This guide assumes the default Fedora config file is being used, the file should be broadly the same across distributions, but could differ slightly.

- First line: comment out *pool 2.fedora.pool.ntp.org iburst* by prepending a hash
    - 
- Fifth line: comment out *sourcedir /run/chrony-dhcp* to prevent the server from syncing with the local network router.
-