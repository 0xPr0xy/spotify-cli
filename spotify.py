#!/usr/bin/env python
# -*- coding: utf-8 -*-

from spotify.api import SpotifyApi
import webbrowser
import urwid
import sys

class ItemWidget (urwid.WidgetWrap):

	def __init__ (self, entry, url):
		""" Creates UI Element for every Entry"""
		if entry is not None:
			self._selectable = entry
			self.content = url
			self.item = [
				urwid.Padding(urwid.AttrWrap(
				urwid.Text('%s' % entry),  'body', 'focus')),
			]
		w = urwid.Columns(self.item)
		self.__super.__init__(w)

	def selectable (self):
		return True

	def keypress(self, size, key):
		return key


class Spotify:

	def __init__(self, query):
		self.query = query
		self.playlist = []
		self.palette = [
			('body','dark cyan', '', 'standout'),
			('focus','dark red', '', 'standout'),
			('head','light red', 'black'),
		]
		self.api = SpotifyApi()
		self.search()

	def initGui(self):
		self.listbox = urwid.ListBox(urwid.SimpleListWalker(self.playlist))
		self.view = urwid.Frame(urwid.AttrWrap(self.listbox, 'body'))
		self.loop = urwid.MainLoop(self.view, self.palette, unhandled_input=self.keystroke)
		self.loop.run()

	def open(self, url):
		""" actually opens result in spotify player >< will try to decode their url system """
		webbrowser.open(url)

	def search(self):
		results = self.api.tracks.search(self.query)
		for track in results:
			self.playlist.append(ItemWidget(track.name, track.href))
		self.initGui()

	def keystroke (self,input):
		""" Handle Keystrokes """

		if input in ('q', 'Q'):
			raise urwid.ExitMainLoop()

		if input is 'enter':
			try:
				self.focus = self.listbox.get_focus()[0].content
			except Exception as e:
				print('listbox get_focus failed:\nError: %s' % e)
			self.open(self.focus)


if len(sys.argv) == 2:
	Spotify(sys.argv[1])