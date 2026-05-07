#!/usr/bin/env python3
"""Example file for class ADS79XX in pipyadc package

ADS79XX AD-converter cycling through sixteen input channels.

Hardware: ADS79XX interfaced to the Raspberry Pi 4
 
Kunxian Huang 2023-10-18

Expand to test 4 subboards (64) channels

revised on 2026-04-30


"""
import os,sys
import logging
from time import perf_counter,sleep,strftime,localtime
import time
import numpy
sys.path.insert(1,"path/to/PiPyADC")
from pipyadc import ADS79XX
from pipyadc.ADS79XX_definitions import *
from pipyadc import ADS79XX_spi0ce0_config, ADS79XX_spi0ce1_config, ADS79XX_spi1ce0_config, ADS79XX_spi1ce1_config, ADS79XX_spi1ce2_config
from pipyadc import ADS79XX_default_config


logging.basicConfig(level=logging.DEBUG)


def raw_to_voltage(raw_channel,v_per_digit):
    #count_mask = 0b0000111111110000 # 8-bit mask
    count_mask = 0b0000111111111111 # 12-bit mask
    #print("reply message is {}".format(raw_channel))
    adc_ch = raw_channel>>12 #D15-D12 ADC channel number
    adc_count = raw_channel&count_mask # D0-D11 ADC count 
    voltage = v_per_digit*adc_count

    return adc_ch,voltage


def loop_oneminute_measurements(ads1,ads2,ads3,ads4, adcFile):
    # Arbitrary length tuple of input channel pair values to scan sequentially
    CH_SEQUENCE = 0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15
    # sample rate 50 Hz for recording 1 min data 
    counts = 1.0 * 60.0* 50.0
    i=0
    while i <counts:

        record_time_1 = reading_sequence(ads1,0,adcFile)
        record_time_2 = reading_sequence(ads2,1,adcFile)
        record_time_3 = reading_sequence(ads3,2,adcFile)
        record_time_4 = reading_sequence(ads4,3,adcFile)
        """
        start = perf_counter()
        # Returns list of integers, one result for each configured channel
        raw_channels = ads.read_sequence(CH_SEQUENCE)
        record_time = strftime('%c', localtime())
        ch_l =[]
        voltage_l=[]
        for raw_channel in raw_channels:
            ch, voltage = raw_to_voltage(raw_channel,ads.v_per_digit)
            ch_l.append(ch)
            voltage_l.append(voltage)

        end = perf_counter()
        exe_time = (end-start)
        print("execute {}-times time {}\n".format(i,exe_time))
        #print("epoch {} channel {} execute time {}\n".format(epoch,chs,exe_time))
        for ch,voltage in zip(ch_l,voltage_l):
            adcFile.write("CH:{}\t Voltage:{}V\t Time:{}\n".format(ch,voltage,record_time))
        """

        time.sleep(1.0/50.0) # 50 Hz
        i+=1
        
def reading_sequence(ads,adsnumber:int,adcFile):

    start = perf_counter()
    raw_channels = ads.read_sequence(CH_SEQUENCE)
    record_time = strftime('%c', localtime())
    ch_l =[]
    voltage_l=[]
    for raw_channel in raw_channels:
        ch, voltage = raw_to_voltage(raw_channel,ads.v_per_digit)
        ch_l.append(int(ch))
        voltage_l.append(voltage)
    ch_la = numpy.array(ch_l)
    ch_la = ch_la + adsnumber*16

    end = perf_counter()
    exe_time = (end-start)
    print("execute {}-times time {}\n".format(i,exe_time))
    for ch,voltage in zip(ch_la,voltage_l):
            adcFile.write("CH:{}\t Voltage:{}V\t Time:{}\n".format(ch,voltage,record_time))

    return record_time

def main():

    adcfile= open("./adc_files.txt","w+",encoding="utf-8")
    try:
        
        # Use this to have ADS79XX automatically close the SPI device and
        # pigpio resources at exit:
        

        ads1 = ADS79XX(ADS79XX_spi0ce0_config)
        ads2 = ADS79XX(ADS79XX_spi0ce0_config)
        ads3 = ADS79XX(ADS79XX_spi0ce0_config)
        ads4 = ADS79XX(ADS79XX_spi0ce0_config)
        ads_l = [ads1,ads2,ads3,ads4]
        for ads in ads_l:
            ads.set_auto2mode(retain_last=1,reset=1)
            ads.set_auto2mode(retain_last=0,reset=0)
            ads.set_programauto2()

        # Get and process data
        loop_oneminute_measurements(ads1,ads2,ads3,ads4,adcfile)

    except KeyboardInterrupt:
        print("\nUser Exit.\n")

if __name__=='__main__':
    main()
