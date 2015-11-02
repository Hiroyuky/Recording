#! /usr/bin/env python
# -*- coding: utf-8 -*-

import pyaudio
import sys
#import pylab
import numpy
import wave
import matplotlib.pyplot as plt
import wx

class myFrame(wx.Frame):
	def __init__(self, parent, title):
		wx.Frame.__init__(self, parent, title=title)
		image = wx.Image('out.png')
		self.bitmap = image.ConvertToBitmap()

		wx.StaticBitmap(self, -1, self.bitmap, (0,0), self.GetClientSize())
		self.SetSize(image.GetSize())

def test_audio(event):
	chunk = 1024
	FORMAT = pyaudio.paInt16
	CHANNELS = 1
	RATE = 44100
	RECORD_SECONDS = 2
	WAVE_OUT_NAME = "outwave.wav"

	p = pyaudio.PyAudio()

	stream = p.open(format = FORMAT,
	                channels = CHANNELS,
	                rate = RATE,
	                input = True,
	                frames_per_buffer = chunk)

	print "* recording"
	all = []
	for i in range(0, RATE / chunk * RECORD_SECONDS):
	    data = stream.read(chunk)
	    all.append(data)
	print "* done recording"

	stream.close()
	p.terminate()

	# write data to WAVE file
	data = ''.join(all)
	result = numpy.frombuffer(data,dtype="int16") / float(2**15)	# 2^15 = 32,768

	"""
	pylab.plot(result)
	pylab.ylim([-1,1])
	pylab.show()
	pylab.savefig("out.png")
	"""

	plt.plot(result)
	plt.savefig("out.png")	
	plt.ylim([-1,1])
	plt.show()
	#plt.savefig("out.png")


#	return result;
	"""
	# 
	wf_o = wave.open(WAVE_OUT_NAME, 'wb')
	wf_o.setnchannels(CHANNELS)
	wf_o.setsampwidth(2)
	wf_o.setframerate(RATE)
	"""

def showWindow():
	application = wx.App()
	frame = wx.Frame(None, wx.ID_ANY, u"test_frame", size=(300, 200))

	panel = wx.Panel(frame, wx.ID_ANY)
	panel.SetBackgroundColour("#bfbfbf")

	button_REC = wx.Button(panel, wx.ID_ANY, "REC", size=(50,50))
	button_REC.SetForegroundColour("#FF0000")
	button_REC.SetToolTipString("recording")
	button_REC.Bind(wx.EVT_BUTTON, test_audio)

	layout = wx.BoxSizer(wx.VERTICAL)
	layout.Add(button_REC)

	panel.SetSizer(layout)


	frame.Show()
	application.MainLoop()

if __name__ == '__main__':
	showWindow()

	print "...finished..."
