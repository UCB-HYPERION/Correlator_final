Dual_Input_Poco
==============================================================

This is a two-input KATCP-based pocket correlator for use on a SNAP board.

Usage
-----------------

In order to run the correlator, a couple of steps must take place. 

1) You must calibrate the ADCs and verify that they are running properly. A 
   secondary aspect of this is checking the power levels of the inputs to the 
   ADC to ensure nothing is saturated, clipping, or is too low to adequately 
   toggle the bits of the ADC.
2) You must decide where you want the data from the correlator run to be stored 
   and get yourself into that location on the RPI.
3) You must run the correlator script itself with the settings you want.

Let's go through step-by-step. 

Step 0
-----------------

Before getting started, make sure that your FPGA has the firmware it needs! You 
will want to make sure that dual_input_poco.bof is located in the directory 
/boffiles on your RPI. If it isn't, your SNAP won't be able to program itself!

ADC Calibration
-----------------

To calibrate the ADCs, you must download and install Zuhra Abdurashidova's 
Python-based ADC calibration software. This can be found here: https://github.com/reeveress/adc16

In particular, you will need to run adc16_init.py with a demux value of 1. This 
script will calibrate the ADC with a test tone. To verify the success of this 
calibration, you will then want to run plot_chans.py. Be sure to include a -s 
when running this command -- that will skip reprogramming the FPGA and losing 
the original calibration.

Further instructions for ADC calibration on the SNAP can be found here: https://casper.berkeley.edu/wiki/SNAP_ADC_Calibration

To check the power levels on the inputs and make sure you're not over- or 
underwhelming the ADCs, you'll also want to run adc_stats.py. This tool plots a 
capture directly from the ADC and calculates the RMS level. Given that it's an 
8-bit ADC, the optimal RMS value will be around 7-8 (i.e. 3 bits toggled). That 
will leave room for bursts of power and RFI in the field without saturating the 
system. Please note that you will have to change the antenna number (i.e. the 
ADC input number) manually to look at anything other than antenna 0.

In order, the commands to run are:

    python adc16_init.py IP_ADDRESS dual_input_poco.bof -d 1
    python plot_chans.py IP_ADDRESS dual_input_poco.bof -d 1 -s
    python adc_stats.py

Data Storage
-----------------

Next up, you want to decide where to keep your data. If you're just doing very 
short runs with your correlator, you may be okay to store your correlator 
output on the RPI itself. However, this is not recommended. If possible, you 
can either run the correlator over SSH and save directly to your machine, or 
you can insert a flash drive or external hard drive to one of the USB ports of 
your RPI, mount that drive, and save your data there. This prevents the risk of 
crashing your RPI by overflowing its small amount of available data storage.

If attaching an external drive, run the following command:

    sudo mount -o uid=pi,gid=pi /dev/sdX /mnt/usb

Then change into the directory /mnt/usb before running the correlator script -- 
remember, the correlator script will save data to whatever the current 
directory of the user is!

NOTE: To find the appropriate value of /dev/sdX, run dmesg | tail after 
inserting the drive to the USB port while the RPI is on. 

Running the Correlator
-----------------

Assuming that you're saving data onto your flash drive and you don't always 
want to babysit your correlator for its whole run, you'll want to get familiar 
with the screen command (or whatever your preferred tool is for safely 
detaching from an SSH session). This will enable the correlator to continue 
running while you continue living your life.

My recommendation is to create a screen session, start the correlator, and then 
detach once you're satisfied that everything is running smoothly. Those 
commands will look something like this:

    screen
    python /path/to/poco_snap_simple.py -s localhost

The -s option is critical in this command, once again this instructs the script 
to skip programming the FPGA with the .bof file and losing the ADC calibration. 
The correlator script DOES NOT calibrate the ADCs, so you MUST include the -s.

If you are running the correlator from your personal machine over an SSH 
connection, replace "localhost" with the IP address of the RPI managing your 
SNAP.

To disconnect from the screen session without killing it, hit ctrl-A-D. To 
return to the screen session, run the command:

    screen -r

Finishing Touches
-----------------

Once you have run your correlator and are ready to call it quits for the day, 
you must shut off your RPI. Run the following command to safely do so before 
cutting power to the SNAP/RPI:
    
    sudo shutdown now

Example
-----------------

I have compiled all of these commands into one bash script that does all the 
hard work for me. This may also be a helpful template to other users. You can 
find that in the file correlator_init_dual
