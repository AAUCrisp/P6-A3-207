# P6-A3-207
6th Semester Data Quality Project

## Program Arguments
Arguments able to call when running the programs.  
Options marked with an astrisk (*) is the default value, and **all** options are non-mandatory.

- `-payload <string>` - Payload you want to be the sensor data.  
- `-target <string>` - Enter the name of the node to transfer to, options are:
  - `up0`
  - `up1`
  - `up2`*
  - `up3`
  - `cal`
  - `ste`
  - `tho`
  - `ub8`

- `-tech <string>` - The *connection technology* it use, (if the system supports them all) options are:
  - `wifi` *
  - `5g` 
  - `ethernet`  

- `-portOut <int>` - The *port* for the outgoing connection, if there is any. 

- `-portIn <int>` - The *port* for incoming connections, if there is any.   

- `-loop` - *Loopback mode*, which makes the program target itself.   

- `-dev` - *Development mode*, setting *Ground Truth* to sync via WiFi, to avoid Ethernet restrictions, and run the rest of the program in *loopback mode*.   

- `-v` - *Verbose mode*, for development and troubleshooting print-outs.   

- `-delay <int>` - Sets the delay between data transfers.   

- `-RTOint <int>` - Sets the delay between syncronization for RTO.   

- `-VKTint <int>` - Sets the delay between syncronization for VKT.   

- `-cwd <string>` - Sets the *Python working directory*, to whatever you've inserted.
   

#### Ground Truth Specific
- `-gt <string>` - Enter the name of the node to transfer to, options are:
  - `up0`
  - `up1`
  - `up2`*
  - `up3`
  - `cal`
  - `ste`
  - `tho`
  - `ub8`  

- `-gtTech <string>` - The connection technology it use, (if the system supports them all) options are:
  - `wifi` *
  - `5g` 
  - `ethernet`  

- `-GTint <int>` - Sets the delay between syncronization for GT.   


## INSTALL
```py
# Install dependencies
pip3 install -r requirements.txt

# Run a sensor:
python3.11 sensor.py

# Run a backend:
python3.11 backend.py

# Run a headend:
python3.11 headend.py
```