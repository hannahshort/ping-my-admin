# ping-my-admin

Basic website that shows all IdPs, along with their Sirtfi status, and hosts a Sirtfi-compliant-only metadata file. Updated every time a cron job is run. 

## License
Copyright 2017 CERN
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
   http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

## Files:

###  index.php
Single php page, uses external library for table

### sirtfi-simple-list.py
Creates a simple list of IdPs from a metadata file and stores in the correct format to be turned into a dynamic table

### sirtfi-cron.sh
Script to be run by a cron job. Downloads eduGAIN metadata file and performs various data extractions.

### pipeline.fd
A pipeline for pyFF Federation Feeder to create a metadata file containing only Sirtfi-compliant entities


## Requirements:
* pyFF Federation Feeder 
* Apache web server
* python, php

