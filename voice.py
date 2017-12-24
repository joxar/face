#-*- cording: utf-8 -*-
import sys
import subprocess

def voiceFunc(phrase):
    pathToMP3 = "mp3/" + phrase + ".MP3"
    subprocess.call("mpg321 " + pathToMP3, shell=True)
