###############################################################################
##
##  Copyright (C) 2014, Tavendo GmbH and/or collaborators. All rights reserved.
##
##  Redistribution and use in source and binary forms, with or without
##  modification, are permitted provided that the following conditions are met:
##
##  1. Redistributions of source code must retain the above copyright notice,
##     this list of conditions and the following disclaimer.
##
##  2. Redistributions in binary form must reproduce the above copyright notice,
##     this list of conditions and the following disclaimer in the documentation
##     and/or other materials provided with the distribution.
##
##  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
##  AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
##  IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
##  ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
##  LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
##  CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
##  SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
##  INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
##  CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
##  ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
##  POSSIBILITY OF SUCH DAMAGE.
##
###############################################################################

from twisted.internet.defer import inlineCallbacks

from autobahn.twisted.wamp import ApplicationSession
import os
import sys
import base64 
from PIL import Image
import cv2
import numpy as np
import io
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO


def stringToImage(base64_string):
    imgdata = base64.b64decode(base64_string)
    return Image.open(io.BytesIO(imgdata))

  
def processImage(data):  
    # Your image processing here.
    img = stringToImage(data)
    gray_image = cv2.cvtColor(np.asarray(img), cv2.COLOR_BGR2GRAY)
    retval, buffer = cv2.imencode('.jpg', gray_image)
    jpg_as_text = base64.b64encode(buffer)
    return jpg_as_text.decode("utf-8")   

def contourCount(data):
    img = stringToImage(data)
    gray = cv2.cvtColor(np.asarray(img), cv2.COLOR_BGR2GRAY)
    ret,thresh = cv2.threshold(gray,127,255,1)
    #contours,h = cv2.findContours(thresh,1,2)
    im2, contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE) 
    for cnt in contours:
        cv2.drawContours(np.asarray(img),[cnt],0,(0,0,255),1)
    retval, buffer = cv2.imencode('.jpg', np.asarray(img))
    jpg_as_text = base64.b64encode(buffer)
    return jpg_as_text.decode("utf-8")          

class MyComponent(ApplicationSession):

    @inlineCallbacks
    def onJoin(self, details):

        def on_cam_event(args):
             returnimage = processImage(args)
             self.publish("com.camera.imagetrip",returnimage)

        try:
             yield self.subscribe(on_cam_event, 'com.camera.image')
        except Exception as e:
             print("failed to register procedures: {}".format(e))
