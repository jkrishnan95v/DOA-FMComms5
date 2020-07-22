#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Calibrate Lin Array X310 Twinrx
# GNU Radio version: 3.7.14.0
##################################################

def struct(data): return type('Struct', (object,), data)()
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio import iio
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from optparse import OptionParser
import doa
import os


class calibrate_lin_array_X310_TwinRX(gr.top_block):

    def __init__(self):
        gr.top_block.__init__(self, "Calibrate Lin Array X310 Twinrx")

        ##################################################
        # Variables
        ##################################################
        self.input_variables = input_variables = struct({'ToneFreq': 10000, 'SampleRate': 10000000, 'CenterFreq': 2450000000, 'RxAddr': "addr=192.168.10.2", 'Gain': 60, 'NumArrayElements': 4, 'NormSpacing': 0.5, 'SnapshotSize': 2**11, 'OverlapSize': 2**9, 'PilotAngle': 45.0, 'DirectoryConfigFiles': "/tmp", 'RelativePhaseOffsets': "measure_X310_TwinRX_relative_phase_offsets_245.cfg", 'AntennaCalibration': "calibration_lin_array_245.cfg", 'Samples2Avg': 2**11, })
        self.rel_phase_offsets_file_name = rel_phase_offsets_file_name = os.path.join(input_variables.DirectoryConfigFiles, input_variables.RelativePhaseOffsets)
        self.antenna_calibration_file_name = antenna_calibration_file_name = os.path.join(input_variables.DirectoryConfigFiles, input_variables.AntennaCalibration)

        ##################################################
        # Blocks
        ##################################################
        self.phase_correct_hier_1 = doa.phase_correct_hier(
            num_ports=input_variables.NumArrayElements,
            config_filename=rel_phase_offsets_file_name,
        )
        self.iio_fmcomms5_source_0_0 = iio.fmcomms5_source_f32c('ip:192.168.3.2', int(input_variables.CenterFreq), int(input_variables.CenterFreq), int(input_variables.SampleRate), int(input_variables.SampleRate), True, True, True, True, 0x8000, True, True, True, "slow_attack", input_variables.Gain, "slow_attack", input_variables.Gain, "slow_attack", input_variables.Gain, "slow_attack", input_variables.Gain, "A_BALANCED", '')
        self.doa_save_antenna_calib_0 = doa.save_antenna_calib(input_variables.NumArrayElements, antenna_calibration_file_name, input_variables.Samples2Avg)
        self.doa_calibrate_lin_array_0 = doa.calibrate_lin_array(input_variables.NormSpacing, input_variables.NumArrayElements, input_variables.PilotAngle)
        self.doa_autocorrelate_0 = doa.autocorrelate(input_variables.NumArrayElements, input_variables.SnapshotSize, input_variables.OverlapSize, 1)
        self.blocks_complex_to_magphase_0 = blocks.complex_to_magphase(input_variables.NumArrayElements)



        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_complex_to_magphase_0, 0), (self.doa_save_antenna_calib_0, 0))
        self.connect((self.blocks_complex_to_magphase_0, 1), (self.doa_save_antenna_calib_0, 1))
        self.connect((self.doa_autocorrelate_0, 0), (self.doa_calibrate_lin_array_0, 0))
        self.connect((self.doa_calibrate_lin_array_0, 0), (self.blocks_complex_to_magphase_0, 0))
        self.connect((self.iio_fmcomms5_source_0_0, 0), (self.phase_correct_hier_1, 0))
        self.connect((self.iio_fmcomms5_source_0_0, 1), (self.phase_correct_hier_1, 1))
        self.connect((self.iio_fmcomms5_source_0_0, 2), (self.phase_correct_hier_1, 2))
        self.connect((self.iio_fmcomms5_source_0_0, 3), (self.phase_correct_hier_1, 3))
        self.connect((self.phase_correct_hier_1, 0), (self.doa_autocorrelate_0, 0))
        self.connect((self.phase_correct_hier_1, 1), (self.doa_autocorrelate_0, 1))
        self.connect((self.phase_correct_hier_1, 2), (self.doa_autocorrelate_0, 2))
        self.connect((self.phase_correct_hier_1, 3), (self.doa_autocorrelate_0, 3))

    def get_input_variables(self):
        return self.input_variables

    def set_input_variables(self, input_variables):
        self.input_variables = input_variables

    def get_rel_phase_offsets_file_name(self):
        return self.rel_phase_offsets_file_name

    def set_rel_phase_offsets_file_name(self, rel_phase_offsets_file_name):
        self.rel_phase_offsets_file_name = rel_phase_offsets_file_name

    def get_antenna_calibration_file_name(self):
        return self.antenna_calibration_file_name

    def set_antenna_calibration_file_name(self, antenna_calibration_file_name):
        self.antenna_calibration_file_name = antenna_calibration_file_name


def main(top_block_cls=calibrate_lin_array_X310_TwinRX, options=None):

    tb = top_block_cls()
    tb.start()
    tb.wait()


if __name__ == '__main__':
    main()
