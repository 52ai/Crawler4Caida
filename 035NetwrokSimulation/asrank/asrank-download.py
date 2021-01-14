#!  /usr/bin/env python3
__author__ = "Bradley Huffaker"
__email__ = "<bradley@caida.org>"
# This software is Copyright (C) 2018 The Regents of the University of
# California. All Rights Reserved. Permission to copy, modify, and
# distribute this software and its documentation for educational, research
# and non-profit purposes, without fee, and without a written agreement is
# hereby granted, provided that the above copyright notice, this paragraph
# and the following three paragraphs appear in all copies. Permission to
# make commercial use of this software may be obtained by contacting:
#
# Office of Innovation and Commercialization
#
# 9500 Gilman Drive, Mail Code 0910
#
# University of California
#
# La Jolla, CA 92093-0910
#
# (858) 534-5815
#
# invent@ucsd.edu
#
# This software program and documentation are copyrighted by The Regents of
# the University of California. The software program and documentation are
# supplied “as is”, without any accompanying services from The Regents. The
# Regents does not warrant that the operation of the program will be
# uninterrupted or error-free. The end-user understands that the program
# was developed for research purposes and is advised not to rely
# exclusively on the program for any reason.
#
# IN NO EVENT SHALL THE UNIVERSITY OF CALIFORNIA BE LIABLE TO ANY PARTY FOR
# DIRECT, INDIRECT, SPECIAL, INCIDENTAL, OR CONSEQUENTIAL DAMAGES,
# INCLUDING LOST PR OFITS, ARISING OUT OF THE USE OF THIS SOFTWARE AND ITS
# DOCUMENTATION, EVEN IF THE UNIVERSITY OF CALIFORNIA HAS BEEN ADVISED OF
# THE POSSIBILITY OF SUCH DAMAGE. THE UNIVERSITY OF CALIFORNIA SPECIFICALLY
# DISCLAIMS ANY WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE. THE
# SOFTWARE PROVIDED HEREUNDER IS ON AN “AS IS” BASIS, AND THE UNIVERSITY OF
# CALIFORNIA HAS NO OBLIGATIONS TO PROVIDE MAINTENANCE, SUPPORT, UPDATES,
# ENHANCEMENTS, OR MODIFICATIONS.
#
import re
import argparse
import sys
import json
import time
#from gql import gql, Client
#from gql.transport.requests import RequestsHTTPTransport
from graphqlclient import GraphQLClient

URL = "https://api.asrank.caida.org/v2/graphql"
verbose = False
PAGE_SIZE = 10000
decoder = json.JSONDecoder()
encoder = json.JSONEncoder()

#method to print how to run script
def print_help():
    print (sys.argv[0],"-u as-rank.caida.org/api/v1")
    
######################################################################
## Parameters
######################################################################
parser = argparse.ArgumentParser()
parser.add_argument("-v", dest="verbose", help="prints out lots of messages", action="store_true")
parser.add_argument("-a", dest="asns", help="download asns", type=str) 
parser.add_argument("-o", dest="organizations", help="download organizations", type=str)
parser.add_argument("-l", dest="asnLinks", help="download asn links", type=str)
parser.add_argument("-q", dest="query", help="single query", type=str)
parser.add_argument("-Q", dest="query", help="list query", type=str)
parser.add_argument("-u", dest="url", help="API URL (https://api.asrank.caida.org/v2/graphiql)", type=str, default="https://api.asrank.caida.org/v2/graphql")
parser.add_argument("-d", dest="debug_limit", help="sets the number to download", type=int)
args = parser.parse_args()

######################################################################
## Main code
######################################################################
def main():
    did_nothing = True
    for fname,function in [
            [args.asns, AsnsQuery], 
            [args.organizations, OrganizationsQuery],
            [args.asnLinks, AsnLinksQuery]
            ]:

        if fname:
            DownloadList(args.url, fname, function, args.debug_limit)
            did_nothing = False
    if did_nothing:
        parser.print_help()
        sys.exit()

######################################################################
## Walks the list until it is empty
######################################################################
def DownloadList(url, fname, function, debug_limit):
    hasNextPage = True
    first = PAGE_SIZE
    offset = 0

    # Used by nested calls

    start = time.time()
    print ("writting",fname)
    with open(fname,"w") as f:
        while hasNextPage:
            type,query = function(first, offset)
            if offset == 0 and args.verbose:
                print (query)

            data = DownloadQuery(url, query)
            if not ("data" in data and type in data["data"]):
                print ("Failed to parse:",data,file=sys.stderr)
                sys.exit()
            data = data["data"][type]
            for node in data["edges"]:
                print (encoder.encode(node["node"]), file=f)

            hasNextPage = data["pageInfo"]["hasNextPage"]
            offset += data["pageInfo"]["first"]

            if args.verbose:
                print ("    ",offset,"of",data["totalCount"], " ",time.time()-start,"(sec)",file=sys.stderr)
                start = time.time()

            if debug_limit and debug_limit < offset:
                hasNextPage = False

def DownloadQuery(url, query):
    client = GraphQLClient(url)
    return decoder.decode(client.execute(query))


######################################################################
## Queries
######################################################################

def AsnsQuery(first,offset):
    return [
        "asns", 
        """{
        asns(first:%s, offset:%s) {
            totalCount
            pageInfo {
                first
                hasNextPage
            }
            edges {
                node {
                    asn
                    asnName
                    rank
                    organization {
                        orgId
                        orgName
                    }
                    cliqueMember
                    seen
                    longitude
                    latitude
                    cone {
                        numberAsns
                        numberPrefixes
                        numberAddresses
                    }
                    country {
                        iso
                        name
                    }
                    asnDegree {
                        provider
                        peer
                        customer
                        total
                        transit
                        sibling
                    }
                    announcing {
                        numberPrefixes
                        numberAddresses
                    }
                }
            }
        }
    }""" % (first, offset)
    ]

def OrganizationsQuery(first, offset):
    return [
        "organizations",
        """{
        organizations(first:%s, offset:%s) {
            totalCount
            pageInfo {
                first
                hasNextPage
            }
            edges {
                node {
                    orgId
                    orgName
                    rank
                    seen
                    country {
                        iso
                        name
                    }
                    asnDegree {
                        provider
                        peer
                        customer
                        total
                        transit
                        sibling
                    }
                    orgDegree {
                        total
                        transit
                    }
                    cone {
                        numberAsns
                        numberPrefixes
                        numberAddresses
                    }
                }
            }
        }
    }""" % (first,offset)
    ]

def AsnLinksQuery(first, offset):
    return [
        "asnLinks",
        """{
        asnLinks(first:%s, offset:%s) {
            totalCount
            pageInfo {
                first
                hasNextPage
            }
            edges {
                node {
                    relationship
                    asn0 {
                        asn
                    }
                    asn1 {
                        asn
                    }
                    numberPaths
                }
            } 
        }
    }"""  % (first, offset)
    ]

#run the main method
main()
