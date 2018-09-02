import pygame
from pygame.locals import *

import time, math, sys, json

import tkinter as tk
from tkinter import filedialog as tkfile

pygame.mixer.pre_init(44100, -16, 2, 128)

pygame.init()
pygame.font.init()

pygame.mixer.init(44100)

def vsub(a, b):
    return list(map(lambda x: x[0]-x[1], zip(a,b)))
def vadd(a, b):
    return list(map(lambda x: x[0]+x[1], zip(a,b)))


class Handler():
    def __init__(self):
        self.size= (800,600)
        self.screen=pygame.display.set_mode(self.size)
        self.done = False 
        self.frame_length = 1/60.

        self.objects = []
        self.active_object = None #The selected textbox
        self.prev_mpos = None
        self.mpos = (0,0)

        self.config = json.load(open('config.json','r'))
        self.base_dir = self.config.get('BeatSaberDir', '.')

        filename = tkfile.askdirectory(initialdir = self.base_dir)

        #Load up files
        #Need project class

        #visual analyzer

        #track display

        #keyframes and cursor track

        #keyframe editor

        #selection editor?

        #playback view

        #track definition editor
        
        #grid controller


    def run(self):
        start_time = time.time()

        while not self.done:
            delta = time.time() - start_time
            start_time += delta
            self.prev_mpos = self.mpos
            self.mpos = pygame.mouse.get_pos()
            self.dmpos = vsub(self.mpos, self.prev_mpos)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.done = True
                elif event.type == pygame.VIDEORESIZE:
                    self.size = event.size
                    for obj in self.objects:
                        obj.resize(self.size)
                    #TODO Update sizes?
                elif event.type == KEYDOWN and event.key == K_ESCAPE:
                    self.done = True
                else:
                    for obj in self.objects:
                        obj.do_event(event)

            self.screen.fill((0,0,0))


            pygame.display.flip()

            extra_time = self.frame_length - (time.time()-start_time)
            if extra_time > 0:
                time.sleep(extra_time)


handler = Handler()
handler.run()

