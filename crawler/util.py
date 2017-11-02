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

from crawler.const import VID_DIGITS
import string

def vid2int(vid):
    res = 0
    for pos, digit in enumerate(vid):
        power = len(vid)-1-pos
        res+= VID_DIGITS.index(digit)*len(VID_DIGITS)**power

    return res

def int2vid(i):
    res = []
    base = len(VID_DIGITS)
    div = i
    while True:
        if div < base:
            res.append(VID_DIGITS[div])
            break
        else:
            res.append(VID_DIGITS[div % base])
            div = div/base
    res.reverse()
    return ''.join(res)

# TODO (dukov) Deprecate this
def vid_gen(start, stop):
    while start <= stop:
        yield start
        start += 1


