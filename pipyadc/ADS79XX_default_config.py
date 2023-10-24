import logging
from pipyadc.ADS79XX_definitions import *
################ Configuration file for one ADS1256 instance  #################
# SPI bus configuration and GPIO pins used for the ADS1255/ADS1256.
#
# These settings are compatible with the "Waveshare High-Precision AD/DA" board.
#
# To create multiple class instances for more than one AD converter, a unique
# configuration must be specified as argument for each instance.

#LOGLEVEL = logging.WARNING
LOGLEVEL = logging.WARNING

# 0 for main SPI bus, 1 for auxiliary SPI bus.
SPI_BUS = 0
# SPI clock rate in Hz. However, since
# the Raspberry pi only supports power-of-two fractions of the 250MHz system
# clock, the closest value would be 1953125 Hz, which is slightly out of spec
# for the ADS79XX. Choosing 250MHz/256 = 976563 Hz is a safe choice.
#SPI_FREQUENCY = 976563
SPI_FREQUENCY = 976563
# Risking the slightly out-of-spec speed:
#SPI_FREQUENCY = 1953125
# If set to True this will perform a chip reset using the hardware reset line
# when initializing the device.
CHIP_HARD_RESET_ON_START = False

#### Raspberry Pi GPIO configuration ##########################################
# =====> NEW in version 2 since using pigpio instead of wiringpi library:
# =====> Raspberry Pi pinning now uses the Broadcom numbering scheme!

# Tuple of all (chip select) GPIO numbers to be configured as an output and
# initialised to (inactive) logic high state before bus communication starts.
# Necessary for more than one SPI device if GPIOs are not otherwise handled.
#CHIP_SELECT_GPIOS_INITIALIZE = (22, 23)
#CHIP_SELECT_GPIOS_INITIALIZE = (22, 23)
# Chip select GPIO pin number.
# This is required as hardware chip select can not be used with the ADS125x
# devices using this library
#CS_PIN      = 22  # GEN3
CS_PIN      = 8   # CE0
# If DRDY is not connected to an input, a sufficient DRDY_TIMEOUT must be
# specified further below and aquisition will be slower.
#DRDY_PIN    = 17
DRDY_PIN    = None
# Hardware reset pin is optional but strongly suggested in case multiple devices
# are connected to the bus as the ADS125x will lock-up in case multiple chips
# are selected simultaneously by accident.
#RESET_PIN   = 18 # Set to None if not used.
RESET_PIN   = None # Set to None if not used.
# Optional power down pin
#PDWN_PIN    = 27 # Set to None if not used.
PDWN_PIN    = None # Set to None if not used.
###############################################################################

# Master clock rate in Hz. Default is 7680000:
# this clock should be the same with SPI clock
CLKIN_FREQUENCY = SPI_FREQUENCY

# 12-bit, 10-bit or 8-bit
DIGITS_NUM = 12
################################################################################


# All following settings are accessible through ADS79XX class properties

##############  ADS79XX Default Adjustable Properties  #################
# Analog reference voltage between VREFH and VREFN pins
v_ref = 3.3
# Gain seting of the integrated programmable amplifier. This value must be
# one of (GAIN_1, GAIN_2, GAIN_4, GAIN_8, GAIN_16, GAIN_32, GAIN_64).
# Gain = 1, V_ref = 2.5V ==> full-scale input voltage = 5.00V, corresponding
# to a 24-bit two's complement output value of 2**23 - 1 = 8388607
gain_flags = 2
################################################################################

####################  ADS1256 Default Register Settings  #######################
# REG_STATUS:
# When enabling the AUTOCAL flag: Any following operation that changes
# PGA GAIN, DRATE or BUFFER flags triggers a self calibration:
# THIS REQUIRES an additional timeout via WaitDRDY() after each such operation.
# Note: BUFFER_ENABLE means the ADC input voltage range is limited
# to (AVDD-2V),see datasheet
status = BUFFER_ENABLE
# REG_MUX:
# Default: positive input = AIN0, negative input = AINCOM
mux = POS_AIN0 | NEG_AINCOM
# REG_ADCON:
# Disable clk out signal (if not needed, source of disturbance),
# sensor detect current sources disabled, gain setting as defined above:
adcon = CLKOUT_OFF | SDCS_OFF | gain_flags
# REG_DRATE: 
# 10 SPS places a filter zero at 50 Hz and 60 Hz for line noise rejection
drate  = DRATE_10
# REG_IO: No GPIOs needed
gpio = 0x00
################################################################################


