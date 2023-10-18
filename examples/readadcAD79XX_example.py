#!/usr/bin/env python3
"""Example file for class ADS79XX in pipyadc package

ADS79XX AD-converter cycling through sixteen input channels.

Hardware: ADS79XX interfaced to the Raspberry Pi 4
 
Kunxian Huang 2023-10-18


"""
import os,sys
import logging
from time import perf_counter,sleep,strftime,localtime
from pipyadc import ADS79XX
from pipyadc.ADS79XX_definitions import *


logging.basicConfig(level=logging.DEBUG)


def raw_to_voltage(raw_channel):
    count_mask = 0b0000111111110000 # 8-bit mask
    
    #print("reply message is {}".format(raw_channel))
    adc_ch = raw_channel>>12 #D15-D12 ADC channel number
    adc_count = raw_channel&count_mask # D0-D11 ADC count 
    voltage = ads.v_per_digit*adc_count

    return adc_ch,voltage


def loop_oneminute_measurements(ads,File):
    # Arbitrary length tuple of input channel pair values to scan sequentially
    CH_SEQUENCE = CH0, CH1, CH2, CH3, CH4, CH5, CH6, CH7, CH8, CH9, CH10, CH11, CH12, CH13, CH14, CH15, CH15
    while True:

        # Returns list of integers, one result for each configured channel
        raw_channels = ads.read_sequence(CH_SEQUENCE)
        ch_l =[]
        voltage_l=[]
        for raw_channel in raw_channels:
            raw_to_voltage(raw_channel)
            

        # Text-mode output
        
        voltages = [i * ads.v_per_digit for i in raw_channels]



def main():


    try:
        ###### STEP 1: ADS1256 now supports the context-manager API. [*]
        # Use this to have ADS1256 automatically close the SPI device and
        # pigpio resources at exit:
        with ADS1256() as ads:
            # Get and process data
            loop_oneminute_measurements(ads,File)

    except KeyboardInterrupt:
        print("\nUser Exit.\n")

if __name__=='__main__':
    main()
