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

from oslo_config import cfg

COMMON_OPTIONS = [
    cfg.ListOpt(
        'gearman',
        default=['localhost:4730'],
        help=('List of gearman servers in HOST:PORT format')
    ),
    cfg.ListOpt(
        'db_uri',
        default=['influx://localhost:8086/crawler'],
        help=('List of InfluxDB servers
            in schema://user:password@host:port/db_name format')
    ),

]
