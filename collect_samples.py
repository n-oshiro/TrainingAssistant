#!/usr/bin/env python
# -*- coding: utf-8 -*-
u"""
Collects samples from bing
"""
import settings
import requests
import json
import os
import sys

def getUrls( word, key, skip=0, urls=[]):
    sys.stdout.write("\rSamples: "+str(len(urls)))

    prefix = 'https://api.datamarket.azure.com/Data.ashx/Bing/Search/v1/Image'
    params = {
            'Query': "'%s'" % word , 
            'Adult': "'Off'", 
            '$format': 'json', 
            }
    
    if skip:
        params.update( { '$skip': str( skip ) } )

    results = requests.get( prefix, auth=( key, key ), params=params )
    results = results.json()

    for result in results['d']['results']:
        typ = result[ 'ContentType' ]
        if typ== 'image/jpg' or typ == 'image/jpeg':
            urls.append( result['MediaUrl'] )

    if results['d'].has_key( '__next' ):
        getUrls( word, key, skip+50 )

    if skip == 0:
         sys.stdout.write("\n")

    return urls

def saveImages( urls, dir ):
    count = 0
    skip = 0
    sys.stdout.write("Saving "+str(len(urls))+" image(s)")
    for url in urls:
        try:
            path = os.path.join( dir, os.path.basename( url ) )
            count += 1
            if count%5==0:
                sys.stdout.write(".")
            if count%50==0:
                sys.stdout.write(str(count))
            if not os.path.exists(path): # ファイル名が被った場合は保存しない
                img = requests.get( url ).content
                f = open( path, 'wb' )
                f.write( img )
                img.close()
                f.close()
            else:
                skip+=1
        except:
            pass
    if skip>0:
      sys.stdout.write("done.(Skip "+str(skip)+" images)\n")
    else:
      sys.stdout.write("done.\n")

if __name__ == '__main__':
    word = settings.word
    key = settings.key
    dir = os.path.join( 'static', 'img' )

    urls = getUrls( word, key )
    saveImages( urls, dir )
