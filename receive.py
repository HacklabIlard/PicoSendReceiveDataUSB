#
# Tutorial: https://goldensyrupgames.com/blog/2022-02-04-pico-simple-two-way-serial/
# Source code: https://github.com/GSGBen/pico-serial

from urandom import randint
import uselect
from machine import Pin, SPI, PWM, RTC
import framebuf
import time
import random
import gc
import math
from sys import stdin, exit
import micropython
import sys

TERMINATOR = "\n"


class Pico:


    def __init__(self):
        self.run_loop = True
        self.buffered_input = []
        self.input_line_this_tick = ""

    def read_serial_input(self):
        select_result = uselect.select([stdin], [], [], 0)
        while select_result[0]:
            input_character = stdin.read(1)
            self.buffered_input.append(input_character)
            select_result = uselect.select([stdin], [], [], 0)
        if TERMINATOR in self.buffered_input:
            line_ending_index = self.buffered_input.index(TERMINATOR)
            self.input_line_this_tick = "".join(self.buffered_input[:line_ending_index])
            if line_ending_index < len(self.buffered_input):
                self.buffered_input = self.buffered_input[line_ending_index + 1 :]
            else:
                self.buffered_input = []
        else:
            self.input_line_this_tick = ""


    def exit(self):
        self.run_loop = False

    def main(self):
        latest_input_line = ""

        while self.run_loop:

            self.read_serial_input()
           
            if self.input_line_this_tick:
                latest_input_line = self.input_line_this_tick
            print(latest_input_line)

            time.sleep_ms(100)


if __name__ == "__main__":
    pico = Pico()
    pico.main()
    gc.collect()