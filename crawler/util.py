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

import string


def vid_gen(end, num_digits):
    digits = string.ascii_lowercase + string.ascii_uppercase + string.digits
    i = 0
    while i <= end:
        k = i
        res = []
        while True:
            res.append(digits[k % 62])
            k = k / 62
            if k == 0:
                break
        if num_digits > len(res):
            res += [digits[0]] * (num_digits - len(res))
        yield i, list(reversed(res))
        i += 1
