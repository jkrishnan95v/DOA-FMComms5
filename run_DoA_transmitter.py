#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Run Doa Transmitter
# GNU Radio version: 3.7.14.0
##################################################

def struct(data): return type('Struct', (object,), data)()
from gnuradio import analog
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio import uhd
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from optparse import OptionParser
import time


class run_DoA_transmitter(gr.top_block):

    def __init__(self):
        gr.top_block.__init__(self, "Run Doa Transmitter")

        ##################################################
        # Variables
        ##################################################
        self.input_variables = input_variables = struct({'ToneFreq': 10000, 'SampleRate': 1000000, 'CenterFreq': 2450000000, 'TxAddr': "addr=169.254.197.15", 'Gain': 20, })

        ##################################################
        # Blocks
        ##################################################
        self.uhd_usrp_sink_0 = uhd.usrp_sink(
        	",".join((input_variables.TxAddr, "")),
        	uhd.stream_args(
        		cpu_format="fc32",
        		channels=range(1),
        	),
        )
        self.uhd_usrp_sink_0.set_clock_source('internal', 0)
        self.uhd_usrp_sink_0.set_samp_rate(input_variables.SampleRate)
        self.uhd_usrp_sink_0.set_center_freq(input_variables.CenterFreq, 0)
        self.uhd_usrp_sink_0.set_gain(input_variables.Gain, 0)
        self.analog_sig_source_x_0 = analog.sig_source_c(input_variables.SampleRate, analog.GR_COS_WAVE, input_variables.ToneFreq, 1, 0)



        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_sig_source_x_0, 0), (self.uhd_usrp_sink_0, 0))

    def get_input_variables(self):
        return self.input_variables

    def set_input_variables(self, input_variables):
        self.input_variables = input_variables


def main(top_block_cls=run_DoA_transmitter, options=None):

    tb = top_block_cls()
    tb.start()
    try:
        raw_input('Press Enter to quit: ')
    except EOFError:
        pass
    tb.stop()
    tb.wait()


if __name__ == '__main__':
    main()
