# mca66
Control HTD MCA66 Home Audio unit with Home Assistant via GW-SL1 Smart Gateway.


Instructions for HA integration:

1. Add the following to HA configuration.yaml file:

    homeassistant:<br>
&nbsp;&nbsp;&nbsp;packages: !include_dir_named packages
  
2. Create "mca66" directory under /config/packages

3. Copy htd.py, mca66.py, and mca66.yaml to /config/packages/mca66 directory.  

4. Edit the IP and port in both sections at the bottom of mca66.py file to match your environment.

5. Edit friendly names in mca66.yaml to match your environment.  Do not edit entitiy names.  Editing the entitiy name could break automations.  

6. Reboot HA.

7. Add items to lovelace to your liking!

