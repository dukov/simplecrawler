# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import logging
import sys


DATEFORMAT = '%Y-%m-%d %H:%M:%S'
LOGFORMAT = '%(asctime)s.%(msecs)03d %(levelname)s ' + \
            '[%(thread)x] (%(module)s) %(message)s'
formatter = logging.Formatter(LOGFORMAT, DATEFORMAT)

def make_nailgun_logger():
    """Make logger for writes logs to stdout"""
    logger = logging.getLogger(__name__)
    handler = logging.StreamHandler(sys.stdout)
    set_logger(logger, handler)
    return logger

def set_logger(logger, handler, level=None):
    if level is None:
        level = logging.DEBUG

    handler.setFormatter(formatter)

    logger.setLevel(level)
    logger.addHandler(handler)


logger = make_nailgun_logger()
