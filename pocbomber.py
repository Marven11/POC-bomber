#!/usr/bin/env python
# coding=utf-8
  ############################
 #   Author tr0uble_mAker   #
###########################

from inc import console, monkey_patch



def main():
    monkey_patch.monkey_patch_all()
    console.pocbomber_console()

if __name__ == '__main__':
    main()



