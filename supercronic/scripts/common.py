#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 17 15:52:27 2020

@author: Paolo Cozzi <paolo.cozzi@ibba.cnr.it>
"""


import os
import shutil
import logging


# Logging istance
logger = logging.getLogger(__name__)

# common file names
ETAG_FILE = "etag_list.csv"
FETCH_BIOSAMPLE_LOG_FILE = "fetch_biosamples.log"

# default page size
PAGE_SIZE = 1000


# from https://bitbucket.org/russellballestrini/virt-back
def rotate_file(target, retention=7):
    """file rotation routine"""

    for i in range(retention-2, 0, -1):  # count backwards
        old_name = "%s.%s" % (target, i)
        new_name = "%s.%s" % (target, i + 1)

        if os.path.exists(old_name):
            logger.debug("Moving %s into %s" % (old_name, new_name))
            shutil.move(old_name, new_name)

    # Moving the first file
    if os.path.exists(target):
        logger.debug("Moving %s into %s.1" % (target, target))
        shutil.move(target, target + '.1')
