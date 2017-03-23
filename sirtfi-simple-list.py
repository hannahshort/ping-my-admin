 #  Copyright 2017 CERN
 #  Licensed under the Apache License, Version 2.0 (the "License");
 #  you may not use this file except in compliance with the License.
 #  You may obtain a copy of the License at
 #      http://www.apache.org/licenses/LICENSE-2.0
 #  Unless required by applicable law or agreed to in writing, software
 #  distributed under the License is distributed on an "AS IS" BASIS,
 #  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 #  See the License for the specific language governing permissions and
 #  limitations under the License.

from xml.dom import minidom
from xml.dom.minidom import getDOMImplementation
import sys, getopt, copy, codecs


class Metadata:
    entity_descriptor_tag='md:EntityDescriptor'
    idp_tag='md:IDPSSODescriptor'
    contact_tag='md:ContactPerson'
    separator='\t'

    def __init__(self, inputfile, outputfile):
        #Read xml from input file and find entities
        self.input_xml = minidom.parse(inputfile)
	#Save the output file
	self.outputfile = outputfile
	#Create array to save elements
	self.idplistcount = 0
        self.sirtfilistcount = 0

    def get_contact_list(self):
	import pprint
	import json
        entity_list \
            = self.input_xml.getElementsByTagName(self.entity_descriptor_tag)
	f = codecs.open(self.outputfile, 'w')
        print "Read a file with %s Entities" % (len(entity_list))
        iter = 0
        for entity in entity_list:
		is_sirtfi = False
		en_name = ''
		primary_contact = ''
		security_contact = ''
		support_contact = ''
		technical_contact = ''
		exclude = False

		#Only interested in IdPs
		is_idp = entity.getElementsByTagName('md:IDPSSODescriptor')
		if (is_idp.length == 0 ) : 
			continue

		#Look for english display name
		display_names = is_idp[0].getElementsByTagName('mdui:DisplayName')
		for name in display_names : 
			if name.getAttribute('xml:lang') == 'en':
				en_name = name.firstChild.data
		if ( en_name == '' ) :
			exclude = True

		#Get the ID
            	id = entity.getAttribute("entityID")

		#See whether it is Sirtfi compliant and ignore if hide-from-discovery
		attributes = entity.getElementsByTagName('saml:Attribute')
		for attribute in attributes : 
			attribute_values = attribute.getElementsByTagName('saml:AttributeValue')
			for value in attribute_values : 
				if ( value.firstChild.data == 'https://refeds.org/sirtfi' ) : 
					is_sirtfi = True
                                        self.sirtfilistcount = self.sirtfilistcount + 1
				elif ( value.firstChild.data == 'http://refeds.org/category/hide-from-discovery') :
					exclude = True
		
		#Pull out all the contacts and find the primary one 
		contact_array = []
		contacts = entity.getElementsByTagName('md:ContactPerson')
	        for contact in contacts:
			type = contact.getAttribute("contactType")
			emails = contact.getElementsByTagName('md:EmailAddress')
			email_string = ''
			for email in emails : 
				#Remove mailto since it's not always there, and comma separate multiples
				address = email.firstChild.data
         			address = address.strip()
				if address.startswith("mailto:") :
					address = address[7:]
				email_string = email_string + address + ","
			if type == "other" and contact.getAttribute("remd:contactType") == "http://refeds.org/metadata/contactType/security" :
				security_contact = email_string
                        elif type == 'technical' : 
				technical_contact = email_string
			elif type == 'support' :
				support_contact = email_string
		#Emails should be security (if present) & support (or technical if no support)
		if support_contact != '' :
			primary_contact = support_contact
		else : 
			primary_contact = technical_contact
		primary_contact = primary_contact.rstrip(',')

		#Put it all together into the struct and print it if it is valid :)
		if ( exclude == False ) :
                        self.idplistcount = self.idplistcount + 1
			f.write("["+'"'+en_name.strip().encode('utf-8').replace('"','')+'", "'+str(is_sirtfi)+'", "'+primary_contact.encode('utf-8')+'"'+"],")
	
	print "Found %s valid IdPs" % (self.idplistcount)
	print "Of which %s Sirtfi-Compliant IdPs" % (self.sirtfilistcount)
        
	fmeta = codecs.open(self.outputfile+".php", 'w')
        fmeta.write("<?php echo '"+str(self.sirtfilistcount)+" Sirtfi-Compliant Organisations!'; ?> ")

def main():
    argv = sys.argv[1:]
    inputfile = ''
    outputfile = ''
    try:
        opts, args = getopt.getopt(argv,"hi:o:")
    except getopt.GetoptError:
        print 'python sirtfi-simple-list.py -i <inputfile> -o <outputfile>1'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'python sirtfi-simple-list.py -i <inputfile> -o <outputfile>2'
            sys.exit()
        elif opt in ("-i"):
            inputfile = arg
        elif opt in ("-o"):
            outputfile = arg

    #Require both files to continue
    if inputfile is '':
        print 'python sirtfi-simple-list.py -i <inputfile> -o <outputfile>3'
        sys.exit(2)
    if outputfile is '':
        print 'python sirtfi-simple-list.py -i <inputfile> -o <outputfile>4'
        sys.exit(2)

    print 'Input file is:', inputfile
    print 'Output file will be:', outputfile 

    #Create metadata object and find compliant Entities, print
    metadata=Metadata(inputfile, outputfile)
    metadata.get_contact_list()

#################################################################

main()
#################################################################

