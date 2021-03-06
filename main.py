# -*- coding: utf-8 -*-
import pygame
import pytmx
import random
import sqlite3
import webbrowser
from mutagen.mp3 import MP3
import datetime
import numpy
import math
import sys
import os
import pymsgbox
import traceback
import menu
import resources

pygame.init()
pygame.display.set_caption('Mutation Purge')
pygame.display.set_icon(pygame.image.load('icon.ico'))
pygame.mouse.set_visible(False)
if resources.FILES[3] != []:
	if resources.FILES[3][0] == 'PT': import database_PT as database
	if resources.FILES[3][0] == 'EN': import database_EN as database
else: import database_PT as database

class Loading():
	def __init__(self):
		self.screen = pygame.display.set_mode((1200, 800), pygame.RESIZABLE | pygame.DOUBLEBUF)
		self.display = pygame.Surface((1200, 800))
		self.windoww = 1200
		self.windowh = 800
		self.fnt = {'DEFAULT': pygame.font.SysFont('Calibri', 30)}
		self.load = 0
		self.classrun = True
		self.dot = ''
		self.txt = 0
		self.msg = 0
		self.tim = 1.0
		self.gif = 0

	def callresources(self):
		self.load = 2
		self.txt = 1
		for w in range(resources.RANGE_SKIN):
			for p in range(resources.RANGE_FACE):
				for h in range(resources.RANGE_HAIR):
					resources.heads(p,w,h)
					self.run()
		self.txt = 2
		for w in range(resources.RANGE_SKIN):
			for t in range(resources.RANGE_COSTUME):
				resources.bodies(w,t)
				self.run()
		self.txt = 3
		resources.battlesprites()
		self.txt = 4
		for j in os.listdir('SFX'): 
			resources.sfx(j)
			self.run()
		self.txt = 5
		for i in range(resources.RANGE_RADIO): 
			resources.radio(i)
			self.run()
		self.txt = 6
		resources.music()
		self.run()
		self.classrun = False

	def run(self):
		flp = False
		if self.load == 1:
			self.callresources()
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			if event.type == pygame.VIDEORESIZE:
				self.windoww = event.w
				self.windowh = event.h
				self.screen = pygame.display.set_mode((self.windoww, self.windowh), pygame.RESIZABLE | pygame.DOUBLEBUF)
				self.fnt = {'DEFAULT': pygame.font.SysFont('Calibri', math.floor(self.windoww/300) * 8)}
				flp = True

		self.tim += 0.01
		if self.tim >= 1.0: self.tim = 0.0; self.msg = round(random.randint(0,len(database.MESSAGES) - 1)); flp = True

		if flp == True: self.display.fill((0,0,0))
		else: self.display.fill((0,0,0),pygame.Rect(1120,720,30,30))

		for i in range(len(database.MESSAGES[self.msg])):
			self.display.blit(self.fnt['DEFAULT'].render(database.MESSAGES[self.msg][i], True, (240,240,240)), (math.floor(self.windoww/300) * 100, (math.floor(self.windoww/300) * 70) + (i * 40)))

		self.gif += 1
		if self.gif >= 8: self.gif = 0
		self.display.blit(pygame.image.load('Sprites/loading_' + str(self.gif) + '.png'), (self.windoww - 80, self.windowh - 80))

		self.screen.blit(self.display, (0, 0))
		if flp == True: pygame.display.flip()
		else: pygame.display.update(pygame.Rect(self.windoww - 80, self.windowh - 80,30,30))
		if self.load == 0: self.load = 1

class Title:
	def __init__(self):
		self.screen = pygame.display.set_mode((1200, 800), pygame.RESIZABLE)
		self.display = [pygame.Surface((600, 400)), pygame.Surface((1200, 800), pygame.SRCALPHA)]
		self.windoww = 1200
		self.windowh = 800
		self.fnt = {'DEFAULT': pygame.font.SysFont('Calibri', 30), 'MONOTYPE': pygame.font.Font('Fonts/PrestigeEliteStd.otf', 30)}
		self.sfx = pygame.mixer.Channel(0)
		self.ton = pygame.mixer.Channel(1)
		self.msc = pygame.mixer.Channel(2)
		self.winbar = 210
		self.wait = 100
		self.noise = 0
		self.tv = round(random.randint(1,10))
		self.transtype = 0
		self.transform = 0
		self.transpeed = 0
		self.rectrot = 0
		self.opt = 0
		self.lopt = 0
		self.mnu = 0
		self.glock = pygame.time.Clock()
		self.FPS = 60
		self.scroll = 0
		self.skip = False
		self.classrun = True
		self.loadingif = None
		self.holiday = datetime.datetime.now()
		self.logoalpha = 0

		for i in resources.FILES[0]:
			if resources.FILES[1][i] == 0:
				del resources.FILES[0][i]
				del resources.FILES[1][i]
				del resources.FILES[2][i]
				del resources.FILES[3][i]

		if resources.GAMETIME != 0:
			self.msc.play(pygame.mixer.Sound('Music/here_comes_the_death.wav'))
			while self.logoalpha < 255:
				if self.mnu >= 1: break
				self.logoalpha += 15
				self.run()
			for i in range(50):
				if self.mnu >= 1: break
				self.run()
			while self.logoalpha > 0:
				if self.mnu >= 1: break
				self.logoalpha -= 15
				self.run()
			for i in range(30):
				if self.mnu >= 1: break
				self.run()
			self.mnu = 1
			for i in range(40):
				if self.mnu >= 2: break
				self.run()
			self.mnu = 2
			while self.winbar > 50:
				self.winbar -= 5
				self.run()

	def random(self):
		self.msc.stop()
		pygame.mixer.music.stop()
		self.ton.play(resources.SOUND['NOISE'],-1)
		self.tv = 0
		self.transform = 0
		self.rectrot = 0
		for i in range(round(random.randint(5,30))): self.run()
		if self.mnu < 6:
			self.ton.stop()
			self.tv = round(random.randint(1,17))
			self.transtype = round(random.randint(0,5))
			spd = round(random.randint(0,100))
			if self.transtype == 5: self.transpeed = 2
			elif spd > 75: self.transpeed = -2
			elif spd > 50: self.transpeed = 2
			elif spd > 25: self.transpeed = -1
			else: self.transpeed = 1
			self.wait = round(random.randint(50,100))
			rd = round(random.randint(0,9))
			if len(resources.RADIO[str(rd)]) > 0:
				sng = round(random.randint(0,len(resources.RADIO[str(rd)]) - 1))
				msc = 'Songs/FM_' + str(rd) + '/' + resources.RADIO[str(rd)][sng]
				if msc.endswith('.mp3'):
					audio = MP3(msc)
					pygame.mixer.music.load(msc)
					pygame.mixer.music.play(1,round(random.randint(20,int(audio.info.length) - 20)))
				elif msc.endswith('.wav'):
					audio = pygame.mixer.Sound(msc)
					self.msc.play(audio)
				elif msc.endswith('.ogg'):
					audio = pygame.mixer.Sound(msc)
					self.msc.play(audio)
			if self.transtype in [0,4] and self.transpeed < 0: self.transform = round(random.randint(200,300))
			if self.transtype == 5: self.transform = round(random.randint(1,2))
			if self.transtype in [1,4]:
				img = pygame.image.load('Backgrounds/tv_' + str(self.tv) + '.png').convert()
				self.rectrot = img.get_rect(center=pygame.Rect(0,0,600,400).center)

	def run(self):
		#RECTS
		flrects = []
		oprects = []
		for i in range(len(resources.FILES[1])):
			flrects.append(pygame.Rect(350,100 + (i * 51),230,50))
			oprects.append([])
			oprects[i].append(pygame.Rect(528,118 + (i * 51),24,24))
			oprects[i].append(pygame.Rect(550,118 + (i * 51),24,24))
		flrects.append(pygame.Rect(350,100 + (len(resources.FILES[1]) * 51),230,50))
		mrect = pygame.image.load('Sprites/cursor_' + str(resources.CURSOR) + '.png').get_rect()
		mrect.x = math.floor(pygame.mouse.get_pos()[0]/2)
		mrect.y = math.floor(pygame.mouse.get_pos()[1]/2)
		#EVENTS
		for event in pygame.event.get():
			#EXIT
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
				exit()
			#RESIZE
			if event.type == pygame.VIDEORESIZE:
				self.windoww = event.w
				self.windowh = event.h
				self.screen = pygame.display.set_mode((self.windoww, self.windowh), pygame.RESIZABLE)
				self.fnt = {'DEFAULT': pygame.font.SysFont('Calibri', math.floor(self.windoww/200) * 2)}
				self.display[1] = pygame.Surface((self.windoww, self.windowh), pygame.SRCALPHA)

			if self.mnu == 4 and self.n.ind == 7: self.mnu = 2
			#MOUSE
			if resources.MOUSE == True:
				self.pressed = pygame.mouse.get_pressed()
				#SKIP
				if self.pressed[0]:
					if self.mnu < 2: self.mnu += 1
					elif self.mnu == 5: self.skip = True
				if self.mnu < 3:
					self.lopt = -1
					for i in range(len(flrects)):
						if pygame.Rect.colliderect(mrect,flrects[i]) == True:
							self.lopt = i
							#FILE MENU
							if self.pressed[0] and self.winbar == 50:
								#SELECT GAME
								if i < len(resources.FILES[0]):
									if self.mnu < 3: self.mnu += 1
								#NEW GAME
								else:
									self.sfx.play(resources.SOUND['FILE_NEW'])
									resources.new_data()
									resources.save_data()
									resources.save_sett()
									resources.recent_data(2,self.lopt)
									pygame.mixer.music.fadeout(3000)
									self.msc.fadeout(3000)
									self.ton.fadeout(3000)
									self.mnu = 6
				elif self.mnu == 3: 
					self.opt = -1
					for i in range(len(oprects)):
						#LOAD GAME
						if pygame.Rect.colliderect(mrect,oprects[i][0]) == True:
							self.opt = 0
							if self.pressed[0]:
								resources.ID = self.lopt
								resources.load_data()
								pygame.mixer.music.stop()
								self.ton.play(resources.SOUND['NOISE'],-1)
								self.msc.stop()
								self.wait = 100
								self.mnu = 7
								self.tv = 0
						#DELETE GAME
						if pygame.Rect.colliderect(mrect,oprects[i][1]) == True:
							self.opt = 1
							if self.pressed[0]:
								resources.ID = self.lopt
								resources.delete_data()
								self.mnu -= 1
				if self.pressed[2]:
					if self.mnu == 3: self.mnu = 2
			#KEYBOARD
			if resources.MOUSE == False:
				self.pressed = pygame.key.get_pressed()
				if self.pressed[resources.ACT[0]]:
					#SKIP
					if self.mnu < 2: self.mnu += 1
					elif self.mnu == 5: self.skip = True
					#FILE MENU
					elif self.winbar == 50:
						#SELECT GAME
						if self.lopt < len(resources.FILES[0]):
							if self.mnu < 3: self.mnu += 1
							elif self.mnu == 3: 
								#LOAD GAME
								if self.opt == 0:
									resources.ID = self.lopt
									resources.load_data()
									pygame.mixer.music.stop()
									self.ton.play(resources.SOUND['NOISE'],-1)
									self.msc.stop()
									self.wait = 100
									self.mnu = 7
									self.tv = 0
								#DELETE GAME
								else:
									resources.ID = self.lopt
									resources.delete_data()
									self.mnu -= 1
						#NEW GAME
						else:
							self.sfx.play(resources.SOUND['FILE_NEW'])
							resources.new_data()
							resources.save_data()
							resources.save_sett()
							resources.recent_data(2,self.lopt)
							pygame.mixer.music.fadeout(3000)
							self.msc.fadeout(3000)
							self.ton.fadeout(3000)
							self.mnu = 6

				if self.pressed[resources.RUN[0]]:
					if self.mnu == 3: self.mnu = 2
				#SELECT
				if self.pressed[resources.UP[0]] and self.mnu == 2: self.lopt -= 1; self.sfx.play(resources.SOUND['MENU_HOR'])
				if self.pressed[resources.DOWN[0]] and self.mnu == 2: self.lopt += 1; self.sfx.play(resources.SOUND['MENU_VER'])

				if self.pressed[resources.LEFT[0]] and self.mnu == 3: self.opt = 0; self.sfx.play(resources.SOUND['MENU_HOR'])
				if self.pressed[resources.RIGHT[0]] and self.mnu == 3: self.opt = 1; self.sfx.play(resources.SOUND['MENU_VER'])
				#RANGE LIMIT
				if self.lopt < 0: self.lopt = len(resources.FILES[0])
				if self.lopt > len(resources.FILES[0]): self.lopt = 0
		for i in self.display: i.fill((0,0,0,0))
		rztxt = math.floor((self.windoww/300)/2)
		#RANDOM SCREEN
		if self.mnu != 5:
			if self.tv == 0:
				self.noise += 1
				if self.noise == 3: self.noise = 0
				self.display[0].blit(pygame.image.load('Backgrounds/noise_' + str(self.noise) + '.png'), (0, 0))
			else:
				self.transform += self.transpeed
				img = pygame.image.load('Backgrounds/tv_' + str(self.tv) + '.png').convert()
				#SCALE
				if self.transtype == 0:
					img = pygame.transform.scale(img,(img.get_rect().width + round(self.transform * 2),img.get_rect().height + round(self.transform * 2)))
					self.display[0].blit(img, (600 - img.get_rect().width, 600 - img.get_rect().height))
				#ROTATE
				elif self.transtype == 1:
					img = pygame.transform.scale(img,(800,800))
					trs = pygame.transform.rotate(img,self.transform)
					self.rectrot = trs.get_rect(center = self.rectrot.center)
					self.display[0].blit(trs, self.rectrot)
				#MOVE HORIZONTAL
				elif self.transtype == 2:
					self.display[0].blit(img, (self.transform, 0))
					if self.transform < 0: self.display[0].blit(img, (600 + self.transform, 0))
					if self.transform > 0: self.display[0].blit(img, (-600 + self.transform, 0))
				#MOVE VERTICAL
				elif self.transtype == 3:
					self.display[0].blit(img, (0, self.transform))
					if self.transform < 0: self.display[0].blit(img, (0, 600 + self.transform))
					if self.transform > 0: self.display[0].blit(img, (0, -600 + self.transform))
				#SCALE AND ROTATE
				if self.transtype == 4:
					img = pygame.transform.scale(img,(img.get_rect().width + round(self.transform/6),img.get_rect().height + round(self.transform/4)))
					trs = pygame.transform.rotate(img,self.transform)
					self.rectrot = trs.get_rect(center = self.rectrot.center)
					self.display[0].blit(trs, self.rectrot)
				#RANDOM
				if self.transtype == 5:
					if self.transform > 17: self.transform = 1
					img = pygame.image.load('Backgrounds/tv_' + str(self.transform) + '.png').convert()
					self.display[0].blit(img, (0,0))
		#FILES MENU
		if self.mnu < 5:
			for i in range(len(resources.FILES[1])):
				if self.lopt == i: col = (255,255,0)
				else: col = (255,255,255)
				pygame.draw.rect(self.display[0], col, flrects[i])
				self.display[1].blit(self.fnt['DEFAULT'].render(database.CHAPTERS[resources.FILES[1][i]][0], True, (0,0,0)), (370 * rztxt, (110 + (i * 51)) * rztxt))
				ss = math.floor(resources.FILES[2][i]/1000)
				mm = 0
				hh = 0
				while ss > 60: ss -= 60; mm += 1
				while mm > 60: mm -= 60; hh += 1
				if ss < 10: ss = '0' + str(ss)
				else: ss = str(ss)
				if mm < 10: mm = '0' + str(mm)
				else: mm = str(mm)
				if hh < 10: hh = '0' + str(hh)
				else: hh = str(hh)
				self.display[1].blit(self.fnt['DEFAULT'].render(hh + ' : ' + mm + ' : ' + ss, True, (0, 0, 0)), (370 * rztxt, (130 + (i * 51)) * rztxt))

				if self.mnu > 2 and self.lopt == i:
					if self.opt == 0: pygame.draw.rect(self.display[0], (255,255,255), oprects[i][0])
					if self.opt == 1: pygame.draw.rect(self.display[0], (255,255,255), oprects[i][1])
					self.display[0].blit(pygame.image.load('Sprites/tc_7.png'), (530, 120 + (i * 51)))
					self.display[0].blit(pygame.image.load('Sprites/tc_8.png'), (552, 120 + (i * 51)))
				else:
					x = 0
					for p in resources.FILES[4][i][::-1]:
						self.display[0].blit(pygame.image.load('Sprites/who_' + str(p) + '.png'), (550 - x, 120 + (i * 51)))
						x += 22
				resources.ID = self.lopt

			if self.lopt == len(resources.FILES[0]): col = (255,255,0)
			else: col = (255,255,255)
			pygame.draw.rect(self.display[0], col, flrects[len(resources.FILES[1])])
			self.display[1].blit(self.fnt['DEFAULT'].render(database.MENU[61], True, (0,0,0)), (420 * rztxt, (120 + (len(resources.FILES[1]) * 51)) * rztxt))
		#RECAP
		if self.mnu == 5:
			lt = 0
			self.display[0].blit(pygame.image.load('Backgrounds/recap_' + str(resources.CHAPTER) + '.png'), (0, -self.scroll))
			for y in database.CHAPTERS[resources.CHAPTER - 1][2]:
				self.display[1].blit(self.fnt['DEFAULT'].render(y, True, (0,0,0)), (101 * rztxt, 1 + (360 - math.floor(self.scroll * 2) + lt) * rztxt))
				self.display[1].blit(self.fnt['DEFAULT'].render(y, True, (0,0,0)), (102 * rztxt, 2 + (360 - math.floor(self.scroll * 2) + lt) * rztxt))
				self.display[1].blit(self.fnt['DEFAULT'].render(y, True, (255,255,255)), (100 * rztxt, (360 - math.floor(self.scroll * 2) + lt) * rztxt))
				lt += 20
			self.scroll += 1
			if self.scroll > 340 + lt or self.skip == True:
				if self.winbar == 50:
					self.msc.fadeout(5000)
					self.mnu = 6
		if self.mnu == 6:
			if self.winbar < 210:
				self.winbar += 5
			if self.winbar == 210:
				self.classrun = False
		#BLACK BARS
		pygame.draw.rect(self.display[1], (0, 0, 0), pygame.Rect(0,0,1200,self.winbar * 2))
		pygame.draw.rect(self.display[1], (0, 0, 0), pygame.Rect(0,800,1200,-self.winbar * 2))
		#INFO
		if self.mnu > 0 and self.mnu < 5:
			self.display[1].blit(self.fnt['DEFAULT'].render(database.ABOUT[0] + ' ' + resources.VERSION, True, (240,240,240)), ((-35 + self.winbar) * rztxt, (-35 + self.winbar) * rztxt))
			self.display[1].blit(self.fnt['DEFAULT'].render(database.ABOUT[1], True, (240,240,240)), ((530 - self.winbar) * rztxt, (420 - self.winbar) * rztxt))
			#HOLIDAYS
			for i in database.HOLIDAYS:
				if self.holiday.month == i[0] and self.holiday.day == i[1]:
					self.display[1].blit(self.fnt['DEFAULT'].render(i[2], True, (240,240,240)), (960, 10))
		#WAIT
		if self.mnu > 0 and self.mnu < 6:
			if self.wait > 0: self.wait -= 1
			prb = round(random.randint(0,100))
			if prb > 50 and self.wait == 0 and self.tv > 0: self.random()
		if self.mnu == 7:
			if self.wait > 0: self.wait -= 1
			prb = round(random.randint(0,100))
			if prb > 50 and self.wait == 0 and self.tv == 0:
				self.msc.play(resources.SONGS['FATE_OCCURRENCES'],-1)
				self.ton.stop()
				self.mnu = 5
		#DRAW SURFACES
		self.screen.blit(pygame.transform.scale(self.display[0], (self.windoww, self.windowh)), (0, 0))
		#self.screen.blit(pygame.transform.scale(self.display[1], (self.windoww, self.windowh)), (0, 0))
		self.screen.blit(self.display[1], (0, 0))
		#LOGO
		if self.mnu == 0:
			srf = pygame.Surface((600,400))
			srf.blit(pygame.image.load('Backgrounds/logo.png'), (0, 0))
			srf.set_alpha(self.logoalpha)
			self.screen.blit(srf, (300,200))
		#MOUSE
		if resources.MOUSE == True:
			self.screen.blit(pygame.image.load('Sprites/cursor_' + str(resources.CURSOR) + '.png'), pygame.mouse.get_pos())
		#UPDATE
		pygame.display.flip()
		self.glock.tick(self.FPS)

class Game:
	def __init__(self):
		#GAME SETTINGS
		self.screen = pygame.display.set_mode((1200, 800), pygame.RESIZABLE | pygame.DOUBLEBUF)
		self.display = [pygame.Surface((600, 400)), pygame.Surface((1200, 800), pygame.SRCALPHA),
			pygame.Surface((600, 400), pygame.SRCALPHA), pygame.Surface((1200, 800), pygame.SRCALPHA)]
		self.displayzw = 600
		self.displayzh = 400
		self.displayx = 0
		self.displayy = 0
		self.windoww = 1200
		self.windowh = 800
		self.glock = pygame.time.Clock()
		self.FPS = 60
		self.fnt = {'DEFAULT': pygame.font.SysFont('Calibri', 30), 'ALT': pygame.font.Font('Fonts/PrestigeEliteStd.otf', 30),
			'MININFO': pygame.font.Font('Fonts/pixel-font.ttf', 25), 'MONOTYPE': pygame.font.Font('Fonts/monotype.ttf', 15),
			'CONTROLKEYS': pygame.font.Font('Fonts/controlkeys.ttf', 15)}
		self.cam = pygame.Rect(0,0,self.displayzw,self.displayzh)
		self.driving = 0
		self.sleepin = False
		self.tilemation = 0
		self.room = ''
		self.rectdebug = False
		self.classrun = 1
		self.scrmov = None
		self.scrspd = 0
		self.hpctrl = []
		self.waitime = 0
		self.waitlst = [['advice',432000],['rain',3600]]
		#MIXER CHANNELS
		pygame.mixer.init(frequency = 44100, size = -16, channels = 1, buffer = 2**12)
		self.ch_sfx = pygame.mixer.Channel(0) #for quick sounds
		self.ch_sfx.set_volume(resources.SFX)
		self.ch_msc = pygame.mixer.Channel(1) #for background ambience loops
		self.ch_msc.set_volume(resources.MSC)
		self.ch_ton = pygame.mixer.Channel(2) #for long sounds or jingles
		self.ch_ton.set_volume(resources.SFX)
		self.ch_rad = pygame.mixer.Channel(3) #for radio songs
		self.ch_rad.set_volume(0.1)
		self.ch_stp = pygame.mixer.Channel(4) #for steps sounds
		self.ch_stp.set_volume(resources.SFX)
		self.ch_rng = pygame.mixer.Channel(5) #for phone ringtone
		self.ch_rng.set_volume(resources.MSC)
		self.ch_dlg = pygame.mixer.Channel(6) #for dialog text sound
		self.ch_dlg.set_volume(resources.SFX)
		#MENU VARIABLES
		self.phn = menu.Phone()
		self.inv = menu.Inventory()
		self.shpmnu = menu.Shop()
		self.nmenu = menu.Naming()
		self.dmenu = None
		self.opt = 1
		self.lopt = 0
		self.mnu = 1
		self.exvar = 0
		self.inventory = 0
		self.invfade = 1050
		self.phone = 0
		self.phofa = 0
		self.nb = ''
		self.shp = False
		self.basket = []
		self.products = []
		self.extract = [0,0,0,0,0,0]
		self.promo = 0
		self.winbar = 210
		self.radonoff = False
		self.rdscroll = 10
		self.fm = 0
		self.vm = 0.5
		self.msc = 0
		self.signal = 0
		self.nottxt = ''
		self.notcol = (0,0,0)
		self.notx = 0
		self.tutorial = {'TEXT': [], 'OUTPUT': [], 'FADE': 0, 'TIME': 0, 'WAIT': 0, 'NEXT': '','GO': 0}
		self.cityname = ''
		#BATTLE VARIABLES
		self.dlg = []
		self.dlgfa = 500
		self.dlgy = 0
		self.dmginfo = ''
		self.dmgy = 200
		self.dlgspd = resources.SPEED
		self.speakin = 0
		self.equip = []
		self.battle = False
		self.effttack = None
		self.effgif = 0
		self.btime = 100
		self.bbg = ''
		self.bbm = 0
		self.obstacles = False
		self.hits = 0
		self.tdmg = 0
		self.hpl = 0
		self.tbt = 0
		self.turn = -1
		self.aim = pygame.Rect(300,200,30,30)
		self.barhp = []
		self.barpp = []
		self.barxp = []
		#BARS
		x = 0
		for i in resources.PARTY[resources.FORMATION]:
			#HP BAR
			resources.CHARACTERS[i]['HP'] = database.CLASSES[resources.CHARACTERS[i]['CLASS']]['VITALITY'][resources.CHARACTERS[i]['LEVEL']]
			self.barhp.append(int(100/(database.CLASSES[resources.CHARACTERS[i]['CLASS']]['VITALITY'][resources.CHARACTERS[i]['LEVEL']]/resources.CHARACTERS[i]['HP'])))
			#XP BAR
			if resources.CHARACTERS[i]['XP'] > 0: self.barxp.append(int(100/(database.NEXTLEVEL[resources.CHARACTERS[i]['LEVEL']]/resources.CHARACTERS[i]['XP'])))
			else: self.barxp.append(0)
			#AMMO BAR
			self.equip.append(0)
			self.barpp.append([])
			for j in resources.INVENTORY[i][4][1:]:
				if j[0] != '_':
					if j[0].startswith('gun') and int(j[1]) > 0: b = int(100/(database.ITEMS[j[0]][5]['CAPACITY']/int(j[1])))
					else: b = 0
					self.barpp[x].append(b)
				else:
					self.barpp[x].append(0)
			x += 1
		#PLAYER
		self.player = []
		for i in range(len(resources.PARTY[resources.FORMATION])):
			self.player.append({'RECT': pygame.Rect(resources.PX + (i * 30),resources.PY,20,20),'SPEED': 0,'JUMP': 0,'GRAVITY': -5,'STEP': 10,'SWIM': None,
		'HEAD': 'BLANKD_' + resources.CHARACTERS[resources.PARTY[resources.FORMATION][i]]['HAIR'] + resources.CHARACTERS[resources.PARTY[resources.FORMATION][i]]['SKIN'],
		'SPRITE': 'STANDD_' + resources.CHARACTERS[resources.PARTY[resources.FORMATION][i]]['COSTUME'] + resources.CHARACTERS[resources.PARTY[resources.FORMATION][i]]['SKIN'],
		'GIF': 0.0,'BLINK': 100,'DMGTIM': 100,'SHK': 0,'DIRECTION': 3,'PAUSE': 0,'FOLLOW': None,'FOLLEND': 0,'FOLLMOV': '','PLAYING': False,'NODES': [],'HOLD': None})
		self.player[0]['PLAYING'] = True
		self.objects = []
		self.tilrect = []
		self.tilhide = False
		self.tilalpha = 0
		#MAP VARIABLES
		self.en = []
		self.foe = []
		self.fig = []
		self.mrc = []
		self.npcs = []
		self.vehicles = []
		self.portals = []
		self.signs = []
		self.lights = []
		self.particles = []
		self.portalgo = {}
		#STARTING GAME
		if resources.CHAPTER == 0 and resources.SCENE == 0:
			self.tutorial = {'TEXT': database.TUTORIALS['BEGIN'], 'OUTPUT': [], 'FADE': 0, 'TIME': 0, 'WAIT': 300, 'NEXT': '','GO': 0}
			for j in self.tutorial['TEXT']:
				if isinstance(j,list):
					if j[0] == 'phone':
						self.tutorial['GO'] = j[1]
					if j[0] == 'wait':
						self.tutorial['WAIT'] = j[1]
						if len(j) > 2: self.tutorial['NEXT'] = j[2]
				else: self.tutorial['OUTPUT'].append(j)
			self.player[0]['PAUSE'] = 1
			self.rendermap('hauntedhouse_0')
			self.phone = 15
			self.mnu = 1
		else: self.rendermap('1urban_0')

	def people(self, i, t):
		#ANIMATION
		if i['PAUSE'] < 2: i['GIF'] += 0.5
		if i['GIF'] >= len(resources.SPRITES[i['SPRITE']]): i['GIF'] = 0
		if i['PAUSE'] < 2: i['BLINK'] -= 1
		if i['BLINK'] < 0: i['BLINK'] = round(random.randint(30,90))
		#JUMP
		if i['GRAVITY'] > -5:
			i['JUMP'] += i['GRAVITY']
			i['GRAVITY'] -= 0.5
		if i['SPRITE'].startswith('SLEEP') == False:
			#MAP ICON
			if resources.MAP == 0:
				self.display[0].blit(pygame.image.load('Sprites/mp_player.png'), (i['RECT'].x - self.cam.x, i['RECT'].y - self.cam.y))
			else:
				xsp = 0
				#BODY AND SHADE
				if i['SWIM'] == None:
					if i['SPRITE'].startswith('SEAT') == False or i['SPRITE'].startswith('DRIVE') == False:
						self.display[0].blit(pygame.image.load('Sprites/Items/it_shade.png'), (i['RECT'].x - self.cam.x - 1,i['RECT'].y - self.cam.y + 7))
					img = resources.SPRITES[i['SPRITE']][math.floor(i['GIF'])]
					if self.turn == -6: img.fill((10,10,10),None,pygame.BLEND_RGBA_MULT)
					self.display[0].blit(img, (i['RECT'].x - self.cam.x + math.floor((20 - img.get_rect().width)/2),i['RECT'].y - self.cam.y - 10 - int(i['JUMP'])))
				#SWIMMING
				else:
					xsp += 21
					i['SWIM'] += 0.1
					if i['SWIM'] > 1.5: i['SWIM'] = 0.0
					self.display[0].blit(pygame.image.load('Sprites/water_' + str(math.floor(i['SWIM'])) + '.png'), (i['RECT'].x - self.cam.x + 4,i['RECT'].y - self.cam.y + 9))
				#HOLDING ITEM
				if i['HOLD'] != None:
					xx = -5; yy = -20
					if i['DIRECTION'] in [1,2,8]: xx = 10
					if i['DIRECTION'] in [4,5,6]: xx = -20
					if i['DIRECTION'] in [2,3,4]: yy = 5
					if i['DIRECTION'] in [6,7,8]: yy = -30
					self.tilrect[2][i['HOLD']][1].x = i['RECT'].x + xx
					self.tilrect[2][i['HOLD']][1].y = i['RECT'].y + yy
				#EXTRA SPACEMENT
				if i['SPEED'] == 0 and i['GIF'] >= 1.0 and i['GIF'] < 3.0: xsp += 1
				if i['SPEED'] > 0:
					if i['GIF'] >= 0.0 and i['GIF'] < 1.0: pass
					elif i['GIF'] >= 4.0 and i['GIF'] < 5.0: pass
					else: xsp += 1
				if i['JUMP'] > 0: xsp = 1
				if i['HEAD'].startswith('BLANKDD'): xsp += 1
				#HEAD
				if i['BLINK'] < 2 and i['DIRECTION'] < 6 and i['GRAVITY'] == -5 and i['JUMP'] == 0:
					try: img = resources.SPRITES[i['HEAD']][1]
					except: img = resources.SPRITES[i['HEAD']][0]
				else: img = resources.SPRITES[i['HEAD']][0]
				if self.turn == -6: img.fill((10,10,10),None,pygame.BLEND_RGBA_MULT)
				xx = i['RECT'].x - self.cam.x + math.floor((20 - img.get_rect().width)/2)
				yy = i['RECT'].y - self.cam.y - 21 + xsp - i['JUMP']
				self.display[0].blit(img, (xx,yy))
				#MOUTH
				if self.speakin == i['RECT'] and i['DIRECTION'] < 6:
					if i['DIRECTION'] == 1: ex1 = (0,1); ex2 = (1,1)
					elif i['DIRECTION'] == 2: ex1 = (4,6); ex2 = (4,5)
					elif i['DIRECTION'] == 3: ex1 = (4,6); ex2 = (5,6)
					elif i['DIRECTION'] == 4: ex1 = (3,5); ex2 = (4,5)
					elif i['DIRECTION'] == 5: ex1 = (8,9); ex2 = (8,8)
					pygame.draw.line(self.display[0],(81,9,0),(xx + ex1[0],yy + 9),(xx + ex1[1],yy + 9))
					if math.floor(i['GIF']) == 0: pygame.draw.line(self.display[0],(183,63,47),(xx + ex2[0],yy + 10),(xx + ex2[1],yy + 10))
					if math.floor(i['GIF']) == 1: pygame.draw.line(self.display[0],(183,63,47),(xx + ex2[0],yy + 9),(xx + ex2[1],yy + 9))
				#ACCESORIES
				if t == True and resources.CHARACTERS[resources.PARTY[resources.FORMATION][0]]['ACCESORIES'] != None and int(i['DIRECTION']) < 6:
					if i['DIRECTION'] == 1: ex = 8
					elif i['DIRECTION'] == 2: ex = 3
					elif i['DIRECTION'] == 3: ex = 2
					elif i['DIRECTION'] == 4: ex = 1
					elif i['DIRECTION'] == 5: ex = 1
					else: ex = 0
					if i['DIRECTION'] == 1: acc = pygame.transform.flip(pygame.image.load('Sprites/Characters/' + resources.CHARACTERS[resources.PARTY[resources.FORMATION][0]]['ACCESORIES'] + '_1.png'),True,False)
					elif i['DIRECTION'] == 5: acc = pygame.image.load('Sprites/Characters/' + resources.CHARACTERS[resources.PARTY[resources.FORMATION][0]]['ACCESORIES'] + '_1.png')
					else: acc = pygame.image.load('Sprites/Characters/' + resources.CHARACTERS[resources.PARTY[resources.FORMATION][0]]['ACCESORIES'] + '_0.png')
					if self.turn == -6: acc.fill((10,10,10),None,pygame.BLEND_RGBA_MULT)
					self.display[0].blit(acc, (i['RECT'].x - self.cam.x + math.floor((20 - img.get_rect().width)/2) + ex,i['RECT'].y - self.cam.y - 21 + xsp - int(i['JUMP']) + 7))

	def enemy(self, i):
		#DRAW
		if self.colide(i['RECT'], self.cam):
			if self.rectdebug == True: pygame.draw.rect(self.display[0], (255,0,0), pygame.Rect(i['RECT'].x - self.cam.x, i['RECT'].y - self.cam.y, i['RECT'].width, i['RECT'].height))
			img = pygame.image.load('Sprites/frk_' + (i['FILE']) + '_mini.png')
			for b in resources.BESTIARY:
				if b['N'] == i['FILE'] and b['SEEN'] == 0 and i['TYPE'] != 'mercenary':
					img.fill((10,10,10),None,pygame.BLEND_RGBA_MULT)
			self.display[0].blit(img, (i['RECT'].x - self.cam.x, i['RECT'].y - self.cam.y))
			if i['PATH'] == 'notice': self.display[0].blit(pygame.image.load('Sprites/notice.png'), (i['RECT'].x - self.cam.x, i['RECT'].y - self.cam.y - 30))
		#REPELLENT
		rplt = False
		for c in resources.PARTY[resources.FORMATION]:
			if resources.CHARACTERS[c]['HEALTH'] == 2: rplt = True
		#MOVEMENT
		if self.winbar == 0 and self.battle == False and i['FIGHTING'] == False:
			#NOTICING
			if i['PATH'] == 'notice':
				if i['TIME'] == 0:
					i['PATH'] = 'follow'
			#STEALTH MOVEMENT
			elif i['PATH'] == 'stealth':
				if self.facing(i,self.player[0]) == 2 and rplt == False:
					self.ch_sfx.play(resources.SOUND['NOTICED'])
					i['PATH'] = 'notice'
					i['TIME'] = 10
				else:
					if i['DIRECTION'] == 0:
						i['DIRECTION'] = 1

					if i['TIME'] == 0:
						if i['DIRECTION'] == 1: i['DIRECTION'] = 5
						elif i['DIRECTION'] == 5: i['DIRECTION'] = 1
						i['TIME'] = 20
			#FOLLOW MOVEMENT
			elif i['PATH'] == 'follow':
				if i['RECT'].y - self.cam.y > self.player[0]['RECT'].y - 5 - self.cam.y:
					if i['RECT'].x - self.cam.x < self.player[0]['RECT'].x + 10 - self.cam.x: i['DIRECTION'] = 8
					elif i['RECT'].x - self.cam.x > self.player[0]['RECT'].x + 10 - self.cam.x: i['DIRECTION'] = 6
					else: i['DIRECTION'] = 7

				elif i['RECT'].y - self.cam.y < self.player[0]['RECT'].y - 5 - self.cam.y: 
					if i['RECT'].x - self.cam.x < self.player[0]['RECT'].x + 10 - self.cam.x: i['DIRECTION'] = 2
					elif i['RECT'].x - self.cam.x > self.player[0]['RECT'].x + 10 - self.cam.x: i['DIRECTION'] = 4
					else: i['DIRECTION'] = 3

				elif i['RECT'].x - self.cam.x < self.player[0]['RECT'].x + 10 - self.cam.x:
					if i['RECT'].y - self.cam.y > self.player[0]['RECT'].y - 5 - self.cam.y: i['DIRECTION'] = 8
					elif i['RECT'].y - self.cam.y < self.player[0]['RECT'].y - 5 - self.cam.y: i['DIRECTION'] = 2
					else: i['DIRECTION'] = 1

				elif i['RECT'].x - self.cam.x > self.player[0]['RECT'].x + 10 - self.cam.x:
					if i['RECT'].y - self.cam.y > self.player[0]['RECT'].y - 5 - self.cam.y: i['DIRECTION'] = 6
					elif i['RECT'].y - self.cam.y < self.player[0]['RECT'].y - 5 - self.cam.y: i['DIRECTION'] = 4
					else: i['DIRECTION'] = 5
				if rplt == True:
					i['PATH'] = 'horizontal'
					i['DIRECTION'] = 0
					i['TIME'] = 20
			#HORIZONTAL MOVEMENT
			elif i['PATH'] == 'horizontal':
				if i['DIRECTION'] == 0:
					i['DIRECTION'] = 1
				if i['TIME'] == 0:
					if i['DIRECTION'] == 1: i['DIRECTION'] = 5
					elif i['DIRECTION'] == 5: i['DIRECTION'] = 1
					i['TIME'] = 20
			#MOVING
			if self.player[0]['PAUSE'] < 3:
				if i['DIRECTION'] == 1: i['RECT'].x += i['AGILITY'] - 1
				if i['DIRECTION'] == 2: i['RECT'].x += i['AGILITY'] - 1; i['RECT'].y += i['AGILITY'] - 1
				if i['DIRECTION'] == 3: i['RECT'].y += i['AGILITY'] - 1
				if i['DIRECTION'] == 4: i['RECT'].x -= i['AGILITY'] - 1; i['RECT'].y += i['AGILITY'] - 1
				if i['DIRECTION'] == 5: i['RECT'].x -= i['AGILITY'] - 1
				if i['DIRECTION'] == 6: i['RECT'].x -= i['AGILITY'] - 1; i['RECT'].y -= i['AGILITY'] - 1
				if i['DIRECTION'] == 7: i['RECT'].y -= i['AGILITY'] - 1
				if i['DIRECTION'] == 8: i['RECT'].x += i['AGILITY'] - 1; i['RECT'].y -= i['AGILITY'] - 1
				i['TIME'] -= 1
		#BATTLE ENTER
		if self.colide(i['RECT'], self.player[0]['RECT']) == True and i['DIRECTION'] > 0 and self.battle == False and self.dlgfa == 500:
			if i['FIGHTING'] == False and rplt == False:
				if i['TYPE'] != 'mercenary': self.foe.append(i)
				else: self.mrc.append(i)
				i['FIGHTING'] = True
				if (len(self.foe) + len(self.mrc)) == 1:
					for b in resources.BESTIARY:
						if b['N'] == i['FILE'] and b['SEEN'] == 0 and i['TYPE'] != 'mercenary':
							self.aim.x = i['MASK'].x
							self.turn = -6
							break
					self.notx = 0
					if self.phone > 0: self.turn = -2
					if self.inventory > 0: self.turn = -2
					if self.turn != -6: self.turn = -self.facing(i,self.player[0])
					self.fight()

	def npc(self, i):
		if i['RECT'].width > 0: rect = pygame.Rect(i['RECT'].x,i['RECT'].y,i['RECT'].width,i['RECT'].height)
		else: rect = pygame.Rect(i['RECT'].x,i['RECT'].y,20,20)

		#DRAW
		if self.rectdebug == True: pygame.draw.rect(self.display[0], (255,0,0), pygame.Rect(rect.x - self.cam.x, rect.y - self.cam.y, rect.width, rect.height))
		if self.battle == False and self.colide(rect, self.cam):
			if i['TYPE'] not in [1,5] and i['RECT'].width == 0: self.people(i,False)
			elif i['TYPE'] == 3:
				img = pygame.image.load('Sprites/mercator.png')
				self.display[0].blit(img, (rect.x - self.cam.x - math.floor(img.get_rect().width/2) + 10, rect.y - self.cam.y - int(img.get_rect().height/2) - 3))
			elif i['TYPE'] == 5:
				self.display[0].blit(pygame.image.load('Sprites/obj_' + str(i['INDEX']) + str(i['WHO']) + '.png'), (rect.x - self.cam.x, rect.y - self.cam.y - 10))
				if self.sleepin == True and i['INDEX'] == 1: self.display[0].blit(pygame.image.load('Sprites/char_0_rest.png'), (rect.x - self.cam.x + 5, rect.y - self.cam.y + 5))
		#FOLLOW
		if i['FOLLOW'] != None and i['FOLLOW'] != (None,None):
			i['SPEED'] = 3
			if i['RECT'].y - self.cam.y > i['FOLLOW'].y - self.cam.y:
				if i['RECT'].x - self.cam.x < i['FOLLOW'].x - self.cam.x: i['DIRECTION'] = 8
				elif i['RECT'].x - self.cam.x > i['FOLLOW'].x - self.cam.x: i['DIRECTION'] = 6
				else: i['DIRECTION'] = 7

			elif i['RECT'].y - self.cam.y < i['FOLLOW'].y - self.cam.y: 
				if i['RECT'].x - self.cam.x < i['FOLLOW'].x - self.cam.x: i['DIRECTION'] = 2
				elif i['RECT'].x - self.cam.x > i['FOLLOW'].x - self.cam.x: i['DIRECTION'] = 4
				else: i['DIRECTION'] = 3

			elif i['RECT'].x - self.cam.x < i['FOLLOW'].x - self.cam.x:
				if i['RECT'].y - self.cam.y > i['FOLLOW'].y - self.cam.y: i['DIRECTION'] = 8
				elif i['RECT'].y - self.cam.y < i['FOLLOW'].y - self.cam.y: i['DIRECTION'] = 2
				else: i['DIRECTION'] = 1

			elif i['RECT'].x - self.cam.x > i['FOLLOW'].x - self.cam.x:
				if i['RECT'].y - self.cam.y > i['FOLLOW'].y - self.cam.y: i['DIRECTION'] = 6
				elif i['RECT'].y - self.cam.y < i['FOLLOW'].y - self.cam.y: i['DIRECTION'] = 4
				else: i['DIRECTION'] = 5
		#HORIZONTAL
		if self.battle == False and i['TYPE'] == 0 and i['RECT'].width == 0 and i['FOLLOW'] == None:
			if i['MOVE'] == 'horizontal':
				i['SPEED'] = 1
				if i['DIRECTION'] not in [1,5]:
					i['DIRECTION'] = 1

				if i['TIME'] == 0:
					if i['DIRECTION'] == 1: i['DIRECTION'] = 5
					elif i['DIRECTION'] == 5: i['DIRECTION'] = 1
					i['TIME'] = 30
				i['TIME'] -= 1
			elif i['MOVE'] == 'nodeon':
				i['SPEED'] = 1
				for n in self.nodes:
					if self.colide(rect,n['RECT']):
						if n['GOING'] == 1: i['DIRECTION'] = n['TYPE']
			elif i['MOVE'] == 'nodeoff':
				i['SPEED'] = 1
				for n in self.nodes:
					if self.colide(rect,n['RECT']):
						if n['GOING'] == 0: i['DIRECTION'] = n['TYPE']
			elif i['MOVE'] == 'fixed': i['SPEED'] = 0
		#MOVEMENT
		if self.player[0]['PAUSE'] < 3:
			if i['SPEED'] > 0:
				if i['DIRECTION'] == 1: i['HEAD'] = 'BLANKR_' + i['INDEX'][0:3] + i['INDEX'][5]; i['SPRITE'] = 'WALKR_' + i['INDEX'][3:6]; i['RECT'].x += i['SPEED']
				if i['DIRECTION'] == 2: i['HEAD'] = 'BLANKRD_' + i['INDEX'][0:3] + i['INDEX'][5]; i['SPRITE'] = 'WALKRD_' + i['INDEX'][3:6]; i['RECT'].x += i['SPEED']; i['RECT'].y += i['SPEED']
				if i['DIRECTION'] == 3: i['HEAD'] = 'BLANKD_' + i['INDEX'][0:3] + i['INDEX'][5]; i['SPRITE'] = 'WALKD_' + i['INDEX'][3:6]; i['RECT'].y += i['SPEED']
				if i['DIRECTION'] == 4: i['HEAD'] = 'BLANKLD_' + i['INDEX'][0:3] + i['INDEX'][5]; i['SPRITE'] = 'WALKLD_' + i['INDEX'][3:6]; i['RECT'].x -= i['SPEED']; i['RECT'].y += i['SPEED']
				if i['DIRECTION'] == 5: i['HEAD'] = 'BLANKL_' + i['INDEX'][0:3] + i['INDEX'][5]; i['SPRITE'] = 'WALKL_' + i['INDEX'][3:6]; i['RECT'].x -= i['SPEED']
				if i['DIRECTION'] == 6: i['HEAD'] = 'BLANKLU_' + i['INDEX'][0:3] + i['INDEX'][5]; i['SPRITE'] = 'WALKLU_' + i['INDEX'][3:6]; i['RECT'].x -= i['SPEED']; i['RECT'].y -= i['SPEED']
				if i['DIRECTION'] == 7: i['HEAD'] = 'BLANKU_' + i['INDEX'][0:3] + i['INDEX'][5]; i['SPRITE'] = 'WALKU_' + i['INDEX'][3:6]; i['RECT'].y -= i['SPEED']
				if i['DIRECTION'] == 8: i['HEAD'] = 'BLANKRU_' + i['INDEX'][0:3] + i['INDEX'][5]; i['SPRITE'] = 'WALKRU_' + i['INDEX'][3:6]; i['RECT'].x += i['SPEED']; i['RECT'].y -= i['SPEED']
			elif i['MOVE'] == 'stand':
				if i['DIRECTION'] == 1: i['HEAD'] = 'BLANKR_' + i['INDEX'][0:3] + i['INDEX'][5]; i['SPRITE'] = 'STANDR_' + i['INDEX'][3:6]
				if i['DIRECTION'] == 2: i['HEAD'] = 'BLANKRD_' + i['INDEX'][0:3] + i['INDEX'][5]; i['SPRITE'] = 'STANDRD_' + i['INDEX'][3:6]
				if i['DIRECTION'] == 3: i['HEAD'] = 'BLANKD_' + i['INDEX'][0:3] + i['INDEX'][5]; i['SPRITE'] = 'STANDD_' + i['INDEX'][3:6]
				if i['DIRECTION'] == 4: i['HEAD'] = 'BLANKLD_' + i['INDEX'][0:3] + i['INDEX'][5]; i['SPRITE'] = 'STANDLD_' + i['INDEX'][3:6]
				if i['DIRECTION'] == 5: i['HEAD'] = 'BLANKL_' + i['INDEX'][0:3] + i['INDEX'][5]; i['SPRITE'] = 'STANDL_' + i['INDEX'][3:6]
				if i['DIRECTION'] == 6: i['HEAD'] = 'BLANKLU_' + i['INDEX'][0:3] + i['INDEX'][5]; i['SPRITE'] = 'STANDLU_' + i['INDEX'][3:6]
				if i['DIRECTION'] == 7: i['HEAD'] = 'BLANKU_' + i['INDEX'][0:3] + i['INDEX'][5]; i['SPRITE'] = 'STANDU_' + i['INDEX'][3:6]
				if i['DIRECTION'] == 8: i['HEAD'] = 'BLANKRU_' + i['INDEX'][0:3] + i['INDEX'][5]; i['SPRITE'] = 'STANDRU_' + i['INDEX'][3:6]
				i['MOVE'] = 'fixed'
			elif i['MOVE'] == 'seat':
				if i['DIRECTION'] == 1: i['HEAD'] = 'BLANKR_' + i['INDEX'][0:3] + i['INDEX'][5]; i['SPRITE'] = 'SEATR_' + i['INDEX'][3:6]
				if i['DIRECTION'] == 2: i['HEAD'] = 'BLANKRD_' + i['INDEX'][0:3] + i['INDEX'][5]; i['SPRITE'] = 'SEATRD_' + i['INDEX'][3:6]
				if i['DIRECTION'] == 3: i['HEAD'] = 'BLANKD_' + i['INDEX'][0:3] + i['INDEX'][5]; i['SPRITE'] = 'SEATD_' + i['INDEX'][3:6]
				if i['DIRECTION'] == 4: i['HEAD'] = 'BLANKLD_' + i['INDEX'][0:3] + i['INDEX'][5]; i['SPRITE'] = 'SEATLD_' + i['INDEX'][3:6]
				if i['DIRECTION'] == 5: i['HEAD'] = 'BLANKL_' + i['INDEX'][0:3] + i['INDEX'][5]; i['SPRITE'] = 'SEATL_' + i['INDEX'][3:6]
				if i['DIRECTION'] == 6: i['HEAD'] = 'BLANKLU_' + i['INDEX'][0:3] + i['INDEX'][5]; i['SPRITE'] = 'SEATLU_' + i['INDEX'][3:6]
				if i['DIRECTION'] == 7: i['HEAD'] = 'BLANKU_' + i['INDEX'][0:3] + i['INDEX'][5]; i['SPRITE'] = 'SEATU_' + i['INDEX'][3:6]
				if i['DIRECTION'] == 8: i['HEAD'] = 'BLANKRU_' + i['INDEX'][0:3] + i['INDEX'][5]; i['SPRITE'] = 'SEATRU_' + i['INDEX'][3:6]
			else:
				if i['DIRECTION'] == 1: i['SPRITE'] = 'STANDR_' + i['INDEX'][3:6]
				if i['DIRECTION'] == 2: i['SPRITE'] = 'STANDRD_' + i['INDEX'][3:6]
				if i['DIRECTION'] == 3: i['SPRITE'] = 'STANDD_' + i['INDEX'][3:6]
				if i['DIRECTION'] == 4: i['SPRITE'] = 'STANDLD_' + i['INDEX'][3:6]
				if i['DIRECTION'] == 5: i['SPRITE'] = 'STANDL_' + i['INDEX'][3:6]
				if i['DIRECTION'] == 6: i['SPRITE'] = 'STANDLU_' + i['INDEX'][3:6]
				if i['DIRECTION'] == 7: i['SPRITE'] = 'STANDU_' + i['INDEX'][3:6]
				if i['DIRECTION'] == 8: i['SPRITE'] = 'STANDRU_' + i['INDEX'][3:6]

			if i['FOLLOW'] != None:
				if i['FOLLOW'] != (None,None):
					if self.colide(rect,i['FOLLOW']):
						if i['FOLLMOV'] != '': i['MOVE'] = i['FOLLMOV']
						i['DIRECTION'] = i['FOLLEND']
						i['FOLLOW'] = None
						i['FOLLEND'] = 0
						i['FOLLMOV'] = ''
						i['SPEED'] = 0
				else:
					if i['FOLLMOV'] != '': i['MOVE'] = i['FOLLMOV']
					i['DIRECTION'] = i['FOLLEND']
					i['FOLLOW'] = None
					i['FOLLEND'] = 0
					i['FOLLMOV'] = ''
					i['SPEED'] = 0
		#ACTIONS
		if self.colide(self.player[0]['RECT'], rect) == True and self.portalgo == {}:
			if i['TALKING'] == False:
				if self.battle == False and self.speakin != rect and self.dlgfa > 0 and isinstance(i['TYPE'],str) == False:
					self.display[0].blit(pygame.image.load('Sprites/arw.png'), (rect.x - self.cam.x + int(rect.width/2) - 5, rect.y - self.cam.y - rect.height * 2))
					self.hpctrl = database.HINTS['NPC_DIALOG']
				if isinstance(i['TYPE'],str) and i['TYPE'].startswith('scene'):
					if resources.SCENE == int(i['TYPE'][5]) - 1:
						resources.SCENE = int(i['TYPE'][5])
						act = True
					else: act = False
				else:
					act = False
					self.pressed = pygame.key.get_pressed()
					if self.pressed[resources.ACT[0]]:
						self.player[0]['PAUSE'] = 1
						act = True
				if act == True:
					i['FOLLOW'] = None
					i['TALKING'] = True
					#NPC DIALOG
					if i['TYPE'] in [0,None] or isinstance(i['TYPE'],str):
						if self.dlgfa > 0:
							i['SPEED'] = 0
							if i['DIRECTION'] == 1: i['HEAD'] = 'TALKR_' + i['INDEX'][0:3] + i['INDEX'][5]
							if i['DIRECTION'] == 2: i['HEAD'] = 'TALKRD_' + i['INDEX'][0:3] + i['INDEX'][5]
							if i['DIRECTION'] == 3: i['HEAD'] = 'TALKD_' + i['INDEX'][0:3] + i['INDEX'][5]
							if i['DIRECTION'] == 4: i['HEAD'] = 'TALKLD_' + i['INDEX'][0:3] + i['INDEX'][5]
							if i['DIRECTION'] == 5: i['HEAD'] = 'TALKL_' + i['INDEX'][0:3] + i['INDEX'][5]
							if i['DIRECTION'] == 6: i['HEAD'] = 'TALKLU_' + i['INDEX'][0:3] + i['INDEX'][5]
							if i['DIRECTION'] == 7: i['HEAD'] = 'TALKU_' + i['INDEX'][0:3] + i['INDEX'][5]
							if i['DIRECTION'] == 8: i['HEAD'] = 'TALKRU_' + i['INDEX'][0:3] + i['INDEX'][5]
							#DIALOG
							if i['WHO'] != 'REWARD':
								if isinstance(i['WHO'], int): self.dialog(database.DIALOGS['NPC_' + str(i['WHO'])][resources.DLGSAV[i['WHO']]].copy(),rect)
								else: self.dialog(database.DIALOGS[i['WHO']][resources.DLGSAV[i['WHO']]].copy(),rect)
							#GET REWARD
							else:
								btls = None
								for b in resources.PARTY[resources.FORMATION]:
									for it in ['bottle100','bottle250']:
										btls = self.inv.find(b,it)
										if btls != None and int(btls[1]) > 0: break
									if btls != None and int(btls[1]) > 0: break
								if btls != None:
									if int(btls[1]) > 150: self.dialog(database.DIALOGS['REWARD'][3].copy(),rect)
									elif int(btls[1]) > 90: self.dialog(database.DIALOGS['REWARD'][2].copy(),rect)
									elif int(btls[1]) > 0: self.dialog(database.DIALOGS['REWARD'][1].copy(),rect)
									if self.notx == 0:
										src = None
										for i in resources.PARTY[resources.FORMATION]:
											src = self.inv.find(i,'credit_card')
											if src == None:
												src = self.inv.find(i,'wallet')
												if src != None:
													src[1] = str(int(src[1][0:6]) + int(btls[1]))
													break
											else:
												src[1] = str(int(src[1]) + int(btls[1]))
												break
										self.ch_sfx.play(resources.SOUND['CASH_GET'])
										self.notification('Adquiriu $' + btls[1],(255, 255, 255))
										self.dlg = []
										btls[1] = '000'
								else: self.dialog(database.DIALOGS['REWARD'][0].copy(),rect)
					#MARKET CASHIER
					elif i['TYPE'] == 2:
						if i['WHO'].startswith('DRITHR'):
							if self.driving == 0:
								if self.dlgfa > 0: self.dialog(database.DIALOGS[i['WHO']][0].copy(),rect)
							else:
								self.products = []
								for p in database.PRODUCTS[int(i['INDEX'])][0]:
									self.products.append(p)
								self.shp = True
								self.lopt = 0
								self.opt = 0
								self.mnu = 2
						elif self.basket == []:
							if self.dlgfa > 0: self.dialog(database.DIALOGS[i['WHO']][0].copy(),rect)
						else:
							self.products = []
							for p in database.PRODUCTS[int(i['INDEX'])][0]:
								self.products.append(p)
							self.shp = True
							self.lopt = 0
							self.opt = 0
							self.mnu = 2
					#DEPOSIT ITEMS
					elif i['TYPE'] == 4:
						self.dialog(database.DIALOGS['DEPOSIT'][0],rect)
						self.inventory = 2
						self.ch_sfx.play(resources.SOUND['INVENTORY_OPEN'])
						self.invfade = 0
						self.opt = 0
						self.lopt = 1
						self.mnu = 0
						self.exvar = 0
					elif i['TYPE'] == 5:
						#ATM MACHINE
						if i['INDEX'] == 0:
							self.extract = [0,0,0,0,0,0]
							self.opt = 0
							self.lopt = 1
							self.mnu = 0
							self.exvar = 0
						#BED
						elif i['INDEX'] == 1:
							self.sleepin = not self.sleepin
							if self.sleepin == False: self.player[0]['PAUSE'] = 1
							else: self.player[0]['PAUSE'] = 0
						#TRASH CAN
						elif i['INDEX'] == 2:
							self.inventory = 3
							self.ch_sfx.play(resources.SOUND['INVENTORY_OPEN'])
							self.invfade = 0
							self.opt = 0
							self.lopt = 1
							self.mnu = 0
						#PHONE
						elif i['INDEX'] == 3:
							src = None
							for i in resources.PARTY[resources.FORMATION]:
								src = self.inv.find(i,'credit_card')
								if src == None:
									src = self.inv.find(i,'wallet')
							if src != None and int(src[1]) > 0:
								resources.MONEY -= 1
								self.phone = 3
								self.wait()
								database.CALLHIST.insert(0,[database.CONTACTS[self.lopt][1],False])
								self.dialog(database.DIALOGS[database.CONTACTS[self.lopt][1]][0],rect)
							else:
								self.dialog([database.MENU[18]],rect)
						#BATTERY PLUG
						elif i['INDEX'] == 4:
							print('here')
							if self.inv.find(resources.PARTY[resources.FORMATION][0],'charger') != None: self.ch_sfx.play(resources.SOUND['MENU_GO']); #resources.BATTERY = 360
							else: self.ch_sfx.play(resources.SOUND['MENU_GO']); self.dialog(database.DIALOGS['PLUG'])
						#REFUEL
						elif i['INDEX'] == 5 and self.driving > 0:
							while resources.GAS < self.vehicles[self.driving - 1]['CAPACITY']:
								resources.GAS += 1
								self.run()
					#PRODUCTS AND MERCATOR
					elif i['TYPE'] != None:
						if i['TYPE'] == 3:
							self.dialog(database.DIALOGS['MERCATOR'][0],rect)
							self.basket = []
							p = 0
							for u in resources.PARTY[resources.FORMATION]:
								self.basket.append([])
								for y in range(len(resources.INVENTORY[u])):
									for x in range(len(resources.INVENTORY[u][y])):
										if resources.INVENTORY[u][y][x][0] != '_' and database.ITEMS[resources.INVENTORY[u][y][x][0]][2] != 0:
											self.basket[p].append([y,x])
								p += 1
						if resources.DATE[3] == database.PRODUCTS[0][1]:
							self.promo = database.PRODUCTS[0][2]
						self.products = []
						for p in database.PRODUCTS[0][0]:
							self.products.append(p)
						self.shp = True
						self.player[0]['PAUSE'] = 1
						self.lopt = 0
						self.opt = 0
						self.mnu = 2
		else: i['TALKING'] = False

	def vehicle(self, i):
		rect = pygame.Rect(i['RECT'].x - 5,i['RECT'].y - 5,60,30)
		if self.driving == i['N'] + 1:
			i['RECT'].x = self.player[0]['RECT'].x
			i['RECT'].y = self.player[0]['RECT'].y
		#DRAW
		if self.rectdebug == True: pygame.draw.rect(self.display[0], (255,0,0), pygame.Rect(rect.x - self.cam.x, rect.y - self.cam.y, rect.width, rect.height))
		if self.colide(rect, self.cam) and self.turn != -6:
			self.display[0].blit(pygame.image.load('Sprites/moto_' + str(i['INDEX']) + '_walkL.png'), (rect.x - self.cam.x + 10, rect.y + rect.height - self.cam.y - 30))
		#MOVEMENT
		if i['MOVE'] == 'nodeon':
			for n in self.nodes:
				if self.colide(rect,n['RECT']):
					if n['GOING'] == 2: i['DIRECTION'] = n['TYPE']
		elif i['MOVE'] == 'nodeoff':
			for n in self.nodes:
				if self.colide(rect,n['RECT']):
					if n['GOING'] == 3: i['DIRECTION'] = n['TYPE']
		elif i['MOVE'] == 'police':
			for n in self.nodes:
				if self.colide(rect,n['RECT']):
					if n['GOING'] in [2,3]:
						if n['TYPE'] in [1,5]:
							if self.player[0]['RECT'].x > i['RECT'].x: i['DIRECTION'] = 1
							if self.player[0]['RECT'].x < i['RECT'].x: i['DIRECTION'] = 5
						if n['TYPE'] in [3,7]:
							if self.player[0]['RECT'].y > i['RECT'].y: i['DIRECTION'] = 3
							if self.player[0]['RECT'].y < i['RECT'].y: i['DIRECTION'] = 7
		if i['MOVE'] != 'fixed':
			if i['DIRECTION'] == 1: i['RECT'].x += 4
			if i['DIRECTION'] == 2: i['RECT'].x += 4; i['RECT'].y += 4
			if i['DIRECTION'] == 3: i['RECT'].y += 4
			if i['DIRECTION'] == 4: i['RECT'].x -= 4; i['RECT'].y += 4
			if i['DIRECTION'] == 5: i['RECT'].x -= 4
			if i['DIRECTION'] == 6: i['RECT'].x -= 4; i['RECT'].y -= 4
			if i['DIRECTION'] == 7: i['RECT'].y -= 4
			if i['DIRECTION'] == 8: i['RECT'].x += 4; i['RECT'].y -= 4
		#ACTION
		if self.colide(self.player[0]['RECT'], rect) == True:
			if self.battle == False and self.driving == 0:
				self.display[0].blit(pygame.image.load('Sprites/arw.png'), (rect.x - self.cam.x + int(rect.width/2) - 5, rect.y - self.cam.y - int(rect.height/2)))
				self.hpctrl = database.HINTS['VEHICLE_USE']
			if self.pressed[resources.ACT[0]] and self.driving == 0 and self.inventory == 0 and self.phone == 0 and self.shp == False:
				trigger = True
				self.driving = i['N'] + 1
				self.player[0]['RECT'].x = rect.x
				self.player[0]['RECT'].y = rect.y
				i['MOVE'] = 'fixed'
				'''self.displayzw = 1200
				self.displayzh = 800
				self.display = pygame.Surface((1200, 800))
				self.cam = pygame.Rect(0,0,self.displayzw,self.displayzh)'''

	def portal(self, i):
		if i['RECT'].width > 0: rect = pygame.Rect(i['RECT'].x,i['RECT'].y,i['RECT'].width,i['RECT'].height)
		else: rect = pygame.Rect(i['RECT'].x,i['RECT'].y,30,30)
		goto = False
		#DRAW
		if self.rectdebug == True: pygame.draw.rect(self.display[0], (255,0,0), pygame.Rect(rect.x - self.cam.x, rect.y - self.cam.y, rect.width, rect.height))
		if self.colide(rect, self.cam) and self.turn != -6:
			if self.colide(self.player[0]['RECT'], rect) == True and self.winbar > 0: spr = '1'
			else: spr = '0'
			if resources.MAP > 0:
				if i['RECT'].width == 24: self.display[0].blit(pygame.image.load('Sprites/door_0' + spr + '.png'), (rect.x - self.cam.x, rect.y - self.cam.y))
				if i['RECT'].width == 48: self.display[0].blit(pygame.image.load('Sprites/door_1' + spr + '.png'), (rect.x - self.cam.x, rect.y - self.cam.y))
			else: self.display[0].blit(pygame.image.load('Sprites/mp_player.png'), (rect.x - self.cam.x, rect.y - self.cam.y))
		#ENTERING DOOR
		if self.colide(self.player[0]['RECT'], rect) == True and self.winbar == 0 and self.portalgo == {}:
			if i['OPENING'] == 'key':
				fnd = self.inv.find(resources.PARTY[resources.FORMATION][0],'key_bedroom')
				if fnd != None and fnd[1] == i['CLOSURE']: goto = True
				else: goto = False

			elif i['OPENING'] != None:
				if resources.TIME[0] > i['OPENING'][0] and resources.TIME[0] < i['CLOSURE'][0]: goto = True
				elif resources.TIME[0] == i['OPENING'][0]:
					if resources.TIME[1] > i['OPENING'][1]: goto = True
				elif resources.TIME[0] == i['CLOSURE'][0]:
					if resources.TIME[1] < i['CLOSURE'][1]: goto = True
			else: goto = True

			if i['RECT'].width == 24 and self.driving > 0: goto = False
			elif i['RECT'].width == 48: goto = False

		if goto == True:
			for p in self.player:
				p['PAUSE'] = 1
				p['SPEED'] = 0
			if i['TYPE'] > 0:
				self.ch_ton.play(resources.SOUND['DOOR_OPEN'])
			if i['MUSIC'] not in ['inside','outside',None]:
				self.ch_msc.fadeout(1000)
				spd = 5
			else: spd = 10
			#BATHROOM
			if i['MAP'] == 'bathroom':
				self.transiction(True, 210)
				for i in range(30): self.run()
				self.ch_ton.play(resources.SOUND['TREASURE'])
				for i in resources.PARTY[resources.FORMATION]:
					if resources.CHARACTERS[i]['HEALTH'] in [3,5]:
						resources.CHARACTERS[i]['HEALTH'] = 0
				for i in range(60): self.run()
				self.ch_ton.play(resources.SOUND['DOOR_CLOSE'])
				for p in self.player[0]:
					p['RECT'].x = i['RECT'].x
					p['RECT'].y = i['RECT'].y + 20
					p['PAUSE'] = 0
				self.transiction(False, 0)
			#GOTO ROOM
			else:
				self.portalgo = [{'MATCH': None, 'RECT' : pygame.Rect(i['RECT'].x - self.cam.x,i['RECT'].y - self.cam.y,i['RECT'].width,i['RECT'].height)},{}]
				self.portalgo[1] = self.player[0].copy()
				self.portalgo[1]['RECT'].x -= self.cam.x
				self.portalgo[1]['RECT'].y -= self.cam.y
				self.transiction(True, 210, spd)
				self.rendermap(i['MAP'])
				self.portalgo[0]['MATCH'] = i['MATCH']
				while self.portalgo[0]['MATCH'] != None: self.run()
				if i['TYPE'] > 0:
					self.ch_ton.play(resources.SOUND['DOOR_CLOSE'])
				if i['MUSIC'] == 'outside': self.ch_msc.set_volume(1.0)
				elif i['MUSIC'] == 'inside': self.ch_msc.set_volume(0.2)
				elif i['MUSIC'] != None: self.ch_msc.play(resources.SOUND[i['MUSIC'].upper()],-1)
				if self.cityname == '':
					self.transiction(False, 0, spd)
				else:
					self.transiction(False, 50, 5)
					for r in range(100): self.run()
					self.transiction(False, 0, 5)
					self.cityname = ''
				self.portalgo = {}
				for p in self.player:
					p['RECT'].x = i['PX']
					p['RECT'].y = i['PY']
					p['PAUSE'] = 0

	def colide(self, i1, i2):
		cld = False
		if isinstance(i2, list):
			ind = 0
			for i in i2[2]:
				if self.facing(i1,i[1]) == 2:
					cld = pygame.Rect.colliderect(i1['RECT'],i[1])
					if cld == True and i1['JUMP'] == 0:
						#HOLD OBJECT
						if i[0] == 'HOLD':
							self.display[0].blit(pygame.image.load('Sprites/arw.png'), (i[1].x - self.cam.x + int(i[1].width/2) - 5, i[1].y - self.cam.y - i[1].height))
							self.pressed = pygame.key.get_pressed()
							if self.pressed[resources.ACT[0]] and self.player[0]['HOLD'] == None:
								self.player[0]['HOLD'] = ind
							cld = False
						#CARRY OBJECT
						elif i[0] == 'CARRY':
							if i1['DIRECTION'] == 1: i[1].x += i1['SPEED']
							if i1['DIRECTION'] == 3: i[1].y += i1['SPEED']
							if i1['DIRECTION'] == 5: i[1].x -= i1['SPEED']
							if i1['DIRECTION'] == 7: i[1].y -= i1['SPEED']
						break
				ind += 1
			#JUMP
			if cld == False:
				for i in i2[3]:
					if self.facing(i1,i[1]) == 2:
						cld = pygame.Rect.colliderect(i1['RECT'],i[1])
						if cld == True and i1['JUMP'] == 0: break
			#TURN ON OFF AREAS
			if cld == False and i1['PLAYING'] == True:
				for i in i2[4]:
					if self.facing(i1,i[1]) == 2:
						if pygame.Rect.colliderect(i1['RECT'],i[1]) and i1['JUMP'] == 0:
							if i[0].endswith('ON') and self.tilhide == False: self.tilhide = True
							if i[0].endswith('OFF') and self.tilhide == True: self.tilhide = False
							break
		else:
			cld = pygame.Rect.colliderect(i1,i2)

		return cld

	def facing(self, i1, i2):
		if isinstance(i2, dict) == False: i2 = {'RECT': i2, 'DIRECTION': self.player[0]['DIRECTION']}
		if i1['DIRECTION'] == i2['DIRECTION'] or i1['DIRECTION'] == i2['DIRECTION'] + 1 or i1['DIRECTION'] == i2['DIRECTION'] - 1:
			if i1['DIRECTION'] == 1:
				if i1['RECT'].x < i2['RECT'].x: return 2
				elif i1['RECT'].x > i2['RECT'].x: return 3
				else: return 1
			elif i1['DIRECTION'] == 2:
				if i1['RECT'].x < i2['RECT'].y: return 2
				elif i1['RECT'].x > i2['RECT'].y: return 3
				else: return 1
			elif i1['DIRECTION'] == 3:
				if i1['RECT'].y < i2['RECT'].y: return 2
				elif i1['RECT'].y > i2['RECT'].y: return 3
				else: return 1
			elif i1['DIRECTION'] == 4:
				if i1['RECT'].y < i2['RECT'].y: return 2
				elif i1['RECT'].y > i2['RECT'].y: return 3
				else: return 1
			elif i1['DIRECTION'] == 5:
				if i1['RECT'].x > i2['RECT'].x: return 2
				elif i1['RECT'].x < i2['RECT'].x: return 3
				else: return 1
			elif i1['DIRECTION'] == 6:
				if i1['RECT'].x > i2['RECT'].y: return 2
				elif i1['RECT'].x < i2['RECT'].y: return 3
				else: return 1
			elif i1['DIRECTION'] == 7:
				if i1['RECT'].y > i2['RECT'].y: return 2
				elif i1['RECT'].y < i2['RECT'].y: return 3
				else: return 1
			elif i1['DIRECTION'] == 8:
				if i1['RECT'].y > i2['RECT'].y: return 2
				elif i1['RECT'].y < i2['RECT'].y: return 3
				else: return 1
		else: return 1

	def events(self):
		for event in pygame.event.get():
			#EXIT
			if event.type == pygame.QUIT:
				self.classrun = 0
				resources.recent_data(1,resources.ID)
				pygame.quit()
				sys.exit()
				exit()
			#RESIZE
			if event.type == pygame.VIDEORESIZE:
				self.windoww = event.w
				self.windowh = event.h
				self.screen = pygame.display.set_mode((self.windoww, self.windowh), pygame.RESIZABLE)
				self.FPS = int(event.w/20)
			#MOUSE
			if resources.MOUSE == True:	
				mrect = pygame.image.load('Sprites/cursor_' + str(resources.CURSOR) + '.png').get_rect()
				mrect.x = math.floor(pygame.mouse.get_pos()[0]/2)
				mrect.y = math.floor(pygame.mouse.get_pos()[1]/2)
				self.pressed = pygame.mouse.get_pressed()

				if self.phone > 0 and self.phn.battery > 0:
					if self.phone == 1:
						#self.opt = -1
						#self.lopt = -1
						for i in range(len(self.phn.optrects)):
							if self.colide(mrect, self.phn.optrects[i]):
								self.lopt = math.floor(i/3)
								self.opt = i - (self.lopt * 3)
								if self.pressed[0]:
									self.phone = self.opt + (self.lopt * 3) + 2

									if self.phone == 2:
										self.mnu = 200
										self.opt = 80
										self.lopt = 80
									if self.phone == 7: resources.recent_data(0)

									self.ch_sfx.play(resources.SOUND['MENU_GO'])
									self.phn.scroll = 0
									self.opt = 0
									self.lopt = 0
									self.mnu = 0
			self.pressed = pygame.key.get_pressed()
			#DEBUG
			if self.pressed[pygame.K_DELETE]:
				self.dmenu = menu.Debug()
				while self.dmenu.classrun:
					self.dmenu.run()
					self.screen.fill((0,0,0),pygame.Rect(1120,720,30,30))
					self.screen.blit(self.dmenu.draw(), (0, 0))
					pygame.display.update(pygame.Rect(0,0,1200,50))
				self.dmenu.command()
				if self.dmenu.dlg == 'sleep':
					self.sleepin = not self.sleepin
				elif self.dmenu.dlg == 'rectdebug':
					self.rectdebug = not self.rectdebug
				elif self.dmenu.dlg == 'pacify':
					self.en = []
				elif self.dmenu.dlg == 'storage':
					self.inventory = 2
					self.invfade = 0
					self.opt = 0
					self.lopt = 1
					self.mnu = 0
					self.exvar = 0
				elif self.dmenu.dlg != []:
					self.dialog(self.dmenu.dlg)
					self.dmenu.dlg = []
				if self.dmenu.goto != '':
					try: self.rendermap(self.dmenu.goto)
					except: self.ch_sfx.play(resources.SOUND['ERROR'])
					self.transiction(False,0)
				self.dmenu = None
			#BATTLE OPTIONS
			if self.battle == True and self.phone == 0 and self.dlgfa > 0:
				self.pressed = pygame.key.get_pressed()
				if self.turn == len(resources.PARTY[resources.FORMATION]):
					self.fight()
					tp = 0
				else:
					if self.turn == 0: tp = 0
					elif self.turn >= len(self.player): tp = 0
					elif self.player[self.turn]['PLAYING'] == True: tp = self.turn
					else: tp = 0
				#CHOOSING WEAPON
				if self.mnu == 1:
					if self.pressed[resources.LEFT[tp]]: self.equip[self.turn] -=1; self.ch_sfx.play(resources.SOUND['MENU_HOR'])
					if self.pressed[resources.RIGHT[tp]]: self.equip[self.turn] +=1; self.ch_sfx.play(resources.SOUND['MENU_HOR'])
				
					if self.equip[self.turn] < 0: self.equip[self.turn] = 7
					if self.equip[self.turn] > 7: self.equip[self.turn] = 0

					if self.pressed[resources.ACT[tp]]:
						#WEAPONS
						if self.equip[self.turn] < 4:
							if resources.INVENTORY[resources.PARTY[resources.FORMATION][self.turn]][4][self.equip[self.turn] + 1][0].startswith('melee'):
								self.ch_sfx.play(resources.SOUND['MELEE'])
								self.mnu = 2
							elif resources.INVENTORY[resources.PARTY[resources.FORMATION][self.turn]][4][self.equip[self.turn] + 1][0].startswith('gun') and self.barpp[self.turn][self.equip[self.turn]] > 0:
								self.ch_sfx.play(resources.SOUND['GUN_TRIGGER'])
								self.mnu = 2
							else:
								self.ch_sfx.play(resources.SOUND['ERROR'])
						#TACTICAL
						elif self.equip[self.turn] == 4:
							self.ch_sfx.play(resources.SOUND['MENU_GO'])
							self.mnu = 2
						#DIALOG
						elif self.equip[self.turn] == 5:
							self.ch_sfx.play(resources.SOUND['MENU_GO'])
							self.fight()
							self.turn += 1
						#GUARD
						elif self.equip[self.turn] == 6:
							self.ch_ton.play(resources.SOUND['GUARD'])
							self.pres[self.turn] += 3
							self.turn += 1
							if self.turn == len(self.fig): self.fight()
						#RUN AWAY
						elif self.equip[self.turn] == 7:
							self.ch_sfx.play(resources.SOUND['MENU_GO'])
							self.fight()
							if self.battle == True:
								self.turn = len(resources.PARTY[resources.FORMATION])
								self.fight()
				#USING WEAPON
				elif self.mnu == 2:
					if self.equip[self.turn] == 4:
						if self.pressed[resources.LEFT[tp]]: self.opt -= 1; self.ch_sfx.play(resources.SOUND['MENU_HOR'])
						if self.pressed[resources.RIGHT[tp]]: self.opt += 1; self.ch_sfx.play(resources.SOUND['MENU_HOR'])
					if self.pressed[resources.ACT[tp]]:
						#SHOT OR HIT
						if self.equip[self.turn] < 4:
							self.fight()
							self.turn += 1
							self.mnu = 1
							if self.turn == len(resources.PARTY[resources.FORMATION]): self.fight()
						#TACTICAL ATTACK
						elif self.equip[self.turn] == 4:
							ttl = self.opt
							for i in self.fig:
								self.equip[self.turn] = resources.TACTICAL[ttl][self.turn]
								if self.equip[self.turn] != 0:
									if self.equip[self.turn] + 1 < 5:
										self.equip[self.turn] -= 1
										self.ch_sfx.play(resources.SOUND['GUN_TRIGGER'])
										self.mnu = 2
										self.wait()
									if self.equip[self.turn] != 6: self.fight()
									else:
										self.pres[self.turn] += 3
										self.ch_sfx.play(resources.SOUND['GUARD'])
								self.turn += 1
							for i in self.equip: i = 4
					#CANCEL MOVE
					if self.pressed[resources.RUN[tp]]:
						self.ch_sfx.play(resources.SOUND['MISS'])
						self.mnu = 1
					if self.opt < 0: self.opt = len(resources.TACTICAL) - 1
					if self.opt > len(resources.TACTICAL) - 1: self.opt = 0
			#SHOP OPTIONS
			if self.shp == True:
				if self.pressed[resources.LEFT[0]]: self.opt -= 1 ; self.ch_sfx.play(resources.SOUND['MENU_HOR'])
				if self.pressed[resources.RIGHT[0]]: self.opt += 1 ; self.ch_sfx.play(resources.SOUND['MENU_HOR'])
				if self.pressed[resources.UP[0]]: self.lopt -= 1 ; self.ch_sfx.play(resources.SOUND['MENU_VER'])
				if self.pressed[resources.DOWN[0]]: self.lopt += 1 ; self.ch_sfx.play(resources.SOUND['MENU_VER'])
				#PRODUCTS
				if self.mnu == 0:
					if self.pressed[resources.ACT[0]]:
						if self.lopt < len(self.products):
							for i in range(self.opt): self.basket.append(self.products[self.lopt])
							self.ch_sfx.play(resources.SOUND['MENU_GO'])
						else:
							self.ch_sfx.play(resources.SOUND['MENU_BACK'])
							self.shp = False
							self.lopt = 0
					if self.opt < 1: self.opt = 10
					if self.opt > 10: self.opt = 1
					if self.lopt < 0: self.lopt = len(self.products)
					if self.lopt > len(self.products): self.lopt = 0
				#CASHIER
				if self.mnu == 1:
					if self.pressed[resources.ACT[0]]:
						if self.lopt == 0:
							for i in self.basket:
								src = None
								for i in resources.PARTY[resources.FORMATION]:
									src = self.inv.find(i,'credit_card')
									if src == None:
										src = self.inv.find(i,'wallet')
								if scr != None and int(scr[1]) >= database.ITEMS[i][2]:
									if self.inv.space(resources.PARTY[resources.FORMATION][0]) == False:
										self.dialog(database.DIALOGS['MERCATOR'][2])
									elif self.confirmation() == 1:
										self.inv.add(resources.PARTY[resources.FORMATION][0],i)
										self.ch_sfx.play(resources.SOUND['BUY'])
										scr[1] = str(int(scr[1]) - database.ITEMS[i][2] - int(database.ITEMS[i][2]/self.promo))
								else:
									self.ch_sfx.play(resources.SOUND['ERROR'])
									self.dialog(database.DIALOGS['MERCATOR'][1])
						else:
							self.ch_sfx.play(resources.SOUND['MENU_BACK'])
							self.shp = False
							self.lopt = 0
					if self.opt < 1: self.opt = 1
					if self.lopt < 0: self.lopt = 1
					if self.lopt > 1: self.lopt = 0
				#MERCATOR
				if self.mnu == 2:
					if self.pressed[resources.ACT[0]]:
						src = None
						for i in resources.PARTY[resources.FORMATION]:
							src = self.inv.find(i,'credit_card')
							if src == None:
								src = self.inv.find(i,'wallet')
								if src != None: break
							if src != None: break
						#BUYING ITEMS
						if self.opt == 0:
							if self.lopt == len(self.products):
								self.player[0]['PAUSE'] = 0
								self.ch_sfx.play(resources.SOUND['MENU_BACK'])
								self.shp = False
								self.lopt = 0
							else:
								if src != None and int(src[1]) >= database.ITEMS[self.products[self.lopt]][2]:
									if self.inv.space(resources.PARTY[resources.FORMATION][0]) == False:
										self.dialog(database.DIALOGS['MERCATOR'][2])
									elif self.confirmation() == 1:
										self.inv.add(resources.PARTY[resources.FORMATION][0],self.products[self.lopt])
										self.ch_sfx.play(resources.SOUND['BUY'])
										if self.promo > 0:
											src[1] = str(int(src[1]) - (database.ITEMS[self.products[self.lopt]][2] - int(database.ITEMS[self.products[self.lopt]][2]/self.promo)))
										else:
											src[1] = str(int(src[1]) - database.ITEMS[self.products[self.lopt]][2])
								else:
									self.ch_sfx.play(resources.SOUND['ERROR'])
									self.dialog(database.DIALOGS['MERCATOR'][1])
						#SELLING ITEMS
						else:
							if self.lopt == len(self.basket[self.opt - 1]):
								self.player[0]['PAUSE'] = 0
								self.ch_sfx.play(resources.SOUND['MENU_BACK'])
								self.shp = False
								self.lopt = 0
							elif self.confirmation() == 1 and src != None:
								src[1] = str(int(src[1]) + math.floor(database.ITEMS[resources.INVENTORY[resources.PARTY[resources.FORMATION][self.opt - 1]][self.basket[self.opt - 1][self.lopt][0]][self.basket[self.opt - 1][self.lopt][1]][0]][2]/2))
								resources.INVENTORY[resources.PARTY[resources.FORMATION][self.opt - 1]][self.basket[self.opt - 1][self.lopt][0]][self.basket[self.opt - 1][self.lopt][1]] = ['_','0000','_','_']
								del self.basket[self.opt - 1][self.lopt]
								self.ch_sfx.play(resources.SOUND['SELL'])
					if self.opt < 0: self.opt = len(resources.PARTY[resources.FORMATION])
					if self.opt > len(resources.PARTY[resources.FORMATION]): self.opt = 0
					if self.opt == 0:
						if self.lopt < 0: self.lopt = len(self.products)
						if self.lopt > len(self.products): self.lopt = 0
					else:
						if self.lopt < 0: self.lopt = len(self.basket[self.opt - 1])
						if self.lopt > len(self.basket[self.opt - 1]): self.lopt = 0
				#BANK
				if self.mnu == 11 or self.mnu == 12:
					if self.pressed[resources.ACT[0]]:
						self.ch_sfx.play(resources.SOUND['CASH_GET'])
						self.shp = False
						self.opt = 0
						self.lopt = 0

					if self.opt < 0: self.opt = 5
					if self.opt > 5: self.opt = 0
					if self.lopt < 0: self.lopt = 9
					if self.lopt > 9: self.lopt = 0

					if self.pressed[resources.LEFT[0]]: self.lopt = self.extract[self.opt]
					if self.pressed[resources.RIGHT[0]]: self.lopt = self.extract[self.opt]
					
					self.extract[self.opt] = self.lopt

					if self.pressed[resources.UP[0]]:
						if self.mnu == 11:
							resources.ATM -= 1
							resources.MONEY += 1
						if self.mnu == 12:
							resources.ATM += 1
							resources.MONEY -= 1

					if self.pressed[resources.DOWN[0]]:
						if self.mnu == 11:
							resources.ATM += 1
							resources.MONEY -= 1
						if self.mnu == 12:
							resources.ATM -= 1
							resources.MONEY += 1
					'''if self.pressed[resources.UP[0]]:
						if self.mnu == 11:
							resources.ATM -= int(str(self.extract[0]) + str(self.extract[1]) + str(self.extract[2]) + str(self.extract[3]) + str(self.extract[4]) + str(self.extract[5]))
							resources.MONEY += int(str(self.extract[0]) + str(self.extract[1]) + str(self.extract[2]) + str(self.extract[3]) + str(self.extract[4]) + str(self.extract[5]))
						if self.mnu == 12:
							resources.ATM += int(str(self.extract[0]) + str(self.extract[1]) + str(self.extract[2]) + str(self.extract[3]) + str(self.extract[4]) + str(self.extract[5]))
							resources.MONEY -= int(str(self.extract[0]) + str(self.extract[1]) + str(self.extract[2]) + str(self.extract[3]) + str(self.extract[4]) + str(self.extract[5]))'''
				if self.mnu == 3:
					if self.pressed[resources.ACT[0]]:
						if self.lopt == 0:
							self.ch_sfx.play(resources.SOUND['MENU_GO'])
							self.mnu = 11
							self.lopt = 0
							self.opt = 5
						if self.lopt == 1:
							self.ch_sfx.play(resources.SOUND['MENU_GO'])
							self.mnu = 12
							self.lopt = 0
							self.opt = 5
						if self.lopt == 2:
							self.ch_sfx.play(resources.SOUND['MENU_BACK'])
							self.shp = False
							self.lopt = 0

					if self.lopt < 0: self.lopt = 2
					if self.lopt > 2: self.lopt = 0
			#INVENTORY OPTIONS
			if self.pressed[resources.BAG[0]] and self.phone == 0 and self.shp == False and self.inv.itmov == '':
				#OPEN AND CLOSE
				if self.inventory > 0:
					if self.inventory == 2: tlk = True
					else: tlk = False
					self.inventory = 0
					self.ch_sfx.play(resources.SOUND['INVENTORY_CLOSE'])
					if tlk == True and self.dlgfa > 0: self.dialog(database.DIALOGS['DEPOSIT'][1])
					self.player[0]['PAUSE'] = 0
					if self.battle == True: self.mnu = 1
				elif self.inventory == 0:
					self.inventory = 1
					self.ch_sfx.play(resources.SOUND['INVENTORY_OPEN'])
					self.player[0]['PAUSE'] = 1
					self.invfade = 0
					self.opt = 0
					self.lopt = 1
					self.mnu = 0
			if self.inventory > 0:
				ch = resources.CHARACTERS[resources.PARTY[resources.FORMATION][self.mnu]]
				#HOLDING ITEM
				if self.inv.itmov != '':
					#ACCESORIES SELECT
					if self.inv.itmov[0] == 0:
						if self.pressed[resources.LEFT[0]]:
							if self.exvar > 1: self.exvar -= 1; self.ch_sfx.play(resources.SOUND['MENU_HOR'])
						if self.pressed[resources.RIGHT[0]]:
							if self.exvar < 3: self.exvar += 1; self.ch_sfx.play(resources.SOUND['MENU_HOR'])
					#MOVING ITEM
					else:
						if self.pressed[resources.LEFT[0]]: self.opt -= 1; self.ch_sfx.play(resources.SOUND['MENU_HOR'])
						if self.pressed[resources.RIGHT[0]]: self.opt += 1; self.ch_sfx.play(resources.SOUND['MENU_HOR'])
						if self.pressed[resources.UP[0]]: self.lopt -= 1; self.ch_sfx.play(resources.SOUND['MENU_VER'])
						if self.pressed[resources.DOWN[0]]: self.lopt += 1; self.ch_sfx.play(resources.SOUND['MENU_VER'])
				#SELECT ITEM
				else:
					if self.pressed[resources.LEFT[0]]: self.opt -= 1; self.ch_sfx.play(resources.SOUND['MENU_HOR'])
					if self.pressed[resources.RIGHT[0]]: self.opt += 1; self.ch_sfx.play(resources.SOUND['MENU_HOR'])
					if self.pressed[resources.UP[0]]: self.lopt -= 1; self.ch_sfx.play(resources.SOUND['MENU_VER'])
					if self.pressed[resources.DOWN[0]]: self.lopt += 1; self.ch_sfx.play(resources.SOUND['MENU_VER'])

				if self.pressed[resources.ACT[0]] and self.opt < 4:
					#USING ITEMS
					if self.inv.itmov == '':
						#FOOD
						if resources.INVENTORY[resources.PARTY[resources.FORMATION][self.mnu]][self.lopt][self.opt][0].startswith('food') and resources.CHARACTERS[resources.PARTY[resources.FORMATION][0]]['HEALTH'] not in [4,10]:
							self.ch_ton.play(resources.SOUND['HEAL'])
							hl = database.ITEMS[resources.INVENTORY[resources.PARTY[resources.FORMATION][self.mnu]][self.lopt][self.opt][0]][5]
							if resources.INVENTORY[resources.PARTY[resources.FORMATION][self.mnu]][self.lopt][self.opt][2] != '_': hl += database.ITEMS[resources.INVENTORY[resources.PARTY[resources.FORMATION][self.mnu]][self.lopt][self.opt][2]][5]
							if resources.INVENTORY[resources.PARTY[resources.FORMATION][self.mnu]][self.lopt][self.opt][4] != '_': hl += database.ITEMS[resources.INVENTORY[resources.PARTY[resources.FORMATION][self.mnu]][self.lopt][self.opt][4]][5]
							if resources.INVENTORY[resources.PARTY[resources.FORMATION][self.mnu]][self.lopt][self.opt][0] in resources.CHARACTERS[self.mnu]['FAVFOOD']: hl += int(hl/2)
							self.ch_sfx.play(resources.SOUND['NOTIFICATION'])
							self.notification('hp_'+str(hp),(255, 0, 0))
							ch['HP'] += hl
							ch['HUNGER'] += database.ITEMS[resources.INVENTORY[resources.PARTY[resources.FORMATION][self.mnu]][self.lopt][self.opt][0]][6]
							if ch['HP'] > database.CLASSES[ch['CLASS']]['VITALITY'][ch['LEVEL']]: ch['HP'] = database.CLASSES[ch['CLASS']]['VITALITY'][ch['LEVEL']]
							resources.INVENTORY[resources.PARTY[resources.FORMATION][self.mnu]][self.lopt][self.opt] = ['_','0000','_','0000','_','0000']
						#DRINK
						elif resources.INVENTORY[resources.PARTY[resources.FORMATION][self.mnu]][self.lopt][self.opt][0].startswith('drink'):
							self.ch_ton.play(resources.SOUND['HEAL'])
							hl = database.ITEMS[resources.INVENTORY[resources.PARTY[resources.FORMATION][self.mnu]][self.lopt][self.opt][0]][5]
							if resources.INVENTORY[resources.PARTY[resources.FORMATION][self.mnu]][self.lopt][self.opt][0] in resources.CHARACTERS[self.mnu]['FAVFOOD']: hl += int(hl/2)
							self.ch_sfx.play(resources.SOUND['NOTIFICATION'])
							self.notification('hp_'+str(hp),(255, 0, 0))
							ch['HP'] += hl
							ch['THIRST'] += database.ITEMS[resources.INVENTORY[resources.PARTY[resources.FORMATION][self.mnu]][self.lopt][self.opt][0]][6]
							if ch['HP'] > database.CLASSES[ch['CLASS']]['VITALITY'][ch['LEVEL']]: ch['HP'] = database.CLASSES[ch['CLASS']]['VITALITY'][ch['LEVEL']]
							resources.INVENTORY[resources.PARTY[resources.FORMATION][self.mnu]][self.lopt][self.opt] = ['_','0000','_','0000','_','0000']
						#REPELLENTS
						elif resources.INVENTORY[resources.PARTY[resources.FORMATION][self.mnu]][self.lopt][self.opt][0].startswith('repellent'):
							self.ch_sfx.play(resources.SOUND['MENU_GO'])
							ch['HEALTH'] = 2
							self.waitlst.append(['repellent' + str(resources.PARTY[resources.FORMATION][self.mnu]),self.waitime + database.ITEMS[resources.INVENTORY[resources.PARTY[resources.FORMATION][self.mnu]][self.lopt][self.opt][0]][5]])
							resources.INVENTORY[resources.PARTY[resources.FORMATION][self.mnu]][self.lopt][self.opt] = ['_','0000','_','0000','_','0000']
						#STRENGHT PILL
						elif resources.INVENTORY[resources.PARTY[resources.FORMATION][self.mnu]][self.lopt][self.opt][0] == 'pill_strenght':
							self.ch_ton.play(resources.SOUND['ATTRIBUTE_GAIN'])
							ch['LEVEL'] += 1
							resources.INVENTORY[resources.PARTY[resources.FORMATION][self.mnu]][self.lopt][self.opt] = ['_','0000','_','0000','_','0000']
						#ATTACK PILL
						elif resources.INVENTORY[resources.PARTY[resources.FORMATION][self.mnu]][self.lopt][self.opt][0] == 'pill_attack':
							self.ch_ton.play(resources.SOUND['ATTRIBUTE_GAIN'])
							ch['LEVEL'] += 1
							resources.INVENTORY[resources.PARTY[resources.FORMATION][self.mnu]][self.lopt][self.opt] = ['_','0000','_','0000','_','0000']
						#AGILITY PILL
						elif resources.INVENTORY[resources.PARTY[resources.FORMATION][self.mnu]][self.lopt][self.opt][0] == 'pill_agility':
							self.ch_ton.play(resources.SOUND['ATTRIBUTE_GAIN'])
							ch['LEVEL'] += 1
							resources.INVENTORY[resources.PARTY[resources.FORMATION][self.mnu]][self.lopt][self.opt] = ['_','0000','_','0000','_','0000']
						#RESISTANCE PILL
						elif resources.INVENTORY[resources.PARTY[resources.FORMATION][self.mnu]][self.lopt][self.opt][0] == 'pill_resistance':
							self.ch_ton.play(resources.SOUND['ATTRIBUTE_GAIN'])
							ch['LEVEL'] += 1
							resources.INVENTORY[resources.PARTY[resources.FORMATION][self.mnu]][self.lopt][self.opt] = ['_','0000','_','0000','_','0000']
						#VITALITY PILL
						elif resources.INVENTORY[resources.PARTY[resources.FORMATION][self.mnu]][self.lopt][self.opt][0] == 'pill_vitality':
							self.ch_ton.play(resources.SOUND['ATTRIBUTE_GAIN'])
							ch['LEVEL'] += 1
							resources.INVENTORY[resources.PARTY[resources.FORMATION][self.mnu]][self.lopt][self.opt] = ['_','0000','_','0000','_','0000']
						#MISTERY PILL
						elif resources.INVENTORY[resources.PARTY[resources.FORMATION][self.mnu]][self.lopt][self.opt][0] == 'pill_mistery':
							self.ch_ton.play(resources.SOUND['ATTRIBUTE_GAIN'])
							ch['LEVEL'] += 1
							resources.INVENTORY[resources.PARTY[resources.FORMATION][self.mnu]][self.lopt][self.opt] = ['_','0000','_','0000','_','0000']
						#LOCKSMITH KEYS
						elif resources.INVENTORY[resources.PARTY[resources.FORMATION][self.mnu]][self.lopt][self.opt][0].startswith('locksmith'):
							self.ch_ton.play(resources.SOUND['MENU_GO'])
							self.inv.itmov = [0,resources.INVENTORY[resources.PARTY[resources.FORMATION][self.mnu]][self.lopt][self.opt][2],resources.INVENTORY[resources.PARTY[resources.FORMATION][self.mnu]][self.lopt][self.opt][4]]
							self.exvar = 1
						#WALLET ITEMS
						elif resources.INVENTORY[resources.PARTY[resources.FORMATION][self.mnu]][self.lopt][self.opt][0] == 'wallet':
							self.ch_ton.play(resources.SOUND['MENU_GO'])
							self.inv.itmov = [0,resources.INVENTORY[resources.PARTY[resources.FORMATION][self.mnu]][self.lopt][self.opt][2],resources.INVENTORY[resources.PARTY[resources.FORMATION][self.mnu]][self.lopt][self.opt][4]]
							self.inv.money = True
							self.exvar = 1
						#ERROR
						else: self.ch_ton.play(resources.SOUND['ERROR'])

						if self.battle == True:
							self.turn += 1
							self.mnu = 1
							self.inventory = 0
					#ACCESORIES EXIT
					elif self.inv.itmov[0] == 0:
						if self.exvar == 3:
							self.ch_sfx.play(resources.SOUND['MENU_GO'])
							self.inv.itmov = ''
							self.inv.money = False
						else: self.ch_ton.play(resources.SOUND['ERROR'])
					#CRAFTING
					elif resources.INVENTORY[resources.PARTY[resources.FORMATION][self.mnu]][self.lopt][self.opt][0] != '_':
						craft = False
						if self.inv.itmov[0].startswith('key') and resources.INVENTORY[resources.PARTY[resources.FORMATION][self.mnu]][self.lopt][self.opt][0].startswith('locksmith'): craft = True
						if self.inv.itmov[0].startswith('id_card') and resources.INVENTORY[resources.PARTY[resources.FORMATION][self.mnu]][self.lopt][self.opt][0].startswith('wallet'): craft = True
						if self.inv.itmov[0].startswith('credit_card') and resources.INVENTORY[resources.PARTY[resources.FORMATION][self.mnu]][self.lopt][self.opt][0].startswith('wallet'): craft = True
						elif self.inv.itmov[0].startswith('condiment') and resources.INVENTORY[resources.PARTY[resources.FORMATION][self.mnu]][self.lopt][self.opt][0].startswith('food'): craft = True
						elif self.inv.itmov[0].startswith('acc') and resources.INVENTORY[resources.PARTY[resources.FORMATION][self.mnu]][self.lopt][self.opt][0].startswith('gun'): craft = True
						#RECHARGE WEAPONS
						if self.inv.itmov[0].startswith('ammo') and resources.INVENTORY[resources.PARTY[resources.FORMATION][self.mnu]][self.lopt][self.opt][0].startswith('gun'):
							if database.ITEMS[self.inv.itmov[0]][5] == database.ITEMS[resources.INVENTORY[resources.PARTY[resources.FORMATION][self.mnu]][self.lopt][self.opt][0]][5]['GAUGE']:
								craft = True
								self.ch_ton.play(resources.SOUND['GUN_RECHARGE'])
								resources.INVENTORY[resources.PARTY[resources.FORMATION][self.mnu]][self.lopt][self.opt][3] = database.ITEMS[resources.INVENTORY[resources.PARTY[resources.FORMATION][self.mnu]][self.lopt][self.opt][0]][5]['CAPACITY']
								if self.lopt == 4 and self.opt > 0:
									if int(resources.INVENTORY[resources.PARTY[resources.FORMATION][self.mnu]][self.lopt][self.opt][3]) > 0:
										plus = int(98/(database.ITEMS[resources.INVENTORY[resources.PARTY[resources.FORMATION][self.mnu]][self.lopt][self.opt][0]][5]['CAPACITY']/int(resources.INVENTORY[resources.PARTY[resources.FORMATION][self.mnu]][self.lopt][self.opt][3])))
									else: plus = 0
									self.barpp[self.mnu][self.opt - 1] = plus
							else: craft = False
						else: craft = False
						#ADDING ACCESORIES
						if craft == True:
							if resources.INVENTORY[resources.PARTY[resources.FORMATION][self.mnu]][self.lopt][self.opt][2] == '_':
								self.ch_ton.play(resources.SOUND['CRAFT'])
								resources.INVENTORY[resources.PARTY[resources.FORMATION][self.mnu]][self.lopt][self.opt][2] = self.inv.itmov[0]
								resources.INVENTORY[resources.PARTY[resources.FORMATION][self.mnu]][self.lopt][self.opt][3] = self.inv.itmov[1]
								self.inv.itmov = ''
							elif resources.INVENTORY[resources.PARTY[resources.FORMATION][self.mnu]][self.lopt][self.opt][4] == '_':
								self.ch_ton.play(resources.SOUND['CRAFT'])
								resources.INVENTORY[resources.PARTY[resources.FORMATION][self.mnu]][self.lopt][self.opt][4] = self.inv.itmov[0]
								resources.INVENTORY[resources.PARTY[resources.FORMATION][self.mnu]][self.lopt][self.opt][5] = self.inv.itmov[1]
								self.inv.itmov = ''
							else: self.ch_ton.play(resources.SOUND['ERROR']); self.shake = 5
						else: self.ch_ton.play(resources.SOUND['ERROR']); self.shake = 5

						if self.battle == True:
							self.turn += 1
							self.mnu = 1
							self.inventory = 0

				if self.pressed[resources.RUN[0]]:
					if self.inv.itmov != '':
						#TAKE SUB-ITEM
						if self.inv.itmov[0] == 0:
							if self.exvar < 3 and self.inv.itmov[self.exvar] != '_':
								self.ch_sfx.play(resources.SOUND['MENU_GO'])
								itm = self.inv.itmov[self.exvar]
								resources.INVENTORY[resources.PARTY[resources.FORMATION][self.mnu]][self.lopt][self.opt][self.exvar + 1] = '_'
								if self.exvar == 1:
									prp = resources.INVENTORY[resources.PARTY[resources.FORMATION][self.mnu]][self.lopt][self.opt][3]
								if self.exvar == 2:
									if resources.INVENTORY[resources.PARTY[resources.FORMATION][self.mnu]][self.lopt][self.opt][2] == '_':
										prp = resources.INVENTORY[resources.PARTY[resources.FORMATION][self.mnu]][self.lopt][self.opt][3]
									else:
										prp = resources.INVENTORY[resources.PARTY[resources.FORMATION][self.mnu]][self.lopt][self.opt][5]
								self.inv.itmov = [itm,prp,'_','_']
							else: self.ch_sfx.play(resources.SOUND['ERROR']); self.inv.shake = 5
						#PLACE ITEM IN INVENTORY
						elif self.opt < 5 and resources.INVENTORY[resources.PARTY[resources.FORMATION][self.mnu]][self.lopt][self.opt][0] == '_' and self.inv.space(resources.PARTY[resources.FORMATION][self.mnu],self.exvar,self.opt,self.lopt) == True:
							self.ch_sfx.play(resources.SOUND['EQUIP'])
							resources.INVENTORY[resources.PARTY[resources.FORMATION][self.mnu]][self.lopt][self.opt] = self.inv.itmov.copy()
							if self.inv.itmov[0].startswith('clth'):
								ch['COSTUME'] = database.ITEMS[self.inv.itmov[0]][5]
							if self.inv.itmov[0].startswith('head'):
								ch['ACCESORIES'] = self.inv.itmov[0]
							#AMMO BAR
							if self.inv.itmov[0].startswith('gun'):
								self.barpp = []
								x = 0
								for i in resources.PARTY[resources.FORMATION]:
									self.barpp.append([])
									for j in resources.INVENTORY[i][4][1:]:
										if j[0] != '_':
											if int(j[1]) > 0: b = int(100/(database.ITEMS[j[0]][5]['CAPACITY']/int(j[1])))
											else: b = 0
											self.barpp[x].append(b)
										else:
											self.barpp[x].append(0)
									x += 1
							self.inv.itmov = ''
							if self.battle == True:
								self.turn += 1
								self.mnu = 1
								self.inventory = 0
						#PLACE ITEM IN STORAGE
						elif self.opt > 4 and database.STORAGE[self.opt + (self.lopt * 5) - 5][0] == '_':
							self.ch_sfx.play(resources.SOUND['EQUIP'])
							database.STORAGE[self.opt + (self.lopt * 5) - 5] = self.inv.itmov.copy()
							chk = True
							for j in database.STORAGE:
								if j[0] == '_': chk = False
							if chk == True:
								for i in range(5): database.STORAGE.append(['_','0000','_','_'])
							self.inv.itmov = ''
							#AMMO BAR
							self.barpp = []
							x = 0
							for i in resources.PARTY[resources.FORMATION]:
								self.barpp.append([])
								for j in resources.INVENTORY[i][4][1:]:
									if j[0] != '_':
										if int(j[1]) > 0: b = int(100/(database.ITEMS[j[0]][5]['CAPACITY']/int(j[1])))
										else: b = 0
										self.barpp[x].append(b)
									else:
										self.barpp[x].append(0)
								x += 1
						#SWITCH ITEMS IN INVENTORY
						elif self.opt < 5 and self.inv.space(self.mnu,self.exvar,self.opt,self.lopt) == True:
							self.ch_sfx.play(resources.SOUND['EQUIP'])
							trd = resources.INVENTORY[resources.PARTY[resources.FORMATION][self.mnu]][self.lopt][self.opt].copy()
							resources.INVENTORY[resources.PARTY[resources.FORMATION][self.mnu]][self.lopt][self.opt] = self.inv.itmov
							if self.inv.itmov[0].startswith('clth'):
								ch['COSTUME'] = database.ITEMS[self.inv.itmov[0]][5]
							self.inv.itmov = trd
						#SWITCH ITEMS IN STORAGE
						elif self.opt > 4:
							self.ch_sfx.play(resources.SOUND['EQUIP'])
							trd = database.STORAGE[self.opt + (self.lopt * 5) - 5].copy()
							database.STORAGE[self.opt + (self.lopt * 5) - 5] = self.inv.itmov.copy()
							if self.inv.itmov[0].startswith('clth'):
								ch['COSTUME'] = database.ITEMS[self.inv.itmov[0]][5]
							self.inv.itmov = trd
						else: self.ch_sfx.play(resources.SOUND['ERROR']); self.inv.shake = 5
					#TAKE ITEM FROM INVENTORY
					elif self.opt < 5 and resources.INVENTORY[resources.PARTY[resources.FORMATION][self.mnu]][self.lopt][self.opt][0] != '_':
						self.ch_sfx.play(resources.SOUND['MENU_GO'])
						self.inv.itmov = resources.INVENTORY[resources.PARTY[resources.FORMATION][self.mnu]][self.lopt][self.opt].copy()
						resources.INVENTORY[resources.PARTY[resources.FORMATION][self.mnu]][self.lopt][self.opt] = ['_','0000','_','0000','_','0000']
					#TAKE ITEM FROM STORAGE
					elif database.STORAGE[self.opt + (self.lopt * 5) - 5][0] != '_':
						self.ch_sfx.play(resources.SOUND['MENU_GO'])
						self.inv.itmov = database.STORAGE[self.opt + (self.lopt * 5) - 5].copy()
						database.STORAGE[self.opt + (self.lopt * 5) - 5] = ['_','0000','_','0000','_','0000']
					'''elif self.inventory == 3:
						if resources.INVENTORY[resources.PARTY[resources.FORMATION][self.mnu]][self.lopt][self.opt][0] != '_' and self.confirmation() == 1:
							resources.INVENTORY[resources.PARTY[resources.FORMATION][self.mnu]][self.lopt][self.opt] = ['_','0000','_','_']'''

				if self.inventory == 1:
					if self.opt < 0: self.opt = 4; self.mnu -= 1
					if self.opt > 4: self.opt = 0; self.mnu += 1
					if self.lopt < 0: self.lopt = 4
					if self.lopt > 4: self.lopt = 0
				if self.inventory == 2:
					if self.opt < 0: self.opt = 9
					if self.opt > 9: self.opt = 0
					if self.opt < 5:
						if self.lopt < 0: self.lopt = 4; self.mnu -= 1
						if self.lopt > 4: self.lopt = 0; self.mnu += 1
					else:
						if self.lopt < 0: self.lopt = math.ceil(len(database.STORAGE)/5) - 1
						if self.lopt > math.ceil(len(database.STORAGE)/5) - 1: self.lopt = 0
					if self.exvar < 0: self.exvar = 1
					if self.exvar > 1: self.exvar = 0

				if self.mnu < 0: self.mnu = len(resources.PARTY[resources.FORMATION]) - 1
				if self.mnu > len(resources.PARTY[resources.FORMATION]) - 1: self.mnu = 0
			#PHONE OPTIONS
			if self.pressed[resources.PHONE[0]] and self.inv.find(resources.PARTY[resources.FORMATION][0],'phone') != None and self.inventory == 0 and self.shp == False and self.nmenu.show == False:
				#OPEN AND CLOSE
				if self.phone == 0 or self.phone > 1:
					if self.phone == 0:
						wh = resources.CHARACTERS[resources.PARTY[resources.FORMATION][0]]['HAIR'] + resources.CHARACTERS[resources.PARTY[resources.FORMATION][0]]['SKIN']
						cl = resources.CHARACTERS[resources.PARTY[resources.FORMATION][0]]['COSTUME'] + resources.CHARACTERS[resources.PARTY[resources.FORMATION][0]]['SKIN']
						self.player[0]['HEAD'] = 'BLANKDD_' + wh
						self.player[0]['SPRITE'] = 'PHONE_' + cl
						self.opt = 0; self.lopt = 0; self.player[0]['PAUSE'] = 1
					if self.phone == 2: self.opt = 0; self.lopt = 0; self.phn.scroll = 0
					if self.phone == 3: self.opt = 1; self.lopt = 0; self.phn.scroll = 0
					if self.phone == 4: self.opt = 2; self.lopt = 0; self.phn.scroll = 0
					if self.phone == 5: self.opt = 0; self.lopt = 1; self.phn.scroll = 0
					if self.phone == 6: self.opt = 1; self.lopt = 1; self.phn.scroll = 0; self.ch_ton.stop(); self.ch_ton.set_volume(resources.SFX)
					if self.phone == 7: self.opt = 2; self.lopt = 1; self.phn.scroll = 0
					if self.phone == 8: self.opt = 0; self.lopt = 2; self.phn.scroll = 0
					if self.phone == 9: self.opt = 1; self.lopt = 2; self.phn.scroll = 0
					if self.phone == 10: self.opt = 2; self.lopt = 2; self.phn.scroll = 0
					if self.phone == 11: self.opt = 0; self.lopt = 3; self.phn.scroll = 60
					if self.phone == 12: self.opt = 1; self.lopt = 3; self.phn.scroll = 60
					if self.phone == 13: self.opt = 2; self.lopt = 3; self.phn.scroll = 60
					if self.phone == 14: self.opt = 0; self.lopt = 4; self.phn.scroll = 120
					if self.phone == 15: self.opt = 1; self.lopt = 4; self.phn.scroll = 120
					if self.phone == 16: self.opt = 2; self.lopt = 4; self.phn.scroll = 120
					if self.phone == 17: self.opt = 0; self.lopt = 5

					if self.phone == 0 and self.battle == True:
						self.phone = 18
						self.mnu = 2
					elif self.nb != '':
						if self.phone == 0: self.phone = 17; self.opt = 0
						elif self.phone == 17: self.phone = 0
					else:
						if self.phone > 1: self.ch_sfx.play(resources.SOUND['MENU_BACK'])
						self.phone = 1
						self.mnu = 0
				else:
					self.phone = 0
					if self.battle == False:
						self.opt = 0
						self.lopt = 0
						self.player[0]['PAUSE'] = 0
					else:
						self.mnu = 1
			if self.phone > 0 and self.phn.battery > 0:
				if self.phone > 1 and self.mnu == 0 and self.pressed[resources.RUN[0]]:
					if resources.CHAPTER != 0 or resources.SCENE != 0:
						self.ch_sfx.play(resources.SOUND['MENU_BACK'])
						self.phone = 1
				#APPS MENU
				if self.phone == 1:
					if self.pressed[resources.UP[0]]: self.lopt -=1; self.ch_sfx.play(resources.SOUND['MENU_VER'])
					if self.pressed[resources.DOWN[0]]: self.lopt +=1; self.ch_sfx.play(resources.SOUND['MENU_VER'])
					if self.pressed[resources.LEFT[0]]: self.opt -=1; self.ch_sfx.play(resources.SOUND['MENU_HOR'])
					if self.pressed[resources.RIGHT[0]]: self.opt +=1; self.ch_sfx.play(resources.SOUND['MENU_HOR'])

					if self.opt < 0: self.opt = 2
					if self.opt > 2: self.opt = 0
					if self.lopt < 0: self.lopt = 4
					if self.lopt > 4: self.lopt = 0

					if self.pressed[resources.ACT[0]]:
						self.phone = self.opt + (self.lopt * 3) + 2
						if self.phone == 2:
							self.mnu = 200
							self.opt = 80
							self.lopt = 80
						if self.phone == 7: resources.recent_data(0)
						self.ch_sfx.play(resources.SOUND['MENU_GO'])
						self.phn.scroll = 0
						self.opt = 0
						self.lopt = 0
						self.mnu = 0
				#CONTACTS MENU
				elif self.phone == 3:
					if self.pressed[resources.LEFT[0]]:
						self.ch_sfx.play(resources.SOUND['MENU_HOR'])
						if self.mnu == 0: self.opt -= 1; self.lopt = 0
						elif self.mnu < 3: self.mnu = 1
						else:
							self.mnu -= 1
							if self.mnu < 3: self.mnu = 5

					if self.pressed[resources.RIGHT[0]]:
						self.ch_sfx.play(resources.SOUND['MENU_HOR'])
						if self.mnu == 0: self.opt += 1; self.lopt = 0
						elif self.mnu < 3: self.mnu = 2
						else:
							self.mnu += 1
							if self.mnu > 5: self.mnu = 3

					if self.pressed[resources.UP[0]]:
						self.ch_sfx.play(resources.SOUND['MENU_VER'])
						if self.mnu < 3: self.lopt -= 1
						else:
							self.exvar -= 1
							if self.exvar < 0: self.exvar = 5
							resources.PARTY[self.lopt][self.mnu - 3] = self.exvar

					if self.pressed[resources.DOWN[0]]:
						self.ch_sfx.play(resources.SOUND['MENU_VER'])
						if self.mnu < 3: self.lopt += 1
						else:
							self.exvar += 1
							if self.exvar > 5: self.exvar = 0
							resources.PARTY[self.lopt][self.mnu - 3] = self.exvar
					#PARTY SELECT
					if self.opt == 0:
						if self.lopt < 0: self.lopt = len(resources.PARTY)
						if self.lopt > len(resources.PARTY): self.lopt = 0

						if self.pressed[resources.ACT[0]]:
							self.ch_sfx.play(resources.SOUND['MENU_GO'])
							if self.lopt < len(resources.PARTY):
								if self.mnu == 0:
									self.mnu = 1
								elif self.mnu == 1:
									resources.FORMATION = self.lopt
									for i in resources.PARTY[resources.FORMATION]:
										resources.CHARACTERS[i]['HP'] = database.CLASSES[resources.CHARACTERS[i]['CLASS']]['VITALITY'][resources.CHARACTERS[i]['LEVEL']]
									self.ch_ton.play(resources.SOUND['PARTY_CHANGE'])
									self.phn.pbg = resources.PARTY[resources.FORMATION][0]
									self.mnu = 0
									self.opt = 0
									self.lopt = 0
								elif self.mnu > 2:
									resources.party_make(self.lopt)
									self.mnu = 0
								elif len(resources.PARTY) > 1:
									del resources.PARTY[self.lopt]
									self.mnu = 0 
							else:
								resources.PARTY.append([0,0,0])
								self.exvar = 0
								self.mnu = 3
					#PHONE SELECT
					if self.opt == 1:
						if self.lopt < 0: self.lopt = len(resources.CONTACTS) - 1
						if self.lopt > len(resources.CONTACTS) - 1: self.lopt = 0

						if self.pressed[resources.ACT[0]]:
							if self.mnu == 0:
								pygame.time.wait(round(random.randint(10,200)))
								if self.phn.credit > 0:
									wh = resources.CHARACTERS[resources.PARTY[resources.FORMATION][0]]['HAIR'] + resources.CHARACTERS[resources.PARTY[resources.FORMATION][0]]['SKIN']
									cl = resources.CHARACTERS[resources.PARTY[resources.FORMATION][0]]['COSTUME'] + resources.CHARACTERS[resources.PARTY[resources.FORMATION][0]]['SKIN']
									credit = self.inv.find(resources.PARTY[resources.FORMATION][0],'phone')
									if credit != None:
										if credit[2] == 'sim_card': credit[3] = str(int(credit[3]) - 1); self.phn.credit = int(credit[3])
										elif credit[4] == 'sim_card': credit[5] = str(int(credit[5]) - 1); self.phn.credit = int(credit[5])
									resources.CALLHIST.insert(0,[resources.CONTACTS[self.lopt][1],False])
									self.player[0]['SPRITE'] = 'CALL_' + cl
									self.phone = 0
									if resources.CONTACTS[self.lopt][1] in ['923778988','969696969','953478809']:
										gt = 0
										for i in self.waitlst:
											if i[0] == 'delivery': gt = 1
										self.dialog(database.DIALOGS[resources.CONTACTS[self.lopt][1]][gt])
									else:
										self.dialog(database.DIALOGS[resources.CONTACTS[self.lopt][1]][0])
									self.player[0]['PAUSE'] = 1
									self.player[0]['SPRITE'] = 'PHONE_' + cl
									self.phone = 3
								else:
									self.dialog([database.MENU[17]])

					if self.opt < 0: self.opt = 2
					if self.opt > 2: self.opt = 0
				#EMAIL MENU
				elif self.phone == 4 and self.signal > 0:
					if self.mnu == 0:
						if self.pressed[resources.UP[0]]: self.lopt -= 1; self.ch_sfx.play(resources.SOUND['MENU_VER'])
						if self.pressed[resources.DOWN[0]]: self.lopt += 1; self.ch_sfx.play(resources.SOUND['MENU_VER'])
						if self.pressed[resources.LEFT[0]]: self.opt -= 1; self.lopt = 0; self.ch_sfx.play(resources.SOUND['MENU_HOR'])
						if self.pressed[resources.RIGHT[0]]: self.opt += 1; self.lopt = 0; self.ch_sfx.play(resources.SOUND['MENU_HOR'])

					if self.pressed[resources.ACT[0]] and self.signal > 0:
						if self.mnu == 0: self.mnu = 1; self.ch_sfx.play(resources.SOUND['MENU_GO'])
						elif self.mnu > 0:
							self.ch_sfx.play(resources.SOUND['MENU_BACK'])
							if self.opt == 0: self.phn.e_unread[self.lopt][3] = 1
							if self.opt == 2: resources.INBOX[self.lopt][3] = 1
							self.mnu = 0
					read = 0
					unrd = 0
					for i in resources.INBOX:
						if i[3] == 0: unrd += 1
						if i[3] == 1: read += 1

					if self.opt < 0: self.opt = 2
					if self.opt > 2: self.opt = 0
					if self.opt == 0:
						if self.lopt < 0: self.lopt = unrd
						if self.lopt > unrd: self.lopt = 0
					if self.opt == 1:
						if self.lopt < 0: self.lopt = read
						if self.lopt > read: self.lopt = 0
					if self.opt == 2:
						if self.lopt < 0: self.lopt = len(resources.INBOX) - 1
						if self.lopt > len(resources.INBOX) - 1: self.lopt = 0
				#NEWS MENU
				elif self.phone == 5 and self.signal > 0:
					if self.mnu == 0:
						if self.pressed[resources.UP[0]]: self.lopt -= 1; self.ch_sfx.play(resources.SOUND['MENU_VER'])
						if self.pressed[resources.DOWN[0]]: self.lopt += 1; self.ch_sfx.play(resources.SOUND['MENU_VER'])

					if self.pressed[resources.ACT[0]]:
						self.ch_sfx.play(resources.SOUND['MENU_GO'])
						if self.mnu == 0: self.mnu = 1
						elif self.mnu > 0: self.mnu = 0

					if self.lopt < 0: self.lopt = 3
					if self.lopt > 3: self.lopt = 0
				#RADIO MENU
				elif self.phone == 6 and self.signal > 0:
					if self.pressed[resources.ACT[0]]:
						self.radonoff = not self.radonoff
					if self.radonoff == False and pygame.mixer.music.get_busy() == True:
						self.ch_sfx.play(resources.SOUND['MENU_BACK'])
						self.ch_ton.stop()
						pygame.mixer.music.stop()
					else:
						self.ch_sfx.play(resources.SOUND['MENU_GO'])
						self.ch_ton.play(resources.SOUND['NOISE'],-1)
				#CAMERA MENU
				elif self.phone == 7 and self.signal > 0:
					if self.pressed[resources.UP[0]]: self.lopt -= 1; self.ch_sfx.play(resources.SOUND['MENU_VER'])
					if self.pressed[resources.DOWN[0]]: self.lopt += 1; self.ch_sfx.play(resources.SOUND['MENU_VER'])

					if self.lopt < 0: self.lopt = 2
					if self.lopt > 2: self.lopt = 0

					if self.pressed[resources.ACT[0]] and self.signal > 0:
						self.ch_sfx.play(resources.SOUND['FILE_SAVE'])
						resources.PX = self.player[0]['RECT'].x
						resources.PY = self.player[0]['RECT'].y
						database.ID = self.lopt
						self.loadingif = 0.0
						if self.lopt < len(resources.FILES[0]):
							self.loading()
							resources.save_data()
							self.loading()
							resources.recent_data(1,self.lopt)
							self.loading()
						else: resources.recent_data(3,self.lopt);resources.new_data(True);resources.save_data()
						self.loadingif = None
						resources.recent_data(0)
				#BESTIARY MENU
				elif self.phone == 8 and self.signal > 0:
					if self.pressed[resources.UP[0]]: self.lopt -= 1; self.ch_sfx.play(resources.SOUND['MENU_VER'])
					if self.pressed[resources.DOWN[0]]: self.lopt += 1; self.ch_sfx.play(resources.SOUND['MENU_VER'])

					if self.pressed[resources.ACT[0]]:
						if self.mnu == 0: self.mnu = 1; self.ch_sfx.play(resources.SOUND['MENU_GO'])
						elif self.mnu > 0: self.mnu = 0; self.ch_sfx.play(resources.SOUND['MENU_BACK'])

					slst = 0
					for i in resources.BESTIARY:
						if i['SEEN'] > 0: slst += 1

					if self.mnu == 0:
						if self.lopt < 0: self.lopt = slst
						if self.lopt > slst: self.lopt = 0

					if self.mnu > 0:
						if self.pressed[resources.LEFT[0]]: self.mnu = 1; self.ch_sfx.play(resources.SOUND['MENU_HOR'])
						if self.pressed[resources.RIGHT[0]]: self.mnu = 2; self.ch_sfx.play(resources.SOUND['MENU_HOR'])

						if self.lopt < 0: self.lopt = 3
						if self.lopt > 3: self.lopt = 0
				#TASKS MENU
				elif self.phone == 9:
					if self.pressed[resources.UP[0]]: self.lopt -= 1; self.ch_sfx.play(resources.SOUND['MENU_VER'])
					if self.pressed[resources.DOWN[0]]: self.lopt += 1; self.ch_sfx.play(resources.SOUND['MENU_VER'])
					if self.pressed[resources.LEFT[0]]: self.opt -= 1; self.ch_sfx.play(resources.SOUND['MENU_HOR'])
					if self.pressed[resources.RIGHT[0]]: self.opt += 1; self.ch_sfx.play(resources.SOUND['MENU_HOR'])

					if self.opt < 0: self.opt = 2
					if self.opt > 2: self.opt = 0
					if self.lopt < 0: self.lopt = len(resources.TASKS) - 1
					if self.lopt > len(resources.TASKS) - 1: self.lopt = 0
				#STATUS MENU
				elif self.phone == 10:
					if self.pressed[resources.LEFT[0]]: self.opt -= 1; self.ch_sfx.play(resources.SOUND['MENU_HOR'])
					if self.pressed[resources.RIGHT[0]]: self.opt += 1; self.ch_sfx.play(resources.SOUND['MENU_HOR'])

					if self.opt < 0: self.opt = len(resources.PARTY[resources.FORMATION]) - 1
					if self.opt > len(resources.PARTY[resources.FORMATION]) - 1: self.opt = 0
				#TACTICS MENU
				elif self.phone == 11:
					#CHOOSING TACTICS
					if self.mnu == 0:
						if self.pressed[resources.ACT[0]]:
							self.ch_sfx.play(resources.SOUND['MENU_GO'])
							if self.lopt == len(resources.TACTICAL):
								resources.TACTICAL.append([0,0,0,0])
							self.mnu = 1
							self.opt = resources.TACTICAL[self.lopt][self.mnu - 1]

						if self.pressed[resources.UP[0]]: self.lopt -= 1; self.ch_sfx.play(resources.SOUND['MENU_VER'])
						if self.pressed[resources.DOWN[0]]: self.lopt += 1; self.ch_sfx.play(resources.SOUND['MENU_VER'])

						if self.lopt < 0: self.lopt = len(resources.TACTICAL)
						if self.lopt > len(resources.TACTICAL): self.lopt = 0
					#MANAGING TACTICS
					elif self.mnu > 0:
						if self.pressed[resources.ACT[0]]:
							self.ch_sfx.play(resources.SOUND['MENU_BACK'])
							if self.mnu < 5:
								self.mnu = 0
							else:
								del resources.TACTICAL[self.lopt]
								self.mnu = 0

						if self.pressed[resources.UP[0]]: self.opt -= 1; self.ch_sfx.play(resources.SOUND['MENU_VER'])
						if self.pressed[resources.DOWN[0]]: self.opt += 1; self.ch_sfx.play(resources.SOUND['MENU_VER'])
						if self.pressed[resources.LEFT[0]]: self.mnu -= 1; self.ch_sfx.play(resources.SOUND['MENU_HOR'])
						if self.pressed[resources.RIGHT[0]]: self.mnu += 1; self.ch_sfx.play(resources.SOUND['MENU_HOR'])

						if self.mnu > 0:
							if self.mnu < 1: self.mnu = 5
							if self.mnu > 5: self.mnu = 1
							if self.opt < 0: self.opt = 7
							if self.opt > 7: self.opt = 0

							if self.pressed[resources.LEFT[0]] or self.pressed[resources.RIGHT[0]]:
								if self.mnu < 5 and len(resources.TACTICAL) > 0: self.opt = resources.TACTICAL[self.lopt][self.mnu - 1]
							else:
								if self.mnu < 5 and len(resources.TACTICAL) > 0: resources.TACTICAL[self.lopt][self.mnu - 1] = self.opt
				#ACHIEVEMENTS MENU
				elif self.phone == 12:
					if self.pressed[resources.UP[0]]: self.lopt -= 1; self.ch_sfx.play(resources.SOUND['MENU_VER'])
					if self.pressed[resources.DOWN[0]]: self.lopt += 1; self.ch_sfx.play(resources.SOUND['MENU_VER'])

					if self.lopt < 0: self.lopt = len(database.ACHIEVEMENTS) - 1
					if self.lopt > len(database.ACHIEVEMENTS) - 1: self.lopt = 0
				#RAKING MENU
				#MANUAL MENU
				elif self.phone == 14:
					if self.mnu == 0:
						if self.pressed[resources.UP[0]]: self.lopt -= 1; self.ch_sfx.play(resources.SOUND['MENU_VER'])
						if self.pressed[resources.DOWN[0]]: self.lopt += 1; self.ch_sfx.play(resources.SOUND['MENU_VER'])

					if self.pressed[resources.ACT[0]]:
						if self.mnu == 0: self.mnu = 1; self.ch_sfx.play(resources.SOUND['MENU_GO'])
						elif self.mnu > 0: self.mnu = 0; self.ch_sfx.play(resources.SOUND['MENU_BACK'])

					if self.lopt < 0: self.lopt = len(database.MANUAL) - 1
					if self.lopt > len(database.MANUAL) - 1: self.lopt = 0
				#SETTINGS MENU
				elif self.phone == 15:
					if self.pressed[resources.UP[0]]: self.lopt -= 1; self.ch_sfx.play(resources.SOUND['MENU_VER'])
					if self.pressed[resources.DOWN[0]]: self.lopt += 1; self.ch_sfx.play(resources.SOUND['MENU_VER'])

					if self.mnu == 0:
						if self.lopt < 0: self.lopt = 3
						if self.lopt > 3: self.lopt = 0
					if self.mnu == 1:
						if self.lopt < 0: self.lopt = 7
						if self.lopt > 7: self.lopt = 0
					if self.mnu == 2:
						if self.lopt < 0: self.lopt = 1
						if self.lopt > 1: self.lopt = 0
					if self.mnu == 3:
						if self.lopt < 0: self.lopt = 7
						if self.lopt > 7: self.lopt = 0
					#MAIN SETTINGS
					if self.mnu == 0:
						if self.pressed[resources.ACT[0]]:
							if self.lopt == 3:
								self.phn = menu.Phone()
								self.inv = menu.Inventory()
								self.shpmnu = menu.Shop()
								resources.save_sett()
								self.ch_sfx.play(resources.SOUND['MENU_GO'])
								self.opt = 1
								self.lopt = 4
								self.phone = 1
								if resources.CHAPTER == 0 and resources.SCENE == 0:
									self.ch_ton.play(resources.SOUND['CALLING'],-1)
									self.ch_rng.play(resources.SOUND['RINGTONE_' + str(self.phn.pbg)],-1)
									self.phone = 17
									self.nb = '977904623'
							else:
								self.mnu = self.lopt + 1
								self.opt = 0
								self.lopt = 0
					#GAMEPLAY SETTINGS
					elif self.mnu == 1:
						if self.lopt == 0:
							if self.pressed[resources.LEFT[0]]:
								resources.LANG = 'EN'; self.ch_sfx.set_volume(resources.SFX); self.ch_sfx.play(resources.SOUND['MENU_HOR'])
							if self.pressed[resources.RIGHT[0]]:
								resources.LANG = 'PT'; self.ch_sfx.set_volume(resources.SFX); self.ch_sfx.play(resources.SOUND['MENU_HOR'])
						if self.lopt == 1:
							if self.pressed[resources.LEFT[0]]: resources.SPEED += 1; self.ch_sfx.set_volume(resources.SFX); self.ch_sfx.play(resources.SOUND['MENU_HOR'])
							if self.pressed[resources.RIGHT[0]]: resources.SPEED -= 1; self.ch_sfx.set_volume(resources.SFX); self.ch_sfx.play(resources.SOUND['MENU_HOR'])

							if resources.SPEED < 1: resources.SPEED = 5
							if resources.SPEED > 5: resources.SPEED = 1
						if self.lopt == 5:
							if self.pressed[resources.LEFT[0]]: resources.BORDER -= 1; self.ch_sfx.set_volume(resources.SFX); self.ch_sfx.play(resources.SOUND['MENU_HOR'])
							if self.pressed[resources.RIGHT[0]]: resources.BORDER += 1; self.ch_sfx.set_volume(resources.SFX); self.ch_sfx.play(resources.SOUND['MENU_HOR'])

							if resources.BORDER < 0: resources.BORDER = resources.RANGE_BORDER
							if resources.BORDER > resources.RANGE_BORDER: resources.BORDER = 0
						if self.lopt == 6:
							if self.pressed[resources.LEFT[0]]: resources.CENSORSHIP = False; self.ch_sfx.set_volume(resources.SFX); self.ch_sfx.play(resources.SOUND['MENU_HOR'])
							if self.pressed[resources.RIGHT[0]]: resources.CENSORSHIP = True; self.ch_sfx.set_volume(resources.SFX); self.ch_sfx.play(resources.SOUND['MENU_HOR'])
						if self.lopt == 7:
							if self.pressed[resources.LEFT[0]]: resources.HINT = False; self.ch_sfx.set_volume(resources.SFX); self.ch_sfx.play(resources.SOUND['MENU_HOR'])
							if self.pressed[resources.RIGHT[0]]: resources.HINT = True; self.ch_sfx.set_volume(resources.SFX); self.ch_sfx.play(resources.SOUND['MENU_HOR'])
						if self.lopt == 8:
							if self.pressed[resources.LEFT[0]]: resources.HELP = False; self.ch_sfx.set_volume(resources.SFX); self.ch_sfx.play(resources.SOUND['MENU_HOR'])
							if self.pressed[resources.RIGHT[0]]: resources.HELP = True; self.ch_sfx.set_volume(resources.SFX); self.ch_sfx.play(resources.SOUND['MENU_HOR'])
					#CONTROLS MENU
					elif self.mnu == 3:
						if self.pressed[resources.ACT[0]]:
							self.mnu = self.lopt + 4
							self.opt = 0
							self.lopt = 0
					#MOUSE SETTINGS
					elif self.mnu == 4:
						if self.lopt == 1:
							if self.pressed[resources.LEFT[0]]: resources.CURSOR -= 1; self.ch_sfx.set_volume(resources.SFX); self.ch_sfx.play(resources.SOUND['MENU_HOR'])
							if self.pressed[resources.RIGHT[0]]: resources.CURSOR += 1; self.ch_sfx.set_volume(resources.SFX); self.ch_sfx.play(resources.SOUND['MENU_HOR'])

							if resources.CURSOR < 0: resources.CURSOR = resources.RANGE_CURSOR
							if resources.CURSOR > resources.RANGE_CURSOR: resources.CURSOR = 0
						if self.pressed[resources.ACT[0]]:
							self.mnu = self.lopt + 4
							self.opt = 0
							self.lopt = 0
					#1P SETTINGS
					elif self.mnu == 5:
						#UP KEY
						if self.lopt == 0:
							if self.pressed[resources.ACT[0]]:
								if self.opt == 0: self.opt = 1
							else:
								if self.opt == 1:
									if event.key not in (resources.DOWN[0],resources.LEFT[0],resources.RIGHT[0],resources.ACT[0],resources.PHONE[0],resources.BAG[0],resources.RUN[0]):
										database.UP = event.key; self.opt = 0
						#DOWN KEY
						if self.lopt == 1:
							if self.pressed[resources.ACT[0]]:
								if self.opt == 0: self.opt = 1
							else:
								if self.opt == 1:
									if event.key not in (resources.UP[0],resources.LEFT[0],resources.RIGHT[0],resources.ACT[0],resources.PHONE[0],resources.BAG[0],resources.RUN[0]):
										database.DOWN = event.key; self.opt = 0
						#LEFT KEY
						if self.lopt == 2:
							if self.pressed[resources.ACT[0]]:
								if self.opt == 0: self.opt = 1
							else:
								if self.opt == 1:
									if event.key not in (resources.DOWN[0],resources.UP[0],resources.RIGHT[0],resources.ACT[0],resources.PHONE[0],resources.BAG[0],resources.RUN[0]):
										database.LEFT = event.key; self.opt = 0
						#RIGHT KEY
						if self.lopt == 3:
							if self.pressed[resources.ACT[0]]:
								if self.opt == 0: self.opt = 1
							else:
								if self.opt == 1:
									if event.key not in (resources.DOWN[0],resources.LEFT[0],resources.UP[0],resources.ACT[0],resources.PHONE[0],resources.BAG[0],resources.RUN[0]):
										database.RIGHT = event.key; self.opt = 0
						#ACT KEY
						if self.lopt == 4:
							if self.pressed[resources.ACT[0]]:
								if self.opt == 0: self.opt = 1
							else:
								if self.opt == 1:
									if event.key not in (resources.DOWN[0],resources.LEFT[0],resources.RIGHT[0],resources.UP[0],resources.PHONE[0],resources.BAG[0],resources.RUN[0]):
										database.ACT = event.key; self.opt = 0
						#RUN KEY
						if self.lopt == 5:
							if self.pressed[resources.ACT[0]]:
								if self.opt == 0: self.opt = 1
							else:
								if self.opt == 1:
									if event.key not in (resources.DOWN[0],resources.LEFT[0],resources.RIGHT[0],resources.UP[0],resources.PHONE[0],resources.BAG[0],resources.ACT[0]):
										database.RUN = event.key; self.opt = 0
						#PHONE KEY
						if self.lopt == 6:
							if self.pressed[resources.ACT[0]]:
								if self.opt == 0: self.opt = 1
							else:
								if self.opt == 1:
									if event.key not in (resources.DOWN[0],resources.LEFT[0],resources.RIGHT[0],resources.ACT[0],resources.UP[0],resources.BAG[0],resources.RUN[0]):
										database.PHONE = event.key; self.opt = 0
						#INVENTORY KEY
						if self.lopt == 7:
							if self.pressed[resources.ACT[0]]:
								if self.opt == 0: self.opt = 1
							else:
								if self.opt == 1:
									if event.key not in (resources.DOWN[0],resources.LEFT[0],resources.RIGHT[0],resources.ACT[0],resources.PHONE[0],resources.UP[0],resources.RUN[0]):
										database.BAG = event.key; self.opt = 0
					#GO BACK
					if self.pressed[resources.RUN[0]]:
						if self.mnu > 0:
							self.ch_sfx.play(resources.SOUND['MENU_BACK'])
							self.mnu = 0
				#ABOUT MENU
				elif self.phone == 16:
					if self.pressed[resources.UP[0]] and self.lopt == 1: self.lopt = 0; self.ch_sfx.play(resources.SOUND['MENU_VER'])
					if self.pressed[resources.DOWN[0]] and self.lopt == 0: self.lopt = 1; self.ch_sfx.play(resources.SOUND['MENU_VER'])

					if self.pressed[resources.ACT[0]]:
						self.ch_sfx.play(resources.SOUND['MENU_GO'])
						if self.lopt == 0:
							webbrowser.get('windows-default').open('twitter.com/kaixtr')
						if self.lopt == 1:
							webbrowser.get('windows-default').open('github.com/kaixtr')
				#CALLING
				elif self.phone == 17:
					if self.pressed[resources.LEFT[0]] and self.opt == 1: self.opt = 0; self.ch_sfx.play(resources.SOUND['MENU_VER'])
					if self.pressed[resources.RIGHT[0]] and self.opt == 0: self.opt = 1; self.ch_sfx.play(resources.SOUND['MENU_VER'])
					if self.pressed[resources.ACT[0]]:
						self.ch_ton.stop()
						self.ch_rng.stop()
						if self.opt == 0:
							wh = resources.CHARACTERS[resources.PARTY[resources.FORMATION][0]]['HAIR'] + resources.CHARACTERS[resources.PARTY[resources.FORMATION][0]]['SKIN']
							cl = resources.CHARACTERS[resources.PARTY[resources.FORMATION][0]]['COSTUME'] + resources.CHARACTERS[resources.PARTY[resources.FORMATION][0]]['SKIN']
							self.phone = 0
							self.ch_sfx.play(resources.SOUND['MENU_GO'])
							self.player[0]['DIRECTION'] = 0
							self.player[0]['SPEED'] = 0
							self.player[0]['SPRITE'] = 'CALL_' + cl
							if self.dlgfa > 0:
								self.dialog(database.DIALOGS[self.nb][0])
								resources.CALLHIST.append([self.nb,True])
								self.player[0]['SPRITE'] = 'STANDD_' + cl
						elif self.opt == 1:
							self.ch_sfx.play(resources.SOUND['MENU_BACK'])
							self.phone = 1
						self.nb = ''
						if self.radonoff == True: pygame.mixer.music.unpause()
						if resources.CHAPTER == 0 and resources.SCENE == 0:
							self.phone = 0
							self.ch_msc.play(resources.SOUND['AMBIENCE_SIREN'],-1)
							self.transiction(False, 50)
							#self.dialog(database.DIALOGS['HHBIANCA'][0])
							self.player[0]['PAUSE'] = 0
							self.transiction(False,0)
				#TAKING PHOTO
				elif self.phone == 18:
					if self.pressed[resources.ACT[0]]:
						rsg = False
						for j in range(len(resources.BESTIARY)):
							if len(self.foe) > 0 and resources.BESTIARY[j]['N'] == self.foe[0]['FILE'] and resources.BESTIARY[j]['SEEN'] == 1:
								fid = str(j)
								if int(fid) < 10: fid = '00' + fid
								elif int(fid) < 40: fid = '0' + fid
								resources.BESTIARY[j]['ID'] = fid
								resources.BESTIARY[j]['DATE'] = str(resources.DATE[0]) + '/' + str(resources.DATE[1])
								resources.BESTIARY[j]['SEEN'] = 2
								rsg = True
						if rsg == True:
							self.ch_sfx.play(resources.SOUND['CAMERA'])
							self.phone = 0
							self.mnu = 1
							self.notification(self.foe[0]['NAME'] + ' registrada',(134, 0, 211))
			#PLAYER HOLD AND DRIVE
			if self.battle == False and self.inventory == 0 and self.phone == 0 and self.shp == False and self.sleepin == False:
				p = 0
				for i in self.player:
					if i['PAUSE'] == 0 and i['PLAYING'] == True:
						#HOLDING OBJECTS
						if self.driving == 0:
							if i['JUMP'] == 0 and resources.MAP > 0:
								if self.pressed[resources.ACT[p]]:
									if i['HOLD'] != None:
										i['HOLD'] = None
						#DRIVING DIRECTIONS
						elif self.driving > 0:
							if resources.GAS > 0:
								if self.pressed[resources.LEFT[p]]:
									i['DIRECTION'] -= 1
									if i['DIRECTION'] == 0: i['DIRECTION'] = 8
								elif self.pressed[resources.RIGHT[p]]:
									i['DIRECTION'] += 1
									if i['DIRECTION'] == 9: i['DIRECTION'] = 1
					p += 1
		#PHONE HOLDING OPTIONS
		if self.phone > 0:
			#MAP MENU
			if self.phone == 2:
				if self.pressed[resources.UP[0]]: self.lopt += 3
				if self.pressed[resources.DOWN[0]]: self.lopt -= 3
				if self.pressed[resources.LEFT[0]]: self.opt += 3
				if self.pressed[resources.RIGHT[0]]: self.opt -= 3
				if self.pressed[resources.ACT[0]]: self.mnu += 5
				if self.pressed[resources.RUN[0]]: self.mnu -= 5

				if self.opt < 50: self.opt = 50
				if self.opt > 200: self.opt = 200
				if self.lopt < 50: self.lopt = 50
				if self.lopt > 200: self.lopt = 200
				if self.mnu < 50: self.mnu = 50
				if self.mnu > 200: self.mnu = 200
			#EMAIL READING
			elif self.phone == 4:
				if self.mnu > 0:
					if self.pressed[resources.UP[0]]: self.mnu -= 2
					if self.pressed[resources.DOWN[0]]: self.mnu += 2

					if self.mnu < 1: self.mnu = 1
					if self.mnu > 1000: self.mnu = 1000
			#NEWS READING
			elif self.phone == 5:
				if self.mnu > 0:
					if self.pressed[resources.UP[0]]: self.mnu -= 2
					if self.pressed[resources.DOWN[0]]: self.mnu += 2

					if self.mnu < 1: self.mnu = 1
					if self.mnu > 1000: self.mnu = 1000
			#RADIO OPTIONS
			elif self.phone == 6:
				if self.pressed[resources.LEFT[0]]: self.fm -= 1; self.vm -= 0.05
				if self.pressed[resources.RIGHT[0]]: self.fm += 1; self.vm += 0.05

				if self.fm < 0: self.fm = 180
				if self.fm > 180: self.fm = 0
				if self.vm < 0.0: self.vm = 1.0
				if self.vm > 1.0: self.vm = 0.0

				pygame.mixer.music.set_volume(self.vm)
				self.ch_ton.set_volume(1 - self.vm)
				if self.vm == 0.0 and self.radonoff == True:
					if resources.RADIO[str(math.floor(self.fm/20))] != []:
						pygame.mixer.music.load('Songs/FM_' + str(math.floor(self.fm/20)) + '/' + resources.RADIO[str(math.floor(self.fm/20))][self.msc])
						pygame.mixer.music.play()
					else: pygame.mixer.music.stop()
			#MANUAL READING
			elif self.phone == 13:
				if self.mnu > 0:
					if self.pressed[resources.UP[0]]: self.mnu -=1
					if self.pressed[resources.DOWN[0]]: self.mnu +=1
							
					if self.mnu < 1: self.mnu = 1
					if self.mnu > 1000: self.mnu = 1000
			#SETTINGS OPTIONS
			elif self.phone == 15:
				#COLORS SETTINGS
				if self.mnu == 1:
					if self.lopt == 2:
						if self.pressed[resources.LEFT[0]]: resources.COLOR[0] -= 5; self.ch_sfx.play(resources.SOUND['MENU_HOR'])
						if self.pressed[resources.RIGHT[0]]: resources.COLOR[0] += 5; self.ch_sfx.play(resources.SOUND['MENU_HOR'])

						if resources.COLOR[0] < 30: resources.COLOR[0] = 242
						if resources.COLOR[0] > 242: resources.COLOR[0] = 30
					if self.lopt == 3:
						if self.pressed[resources.LEFT[0]]: resources.COLOR[1] -= 5; self.ch_sfx.play(resources.SOUND['MENU_HOR'])
						if self.pressed[resources.RIGHT[0]]: resources.COLOR[1] += 5; self.ch_sfx.play(resources.SOUND['MENU_HOR'])

						if resources.COLOR[1] < 30: resources.COLOR[1] = 242
						if resources.COLOR[1] > 242: resources.COLOR[1] = 30
					if self.lopt == 4:
						if self.pressed[resources.LEFT[0]]: resources.COLOR[2] -= 5; self.ch_sfx.play(resources.SOUND['MENU_HOR'])
						if self.pressed[resources.RIGHT[0]]: resources.COLOR[2] += 5; self.ch_sfx.play(resources.SOUND['MENU_HOR'])

						if resources.COLOR[2] < 30: resources.COLOR[2] = 242
						if resources.COLOR[2] > 242: resources.COLOR[2] = 30
				#AUDIO SETTINGS
				if self.mnu == 2:
					if self.lopt == 0:
						if self.pressed[resources.LEFT[0]]: resources.SFX -= 0.1; self.ch_sfx.play(resources.SOUND['MENU_HOR'])
						if self.pressed[resources.RIGHT[0]]: resources.SFX += 0.1;  self.ch_sfx.play(resources.SOUND['MENU_HOR'])

						self.ch_sfx.set_volume(resources.SFX)
						self.ch_ton.set_volume(resources.SFX)
						self.ch_stp.set_volume(resources.SFX)
						self.ch_dlg.set_volume(resources.SFX)

						if resources.SFX < 0.0: resources.SFX = 0.0
						if resources.SFX > 1.0: resources.SFX = 1.0
					if self.lopt == 1:
						if self.pressed[resources.LEFT[0]]: resources.MSC -= 0.1; self.ch_msc.play(resources.SOUND['MENU_HOR'])
						if self.pressed[resources.RIGHT[0]]: resources.MSC += 0.1; self.ch_msc.play(resources.SOUND['MENU_HOR'])

						self.ch_msc.set_volume(resources.MSC)
						self.ch_rad.set_volume(resources.MSC)
						self.ch_rng.set_volume(resources.MSC)

						if resources.MSC < 0.0: resources.MSC = 0.0
						if resources.MSC > 1.0: resources.MSC = 1.0
		#PLAYER MOVEMENT
		p = 0
		for i in self.player:
			if i['PAUSE'] == 0 and i['PLAYING'] == True and self.battle == False:
				self.pressed = pygame.key.get_pressed()
				#MOVING OPTIONS
				if self.driving == 0:
					if i['JUMP'] == 0:
						if resources.MAP > 0:
							#RUN
							if self.pressed[resources.RUN[p]]:
								i['SPEED'] = 6 + math.floor(resources.CHARACTERS[resources.PARTY[resources.FORMATION][p]]['ATLETISM']/2)
								if i['SWIM'] != None: i['SPEED'] -= 3
								elif self.inv.space(p) == False: i['SPEED'] -= 2
							#WALK
							else:
								i['SPEED'] = 3 + math.floor(resources.CHARACTERS[resources.PARTY[resources.FORMATION][p]]['ATLETISM']/4)
								if i['SWIM'] != None: i['SPEED'] -= 1
								elif self.inv.space(p) == False: i['SPEED'] -= 1
						else: i['SPEED'] = 1
						#MOVE UP
						if self.pressed[resources.UP[p]]:
							if self.pressed[resources.LEFT[p]]: i['DIRECTION'] = 6
							elif self.pressed[resources.RIGHT[p]]: i['DIRECTION'] = 8
							else: i['DIRECTION'] = 7
						#MOVE DOWN
						elif self.pressed[resources.DOWN[p]]:
							if self.pressed[resources.LEFT[p]]: i['DIRECTION'] = 4
							elif self.pressed[resources.RIGHT[p]]: i['DIRECTION'] = 2
							else: i['DIRECTION'] = 3
						#MOVE LEFT
						elif self.pressed[resources.LEFT[p]]:
							if self.pressed[resources.UP[p]]: i['DIRECTION'] = 6
							elif self.pressed[resources.DOWN[p]]: i['DIRECTION'] = 4
							else: i['DIRECTION'] = 5
						#MOVE RIGHT
						elif self.pressed[resources.RIGHT[p]]:
							if self.pressed[resources.UP[p]]: i['DIRECTION'] = 8
							if self.pressed[resources.DOWN[p]]: i['DIRECTION'] = 2
							else: i['DIRECTION'] = 1
						else: i['SPEED'] = 0
				#DRIVING OPTIONS
				elif self.driving > 0:
					if self.pressed[resources.UP[p]]:
						self.driving = 0
						'''self.displayzw = 600
						self.displayzh = 400
						self.display[0] = pygame.Surface((600, 400))
						self.cam.width = self.displayzw
						self.cam.height = self.displayzh'''
						i['DIRECTION'] = 3
					if resources.GAS > 0:
						if self.pressed[resources.DOWN[p]]:
							if i['SPEED'] > 0.0: i['SPEED'] -= self.vehicles[self.driving - 1]['ACCELERATION']

						elif self.pressed[resources.RUN[p]]:
							if i['SPEED'] < self.vehicles[self.driving - 1]['SPEED'] and resources.GAS > 0.0:
								i['SPEED'] += self.vehicles[self.driving - 1]['ACCELERATION']
							resources.GAS -= self.vehicles[self.driving - 1]['GAS']
						else: i['SPEED'] -= self.vehicles[self.driving - 1]['ACCELERATION']
			#FOLLOW
			if i['FOLLOW'] != None:
				if i['FOLLOW'] != (None,None):
					i['SPEED'] = 3
					if i['RECT'].y - self.cam.y > i['FOLLOW'].y - self.cam.y:
						if i['RECT'].x - self.cam.x < i['FOLLOW'].x - self.cam.x: i['DIRECTION'] = 8
						elif i['RECT'].x - self.cam.x > i['FOLLOW'].x - self.cam.x: i['DIRECTION'] = 6
						else: i['DIRECTION'] = 7

					elif i['RECT'].y - self.cam.y < i['FOLLOW'].y - self.cam.y: 
						if i['RECT'].x - self.cam.x < i['FOLLOW'].x - self.cam.x: i['DIRECTION'] = 2
						elif i['RECT'].x - self.cam.x > i['FOLLOW'].x - self.cam.x: i['DIRECTION'] = 4
						else: i['DIRECTION'] = 3

					elif i['RECT'].x - self.cam.x < i['FOLLOW'].x - self.cam.x:
						if i['RECT'].y - self.cam.y > i['FOLLOW'].y - self.cam.y: i['DIRECTION'] = 8
						elif i['RECT'].y - self.cam.y < i['FOLLOW'].y - self.cam.y: i['DIRECTION'] = 2
						else: i['DIRECTION'] = 1

					elif i['RECT'].x - self.cam.x > i['FOLLOW'].x - self.cam.x:
						if i['RECT'].y - self.cam.y > i['FOLLOW'].y - self.cam.y: i['DIRECTION'] = 6
						elif i['RECT'].y - self.cam.y < i['FOLLOW'].y - self.cam.y: i['DIRECTION'] = 4
						else: i['DIRECTION'] = 5

					if self.colide(i['RECT'],i['FOLLOW']):
						i['DIRECTION'] = i['FOLLEND']
						i['FOLLOW'] = None
						i['FOLLEND'] = 'head'
						i['SPEED'] = 0
				else:
					i['DIRECTION'] = i['FOLLEND']
					i['FOLLOW'] = None
					i['FOLLEND'] = 'head'
					i['SPEED'] = 0
			#MOVING CHARACTER
			if self.colide(i, self.tilrect) == False:
				wh = resources.CHARACTERS[resources.PARTY[resources.FORMATION][p]]['HAIR'] + resources.CHARACTERS[resources.PARTY[resources.FORMATION][p]]['SKIN']
				cl = resources.CHARACTERS[resources.PARTY[resources.FORMATION][p]]['COSTUME'] + resources.CHARACTERS[resources.PARTY[resources.FORMATION][p]]['SKIN']
				#POSITION UPDATE
				if i['SPEED'] > 0 and i['JUMP'] == 0 and i['PLAYING'] == True:
					if i['DIRECTION'] == 1: i['RECT'].x += i['SPEED']
					elif i['DIRECTION'] == 2: i['RECT'].x += i['SPEED']; i['RECT'].y += i['SPEED']
					elif i['DIRECTION'] == 3: i['RECT'].y += i['SPEED']
					elif i['DIRECTION'] == 4: i['RECT'].x -= i['SPEED']; i['RECT'].y += i['SPEED']
					elif i['DIRECTION'] == 5: i['RECT'].x -= i['SPEED']
					elif i['DIRECTION'] == 6: i['RECT'].x -= i['SPEED']; i['RECT'].y -= i['SPEED']
					elif i['DIRECTION'] == 7: i['RECT'].y -= i['SPEED']
					elif i['DIRECTION'] == 8: i['RECT'].x += i['SPEED']; i['RECT'].y -= i['SPEED']
				elif i['JUMP'] > 0 and i['PLAYING'] == True:
					if i['DIRECTION'] == 3: i['RECT'].y += i['SPEED']
					elif i['DIRECTION'] == 7: i['RECT'].y -= i['SPEED']
				#PARTY FOLLOW
				if i['PLAYING'] == False:
					if len(self.player[p - 1]['NODES']) > 5:
						if self.player[p - 1]['SPEED'] > 0:
							i['SPEED'] = self.player[p - 1]['NODES'][0]['SPEED']
							i['RECT'] = self.player[p - 1]['NODES'][0]['RECT']
							i['DIRECTION'] = self.player[p - 1]['NODES'][0]['DIRECTION']
							del self.player[p - 1]['NODES'][0]
						else: i['SPEED'] = 0
				if len(self.player) > p + 1 and i['SPEED'] > 0: i['NODES'].append({'RECT': i['RECT'].copy(),'DIRECTION': i['DIRECTION'],'SPEED': i['SPEED']})
				#SPRITE UPDATE
				if i['JUMP'] > 0: spr = 'JUMP'
				elif self.driving > 0: spr = 'DRIVE'
				elif i['SPEED'] > 3: spr = 'RUN'
				elif i['SPEED'] > 0: spr = 'WALK'
				else: spr = 'STAND'
				if i['SPEED'] > 0 or i['FOLLEND'] == 'head':
					hed = 'BLANK'
					if i['DIRECTION'] == 1: i['HEAD'] = hed + 'R_' + wh
					elif i['DIRECTION'] == 2: i['HEAD'] = hed + 'RD_' + wh
					elif i['DIRECTION'] == 3: i['HEAD'] = hed + 'D_' + wh
					elif i['DIRECTION'] == 4: i['HEAD'] = hed + 'LD_' + wh
					elif i['DIRECTION'] == 5: i['HEAD'] = hed + 'L_' + wh
					elif i['DIRECTION'] == 6: i['HEAD'] = hed + 'LU_' + wh
					elif i['DIRECTION'] == 7: i['HEAD'] = hed + 'U_' + wh
					elif i['DIRECTION'] == 8: i['HEAD'] = hed + 'RU_' + wh
				if self.phone == 0:
					if i['DIRECTION'] == 1: i['SPRITE'] = spr + 'R_' + cl
					elif i['DIRECTION'] == 2: i['SPRITE'] = spr + 'RD_' + cl
					elif i['DIRECTION'] == 3: i['SPRITE'] = spr + 'D_' + cl
					elif i['DIRECTION'] == 4: i['SPRITE'] = spr + 'LD_' + cl
					elif i['DIRECTION'] == 5: i['SPRITE'] = spr + 'L_' + cl
					elif i['DIRECTION'] == 6: i['SPRITE'] = spr + 'LU_' + cl
					elif i['DIRECTION'] == 7: i['SPRITE'] = spr + 'U_' + cl
					elif i['DIRECTION'] == 8: i['SPRITE'] = spr + 'RU_' + cl

			if resources.GAS < 1.0: i['DIRECTION'] = 0
			if i['SPEED'] < 0: i['SPEED'] = 0
			p += 1
		#DIALOG SPEED
		if self.dlgfa == 0:
			self.pressed = pygame.key.get_pressed()
			self.dlgspd = resources.SPEED
			for i in resources.ACT:
				if self.pressed[i]: self.dlgspd = 1

	def dialog(self, tx, wh=0):
		self.dlg = []
		self.dlgy = 0
		self.lopt = 0
		self.speakin = wh
		self.player[0]['PAUSE'] = 1
		self.player[0]['SPEED'] = 0
		txt = tx
		tid = 0
		did = 0
		spd = 10
		while tid < len(txt):
			#TEXT
			if isinstance(txt[tid], str):
				while self.dlgfa > 0:
					if self.winbar < 50 and self.battle == False: self.winbar += 5
					self.dlgfa -= 50
					self.run()
				else:
					self.dlg.append('')
					for i in txt[tid]:
						while True:
							if spd > 0: spd -= 10/self.dlgspd
							else:
								if self.ch_dlg.get_busy(): self.ch_sfx.play(resources.SOUND['TEXT_INPUT'])
								else: self.ch_dlg.play(resources.SOUND['TEXT_INPUT'])
								self.dlg[did] += i
								spd = 10
								break
							self.run()
					did += 1
			#DIALOG PROTOCOLS
			else:
				#SIDE MESSAGE
				if txt[tid] == 0:
					self.dlg.append(0)
					did += 1
				#WAIT FOR PRESS
				elif txt[tid] == 1:
					self.dlg.append(1)
					self.wait()
					self.ch_ton.play(resources.SOUND['MENU_GO'])
					did += 1
				#CHAPTER INTRO
				elif txt[tid] == 2:
					resources.SCENE = -1
					self.ch_msc.pause()
					self.ch_ton.play(resources.SOUND['BAUM'])
					self.player[0]['PAUSE'] = 3
					for i in range(100): self.run()
					resources.SCENE = 0
					self.player[0]['PAUSE'] = 1
					self.ch_msc.unpause()
				#CHAPTER END
				elif txt[tid] in [3,4]:
					self.scrmov = 0
					pygame.mixer.stop()
					self.player[0]['PAUSE'] = 3
					self.ch_ton.play(resources.SOUND['CHAPTER_END'])
					for i in range(120): self.run()
					if txt[tid] == 3: resources.CHAPTER += 1
					self.classrun = 2
				#MONEY GET
				elif txt[tid][0] == 0 and self.notx == 0:
					src = None
					for i in resources.PARTY[resources.FORMATION]:
						src = self.inv.find(i,'credit_card')
						if src == None:
							src = self.inv.find(i,'wallet')
							if src != None: break
						else: break
					if src != None:
						if len(src[1]) <= 6: src[1] = str(int(src[1]) + txt[tid][1])
						else: src[1] = str(int(src[1][0:6]) + txt[tid][1]) + src[1][6:]
						self.ch_sfx.play(resources.SOUND['CASH_GET'])
						self.notification('Adquiriu $' + str(txt[tid][1]),(255, 255, 255))
				#ITEM GET
				elif txt[tid][0] == 1 and self.notx == 0:
					if len(txt[tid]) > 4: prp = txt[tid][4]
					else: prp = '0000'
					gt = True
					if txt[tid][2] != 0:
						src = None
						for i in resources.PARTY[resources.FORMATION]:
							src = self.inv.find(i,'credit_card')
							if src == None:
								src = self.inv.find(i,'wallet')
								if src != None: break
							else: break
						if src == None: gt = False
						if int(src[1]) < txt[tid][2]: gt = False
					if txt[tid][3] > 0:
						if database.CHESTS[self.room][txt[tid][3] - 1] == False:
							database.CHESTS[self.room][txt[tid][3] - 1] = True
						else:
							for j in database.DIALOGS['EMPTY CHEST'][::-1]:
								txt.insert(tid + 1, j)
								gt = False
					if gt == True:
						if txt[tid][2] != 0:
							if len(src[1]) <= 6: src[1] = str(int(src[1]) - txt[tid][2])
							else: src[1] = str(int(src[1][0:6]) - txt[tid][2]) + src[2][6:]
						self.inv.add(resources.PARTY[resources.FORMATION][0],txt[tid][1],prp)
						self.ch_sfx.play(resources.SOUND['ITEM_GET'])
						self.notification('Adquiriu ' + database.ITEMS[txt[tid][1]][0],(255, 255, 255))
				#MORALITY
				elif txt[tid][0] == 2 and self.notx == 0:
					resources.CHARACTERS[resources.PARTY[resources.FORMATION][0]]['MORALITY'] += txt[tid][1]
					self.ch_sfx.play(resources.SOUND['NOTIFICATION'])
					self.notification('ml_'+str(txt[tid][1]),(0, 0, 0))
				#MAP MARKER
				elif txt[tid][0] == 3 and self.notx == 0:
					self.ch_sfx.play(resources.SOUND['NOTIFICATION'])
					self.notification('Marcador adicionado',(140, 255, 253))
				#CALLING
				elif txt[tid][0] == 4:
					if txt[tid][1] != 'stop':
						self.ch_ton.play(resources.SOUND['CALLING'],-1)
						self.ch_rng.play(resources.SOUND['RINGTONE_' + str(self.phn.pbg)])
						if self.radonoff == True: pygame.mixer.music.pause()
						tw = 0
						cl = False
						while tw < 2000 and cl == False:
							pygame.time.wait(10)
							for event in pygame.event.get():
								if event.type == pygame.KEYUP:
									cl = True
							tw += 1
						self.ch_ton.stop()
						self.ch_rng.stop()
						self.ch_sfx.play(resources.SOUND['EQUIP'])
						if cl == True:
							self.phone = 3
							self.mnu = 1
							txt.insert(tid + 1, [2,'stop'])
							txt.insert(tid + 1, 0)
							for i in self.phn.call(str(database.CONTACTS[txt[tid][1]][1]),0,False,False)[-1:0:-1]:
								txt.insert(tid + 1, i)
					else:
						self.phone = 0
						self.mnu = 0
				#NEW EMAIL
				elif txt[tid][0] == 5 and self.notx == 0:
					self.ch_sfx.play(resources.SOUND['NOTIFICATION'])
					mail = database.EMAILS[txt[tid][1]].copy()
					mail.append(0)
					resources.INBOX.append(mail)
					resources.inbx_save(len(resources.INBOX)-1,0)
					self.notification('Novo email',(255, 221, 0))
				#NEW TASK
				elif txt[tid][0] == 6 and self.notx == 0:
					self.ch_sfx.play(resources.SOUND['NOTIFICATION'])
					if txt[tid][2] == False:
						resources.TASKS.append([database.TASKINDEX[txt[tid][1]], 0])
						resources.task_save(txt[tid][1],0)
						self.notification('Nova tarefa disponível',(255, 123, 0))
					elif self.inv.find(resources.PARTY[resources.FORMATION][0],txt[tid][1]):
						self.ch_ton.play(resources.SOUND['ITEM_GET'])
						for j in txt[tid][3][::-1]:
							txt.insert(tid + 1, j)
					else:
						for j in txt[tid][2][::-1]:
							txt.insert(tid + 1, j)
				#NEW CONTACT
				elif txt[tid][0] == 7 and self.notx == 0:
					self.ch_sfx.play(resources.SOUND['NOTIFICATION'])
					database.CONTACTS.append(database.NUMBERS[txt[tid][1]].copy())
					database.call_save(len(database.CONTACTS)-1)
					self.notification('Contato adicionado',(165, 255, 0))
				#ACHIEVEMENT
				elif txt[tid][0] == 8 and self.notx == 0:
					self.ch_sfx.play(resources.SOUND['ACHIEVEMENT'])
					database.ACHIEVEMENTS[txt[tid][1]][2] = True
					self.notification(database.ACHIEVEMENTS[txt[tid][1]][0],(255, 191, 0))
				#RANKING
				elif txt[tid][0] == 9 and self.notx == 0:
					self.ch_sfx.play(resources.SOUND['NOTIFICATION'])
					self.notification('Subiu de posição!',(56, 255, 0))
				#DIALOG CHOICES
				elif txt[tid][0] == 10:
					while self.dlgfa > 0:
						if self.winbar < 50 and self.battle == False: self.winbar += 5
						self.dlgfa -= 50
						self.run()
					else:
						self.speakin = 0
						self.dlg.append(0)
						for j in txt[tid][-1:0:-1]:
							self.dlg.append(j[0])
						self.dlg.append(0)
						self.diopt(len(txt[tid][1:]))
						self.speakin = wh
						for j in txt[tid][self.lopt][-1:0:-1]:
							txt.insert(tid + 1, j)
						self.lopt = 0
						did = len(self.dlg)
				#SKIP DIALOGS
				elif txt[tid][0] == 11:
					tid += txt[tid][1]
				#RETURN DIALOGS
				elif txt[tid][0] == 12:
					tid -= txt[tid][1]
				#BATTLE
				elif txt[tid][0] == 13:
					self.dlg = []
					pygame.mixer.music.stop()
					for i in txt[tid][1:]:
						fo = database.FREAKS[i].copy()
						fo['FILE'] = i
						fo['SPRITE'] = pygame.image.load('Sprites/frk_' + (fo['FILE']) + '_stand.png')
						siz = fo['SPRITE'].get_rect()
						fo['MASK'] = pygame.Rect(230,280 - siz.height,44,85)
						fo['DIRECTION'] = False
						fo['FIGHTING'] = False
						fo['HEALTH'] = 0
						fo['FADE'] = 10
						if fo['TYPE'] == 'mercenary': self.mrc.append(fo)
						else: self.foe.append(fo)
					txt = []
					tid = 0
					self.mnu = 0
					self.turn = -5
					self.fight()
				#ARMY BATTLE
				elif txt[tid][0] == 14:
					self.dlg = []
					pygame.mixer.music.stop()
					for k in range(txt[tid][1]):
						for f in txt[tid][2]:
							i = database.FREAKS[f].copy()
							i['FILE'] = f
							i['SPRITE'] = pygame.image.load('Sprites/frk_' + (i['FILE']) + '_stand.png')
							siz = i['SPRITE'].get_rect()
							i['MASK'] = pygame.Rect(230,280 - siz.height,44,85)
							i['DIRECTION'] = False
							i['FIGHTING'] = False
							i['HEALTH'] = 0
							i['FADE'] = 10
							if i['TYPE'] == 'mercenary': self.mrc.append(i)
							else: self.foe.append(i)
					txt = []
					tid = 0
					self.mnu = 0
					self.turn = -4
					self.fight()
				#PLAY MUSIC
				elif txt[tid][0] == 15:
					if txt[tid][2] == 0:
						if len(txt[tid]) > 2: lp = txt[tid][2]
						else: lp = 0
						self.ch_sfx.play(resources.SOUND[txt[tid][1]],lp)
					if txt[tid][2] == 1:
						pygame.mixer.music.load('Music/' + txt[tid][1] + '.mp3')
						pygame.mixer.music.play(-1)
				#CHECK CHARACTER
				elif txt[tid][0] == 16:
					if resources.PARTY[resources.FORMATION][0] == txt[tid][1]:
						for j in txt[tid][2][::-1]:
							txt.insert(tid + 1, j)
				#DELIVERY
				elif txt[tid][0] == 17:
					self.waitlst.append(['delivery',self.waitime + txt[tid][2],txt[tid][3]])
				#CHANGE PARTY
				elif txt[tid][0] == 18:
					ap = []
					p = 0
					for i in txt[tid][1:]:
						if i[1] != None:
							for n in range(len(self.npcs)):
								if i[1] == self.npcs[n]['N']:
									player = self.player[p].copy()
									xx = player['RECT'].x
									yy = player['RECT'].y
									dd = player['DIRECTION']
									cc = resources.CHARACTERS[resources.PARTY[resources.FORMATION][p]].copy()
									ii = cc['HAIR'] + cc['COSTUME'] + cc['SKIN']
									npc = self.npcs[n].copy()
									self.player[p]['RECT'].x = npc['RECT'].x
									self.player[p]['RECT'].y = npc['RECT'].y
									self.player[p]['DIRECTION'] = npc['DIRECTION']
									self.player[p]['FOLLEND'] = 'head'
									self.player[p]['SPEED'] = 0
									self.npcs[n]['RECT'].x = xx
									self.npcs[n]['RECT'].y = yy
									self.npcs[n]['INDEX'] = ii
									self.npcs[n]['DIRECTION'] = dd
									self.npcs[n]['MOVE'] = 'stand'
									if len(i) > 2: self.npcs[n]['WHO'] = i[2]
						ap.append(i[0])
						p += 1
					resources.PARTY[resources.FORMATION] = ap
				#DECREASE STATUS
				elif txt[tid][0] == 19:
					for i in self.foe + self.mrc:
						prb = round(random.randint(0,20))
						if prb > 10:
							self.ch_sfx.play(resources.SOUND['ATTRIBUTE_LOSS'])
							if i['TYPE'] == 'spirit': tst = self.fig[self.turn]['SPIRITS']
							else: tst = self.fig[self.turn]['INTIMIDATION']
							if txt[tid][1] == 0:
								i['STRENGHT'] -= txt[tid][2] + tst
								self.hitisplay(0, self.aim, '-' + str(txt[tid][2]) + ' ' + database.BATTLE[24].lower(), (200, 20, 20))
							if txt[tid][1] == 1:
								i['AGILITY'] -= txt[tid][2] + tst
								self.hitisplay(0, self.aim, '-' + str(txt[tid][2]) + ' ' + database.BATTLE[23].lower(), (20, 200, 20))
							if txt[tid][1] == 2:
								i['RESISTANCE'] -= txt[tid][2] + tst
								self.hitisplay(0, self.aim, '-' + str(txt[tid][2]) + ' ' + database.BATTLE[25].lower(), (20, 20, 200))
				#INCREASE STATUS
				elif txt[tid][0] == 20:
					prb = round(random.randint(0,20))
					if prb > 10:
						self.ch_sfx.play(resources.SOUND['ATTRIBUTE_GAIN'])
						if txt[tid][1] == 0:
							self.pstr[self.turn] += txt[tid][2] + self.fig[self.turn]['CARISM']
							self.hitisplay(0, self.aim, '+' + str(txt[tid][2]) + ' ' + database.BATTLE[24].lower(), (200, 20, 20))
						if txt[tid][1] == 1:
							self.pagi[self.turn] += txt[tid][2] + self.fig[self.turn]['CARISM']
							self.hitisplay(0, self.aim, '+' + str(txt[tid][2]) + ' ' + database.BATTLE[23].lower(), (20, 200, 20))
						if txt[tid][1] == 2:
							self.pres[self.turn] += txt[tid][2] + self.fig[self.turn]['CARISM']
							self.hitisplay(0, self.aim, '+' + str(txt[tid][2]) + ' ' + database.BATTLE[25].lower(), (20, 20, 200))
				#NEXT SCENE
				elif txt[tid][0] == 21:
					if isinstance(txt[tid][1],str): resources.DLGSAV[txt[tid][1]] = txt[tid][2]
					else: resources.SCENE = txt[tid][1]
				#NAME INPUT
				elif txt[tid][0] == 22:
					snd = self.ch_msc.get_sound()
					self.ch_msc.stop()
					self.nmenu = menu.Naming()
					self.nmenu.ninput = txt[tid][1]
					self.nmenu.show = True
					self.FPS = 0
					while self.nmenu.show == True:
						self.nmenu.events()
						self.nmenu.run()
						self.run()
					self.FPS = 60
					database.load_dialogs()
					if snd != None: self.ch_msc.play(snd,-1)
				#GET OTHER DIALOG
				elif txt[tid][0] == 23:
					dlg = txt[tid][1]
					idx = None
					if len(txt[tid]) > 2: idx = txt[tid][2]
					if self.battle == True:
						if dlg == None: dlg = self.foe[self.opt]['FILE']
						if database.FREAKS[dlg]['TYPE'] not in ('humanoid','psychic'):
							dlg = 'IRRATIONAL'
						else: dlg = self.foe[self.opt]['FILE'].upper()
					if idx == None:
						for j in database.DIALOGS[dlg].copy()[::-1]:
							txt.insert(tid + 1, j)
					else:
						for j in database.DIALOGS[dlg][idx].copy()[::-1]:
							txt.insert(tid + 1, j)
					did = len(self.dlg)
				#MOVE CHARACTER
				elif txt[tid][0] == 24:
					px = txt[tid][2][0]
					py = txt[tid][2][1]
					if isinstance(px,str): px = self.player[0]['RECT'].x + int(px[2:])
					if isinstance(py,str): py = self.player[0]['RECT'].y + int(py[2:])
					if txt[tid][1] == None:
						if txt[tid][2] != (None,None):
							self.player[0]['FOLLOW'] = pygame.Rect(px,py,10,10)
						else: self.player[0]['FOLLOW'] = (None,None)
						self.player[0]['FOLLEND'] = txt[tid][3]
						if len(txt[tid]) > 4: self.player[0]['FOLLMOV'] = txt[tid][4]
					else:
						if txt[tid][1] == 'n':
							n = 0
							for i in self.npcs:
								if i['N'] > n: n = i['N']
						else: n = txt[tid][1]
						for i in self.npcs:
							if i['N'] == n:
								if txt[tid][2] != (None,None):
									i['FOLLOW'] = pygame.Rect(px,py,10,10)
								else: i['FOLLOW'] = (None,None)
								i['FOLLEND'] = txt[tid][3]
								if len(txt[tid]) > 4: i['FOLLMOV'] = txt[tid][4]
				#CHARACTER EMOTION
				elif txt[tid][0] == 25:
					if txt[tid][1] == None:
						self.player[0]['HEAD'] = txt[tid][2] + '_' + resources.CHARACTERS[resources.PARTY[resources.FORMATION][0]]['HAIR'] + resources.CHARACTERS[resources.PARTY[resources.FORMATION][0]]['SKIN']
					else:
						for i in self.npcs:
							if i['N'] == txt[tid][1]:
								i['HEAD'] = txt[tid][2] + '_' + i['INDEX'][0:3] + i['INDEX'][5]
				#CAMERA
				elif txt[tid][0] == 26:
					if isinstance(txt[tid][1],int):
						for i in self.npcs:
							if i['N'] == txt[tid][1]:
								self.speakin = i['RECT']
					else: self.speakin = pygame.Rect(txt[tid][1][0],txt[tid][1][1],1,1)
				#WAIT
				elif txt[tid][0] == 27:
					ds = self.dlg.copy()
					self.dlg = []
					if len(txt[tid]) > 2 and txt[tid][2] == 'TWNN': self.cityname = 'TWNN'
					for i in range(txt[tid][1]): self.run()
					if len(txt[tid]) > 2 and txt[tid][2] == 'TWNN': self.cityname = ''
					self.dlg = ds
				#TUTORIAL
				elif txt[tid][0] == 28:
					if resources.HINT == True:
						self.ch_ton.play(resources.SOUND['NOTIFICATION'])
						self.tutorial = {'TEXT': database.TUTORIALS[txt[tid][1]].copy(), 'OUTPUT': [], 'FADE': 0, 'TIME': 0, 'WAIT': 300, 'NEXT': '','GO': 0}
						for j in self.tutorial['TEXT']:
							if isinstance(j,list):
								if j[0] == 'phone':
									self.tutorial['GO'] = j[1]
									if len(j) > 2: self.tutorial['NEXT'] = j[2]
								if j[0] == 'wait':
									self.tutorial['WAIT'] = j[1]
									if len(j) > 2: self.tutorial['NEXT'] = j[2]
								if j[0] == 'image':
									self.tutorial['OUTPUT'].append(j)
							else: self.tutorial['OUTPUT'].append(j)
				#ANOTHER PLACE
				elif txt[tid][0] == 29:
					ds = self.dlg.copy()
					self.dlg = []
					self.transiction(True, 210, 10)
					self.rendermap(txt[tid][1])
					self.player[0]['RECT'].x = txt[tid][2]
					self.player[0]['RECT'].y = txt[tid][3]
					self.transiction(False, 50, 10)
					self.dlg = ds
				#PUT CHARACTER
				elif txt[tid][0] == 30:
					ind = 0
					for n in self.npcs:
						if n['N'] > ind: ind = n['N']
					ind += 1
					self.npcs.append({'N': ind, 'RECT': pygame.Rect(txt[tid][1][0], txt[tid][1][1], 0, 0), 'TYPE': txt[tid][4], 'INDEX': txt[tid][2], 'WHO': txt[tid][3],
					'GIF': 0.0,'BLINK': 100,'HEAD': 'BLANKD_' + txt[tid][2][0:3] + txt[tid][2][5],'SPRITE': 'STANDD_' + txt[tid][2][3:6],'MOVE': 'fixed','DIRECTION': 3,'SPEED': 0,
					'JUMP': 0,'GRAVITY': -5,'TIME': 20,'FOLLOW': None,'FOLLEND': 0,'FOLLMOV': '','TALKING': False,'SWIM': None,'HOLD': None,'PAUSE': 0})
					self.objects.append([2,ind,txt[tid][1][1]])
				#CENSORSHIP
				elif txt[tid][0] == 31:
					if resources.CENSORSHIP == False: txt.insert(tid + 1, txt[tid][2])
					elif resources.CENSORSHIP == True: txt.insert(tid + 1, txt[tid][1])
			tid += 1

		self.dlg = []
		self.speakin = 0
		self.player[0]['PAUSE'] = 0

		while self.dlgfa < 500:
			self.dlgfa += 50
			if self.winbar > 0 and self.battle == False:
				self.winbar -= 5
				self.run()

	def diopt(self, ln):
		self.lopt = 1
		trigger = True
		while trigger:
			self.run()
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					trigger = False
					pygame.quit()
					sys.exit()
				self.pressed = pygame.key.get_pressed()
				if self.pressed[resources.UP[0]]:
					if self.lopt < ln: self.ch_sfx.play(resources.SOUND['MENU_HOR']); self.lopt += 1
				if self.pressed[resources.DOWN[0]]:
					if self.lopt > 1: self.ch_sfx.play(resources.SOUND['MENU_VER']); self.lopt -= 1
				if self.pressed[resources.ACT[0]]:
					self.ch_ton.play(resources.SOUND['MENU_GO'])
					i = 1
					crg = -1
					while i <= ln + 1:
						if i != self.lopt: del self.dlg[crg - i]; crg += 1; ln -= 1
						i += 1
					trigger = False
					break

	def wait(self):
		waiting = True
		while waiting == True:
			self.events()
			self.draw()
			self.glock.tick(self.FPS)
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					waiting = False
					pygame.quit()
					sys.exit()
				if event.type == pygame.KEYDOWN:
					waiting = False
				if event.type == pygame.MOUSEBUTTONUP and resources.MOUSE == True:
					waiting = False

	def confirmation(self):
		yesno = 0
		opt = 1
		brd = pygame.Surface((200,100))
		brd.fill((resources.COLOR[0],resources.COLOR[1],resources.COLOR[2]))
		for x in range(20):
			for y in range(10):
				brd.blit(pygame.image.load('Sprites/border_' + str(resources.BORDER) + '.png'), (x * 10, y * 10))
		pygame.draw.rect(brd, (0,0,0), pygame.Rect(10,10,180,80))
		txt = pygame.Surface((360,160))
		while yesno == 0:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
				self.pressed = pygame.key.get_pressed()
				if self.pressed[resources.LEFT[0]]: self.ch_sfx.play(resources.SOUND['MENU_HOR']); opt = 1
				if self.pressed[resources.RIGHT[0]]: self.ch_sfx.play(resources.SOUND['MENU_VER']); opt = 2
				if self.pressed[resources.ACT[0]]:
					yesno = opt
					if yesno == 1: self.ch_sfx.play(resources.SOUND['MENU_GO'])
					if yesno == 2: self.ch_sfx.play(resources.SOUND['MENU_BACK'])
					opt = 0
			txt.fill((0,0,0))
			txt.blit(self.fnt['DEFAULT'].render(database.MENU[85], True, (255, 255, 255)), (90, 20))
			if opt == 1: txt.blit(self.fnt['DEFAULT'].render(database.MENU[83], True, (resources.COLOR[0],resources.COLOR[1],resources.COLOR[2])), (80, 100))
			else: txt.blit(self.fnt['DEFAULT'].render(database.MENU[83], True, (255, 255, 255)), (80, 100))
			if opt == 2: txt.blit(self.fnt['DEFAULT'].render(database.MENU[84], True, (resources.COLOR[0],resources.COLOR[1],resources.COLOR[2])), (220, 100))
			else: txt.blit(self.fnt['DEFAULT'].render(database.MENU[84], True, (255, 255, 255)), (220, 100))

			self.display[0].blit(brd,(195,145))
			self.display[1].blit(txt,(410,310))
			self.screen.blit(pygame.transform.scale(self.display[0], (self.windoww, self.windowh)), (self.displayx, self.displayy))
			self.screen.blit(pygame.transform.scale(self.display[1], (self.windoww, self.windowh)), (self.displayx, self.displayy))
			pygame.display.update(400,300,380,180)
			self.glock.tick(self.FPS)

		return yesno

	def transiction(self, fade, limit, spd=5):
		if fade == False:
			while self.winbar > limit:
				self.winbar -= spd
				if self.winbar > limit: self.run()
			if self.winbar > limit: self.winbar = limit
		else:
			while self.winbar < limit:
				self.winbar += spd
				if self.winbar < limit: self.run()
			if self.winbar < limit: self.winbar = limit

	def fight(self):
		#BATTLE START
		if self.turn < 0:
			#PLAY SOUND
			self.inventory = 0
			self.phone = 0
			self.shp = False
			self.player[0]['PAUSE'] = 2
			self.player[0]['SPEED'] = 0
			if self.radonoff == True: pygame.mixer.music.pause()
			if self.turn == -1: self.ch_ton.play(resources.SOUND['BATTLE_FOE'])
			elif self.turn == -2: self.ch_ton.play(resources.SOUND['BATTLE_ENEMY'])
			elif self.turn == -3: self.ch_ton.play(resources.SOUND['BATTLE_AMBUSH'])
			elif self.turn == -6: self.ch_ton.play(resources.SOUND['BATTLE_FOE'])
			else: self.ch_ton.play(resources.SOUND['BATTLE_BOSS'])
			if self.driving > 0: self.obstacles = True
			#ZOOM TRANSITION
			if self.turn != -6:
				acc = 0
				while True:
					self.displayzw -= acc * 6
					self.displayzh -= acc * 4
					self.cam.x += acc * 3
					self.cam.y += acc * 2
					self.cam.width = self.displayzw
					self.cam.height = self.displayzh
					if self.displayzw > 6: self.display[0] = pygame.Surface((self.displayzw, self.displayzh))
					else:
						self.displayzw = 6; self.displayzh = 4;
						self.cam.width = 6; self.cam.height = 4;
						self.display[0] = pygame.Surface((self.displayzw, self.displayzh))
						break
					self.draw()
					acc += 1
				self.battle = True
			#MYSTERIOUS FREAK
			else:
				freakname = self.foe[0]['NAME'].lower()
				showname = ''
				self.speakin = self.foe[0]['RECT']
				for i in range(30): self.run()
				self.transiction(True,210)
				for i in range(len(freakname)):
					for l in ' abcdefghijklmnopqrstuvwxyzãâáàéèêóòôõíúç':
						showname = showname[:-1] + l
						self.cityname = showname
						self.run()
						if showname[-1] == freakname[i]: break
					showname += ' '
				for i in range(60): self.run()
				self.cityname = ''
				self.speakin = 0
				self.battle = True
			self.fig = []
			tr = 0
			for i in resources.PARTY[resources.FORMATION]:
				dt = resources.CHARACTERS[i]
				if dt['HP'] > 0:
					dt['N'] = tr
					self.fig.append(dt)
				tr += 1
			#BACKGROUND
			self.bbg = pygame.image.load('Backgrounds/mountains.png')
			self.bbm = 0
			#SET UP PARTY
			self.player[0]['SPEED'] = 0
			self.pstr = []
			self.patt = []
			self.pagi = []
			self.pres = []
			self.tatt = []
			self.tagi = []
			self.tstr = []
			self.tres = []
			self.opt = 0
			p = 0
			for i in resources.PARTY[resources.FORMATION]:
				self.pstr.append(database.CLASSES[resources.CHARACTERS[i]['CLASS']]['STRENGHT'][resources.CHARACTERS[i]['LEVEL']])
				self.patt.append(database.CLASSES[resources.CHARACTERS[i]['CLASS']]['ATTACK'][resources.CHARACTERS[i]['LEVEL']])
				self.pagi.append(database.CLASSES[resources.CHARACTERS[i]['CLASS']]['AGILITY'][resources.CHARACTERS[i]['LEVEL']])
				self.pres.append(database.CLASSES[resources.CHARACTERS[i]['CLASS']]['RESISTANCE'][resources.CHARACTERS[i]['LEVEL']])
				self.tatt.append(0)
				self.tagi.append(0)
				p += 1
			#SET UP FREAKS
			enx = 0
			while enx < len(self.foe):
				self.foe[enx]['MASK'].x += enx * 80
				dprb = [1,5]
				self.foe[enx]['DIRECTION'] = dprb[round(random.randint(0,1))]
				self.foe[enx]['VITALITY'] = self.foe[enx]['HP']
				enx += 1
			#SET UP MERCENARIES
			enx = 0
			while enx < len(self.mrc):
				self.mrc[enx]['MASK'].x += enx * 80
				self.mrc[enx]['DIRECTION'] = 5
				self.mrc[enx]['VITALITY'] = self.mrc[enx]['HP']
				enx += 1
			#CONDITIONS
			if len(self.foe) > 0:
				if self.turn == -3: self.foe[0]['SPRITE'] = pygame.image.load('Sprites/frk_' + (self.foe[0]['FILE']) + '_backwards.png'); self.foe[0]['HEALTH'] = 1
			else:
				if self.turn == -3: self.mrc[0]['SPRITE'] = pygame.image.load('Sprites/frk_' + (self.mrc[0]['FILE']) + '_backwards.png'); self.mrc[0]['HEALTH'] = 1
			#ZOOM TRANSITION
			if self.turn != -6:
				acc = 0
				while True:
					self.displayzw += acc * 6
					self.displayzh += acc * 4
					self.cam.x -= acc * 3
					self.cam.y -= acc * 2
					self.cam.width = self.displayzw
					self.cam.height = self.displayzh
					if self.displayzw < 600: self.display[0] = pygame.Surface((self.displayzw, self.displayzh))
					else:
						self.displayzw = 600; self.displayzh = 400;
						self.cam.x = 0; self.cam.y = 0;
						self.cam.width = 600; self.cam.height = 400;
						self.display[0] = pygame.Surface((self.displayzw, self.displayzh))
						break
					self.draw()
					acc += 1
			#PLAY SONG
			if len(self.foe) > 0: self.ch_msc.play(resources.SONGS[self.foe[0]['SONG']],-1)
			elif len(self.mrc) > 0: self.ch_msc.play(resources.SONGS[self.mrc[0]['SONG']],-1)
			self.player[0]['GIF'] = 0.0
			self.tilemation = 0.0
			#TRANSICTION
			if self.turn != -6: self.transiction(True, 100)
			else: self.turn = 0; self.transiction(False, 100)
			#SEEN ANOMALY
			chk = None
			for i in resources.BESTIARY:
				if len(self.foe) > 0:
					if self.foe[0]['FILE'] == i['N'] and i['SEEN'] == 0:
						chk = self.foe[0]['NAME']
						i['SEEN'] = 1
			if chk == None and len(self.mrc) > 0: chk = self.mrc[0]['NAME']
			#AMBUSH
			if self.turn == -2: self.turn = len(self.fig)
			else: self.turn = 0
			self.mnu = 1
		#PLAYERS TURN
		elif self.turn < len(resources.PARTY[resources.FORMATION]):
			print(self.pstr)
			print(self.patt)
			print(self.pagi)
			print(self.pres)
			again = False
			self.mnu = 3
			#WEAPONS
			if self.equip[self.turn] < 4:
				pp = int(resources.INVENTORY[resources.PARTY[resources.FORMATION][self.turn]][4][self.equip[self.turn] + 1][1])
				pp -= 1
				resources.INVENTORY[resources.PARTY[resources.FORMATION][self.turn]][4][self.equip[self.turn] + 1][1] = str(pp)
				gottem = False
				for i in self.foe + self.mrc:
					if self.colide(self.aim, i['MASK']) and i['FIGHTING'] == True:
						gottem = True
						wpdmg = database.ITEMS[resources.INVENTORY[resources.PARTY[resources.FORMATION][self.turn]][4][self.equip[self.turn] + 1][0]][5]['DAMAGE']
						dmg = int(random.randint(wpdmg - 2,wpdmg + 2)) - i['RESISTANCE'] + database.CLASSES[self.fig[self.turn]['CLASS']]['STRENGHT'][self.fig[self.turn]['LEVEL']]
						if resources.CHARACTERS[resources.PARTY[resources.FORMATION][self.turn]]['HEALTH'] == 11: dmg = int(dmg/2)
						if i['HEALTH'] != 1: i['SPRITE'] = pygame.image.load('Sprites/frk_' + (i['FILE']) + '_damage.png')
						#HIT
						if dmg > 0:
							for p in range(dmg * 2):
								if i['TYPE'] == 'mercenary': cl = (150, 25, 29)
								else: cl = (10, 255, 50)
								self.particles.append({'TYPE': 'blood', 'X': self.aim.x, 'Y': self.aim.y, 'RADIUS': round(random.randint(3,5)), 'DIRECTION': round(random.randint(0,360)),
									'SPEED': round(random.randint(2,6)), 'COLOR': cl})
							if dmg == wpdmg + 2 - i['RESISTANCE']:
								self.ch_sfx.play(resources.SOUND['CRITICAL'])
								self.hitisplay(10, i['MASK'], database.BATTLE[3], (200, 0, 0))
							else:
								self.ch_sfx.play(resources.SOUND['HIT'])
								self.hitisplay(10, i['MASK'], str(dmg), (200, 0, 0))
							if i['HEALTH'] != 1 and i['HP'] > 0: i['SPRITE'] = pygame.image.load('Sprites/frk_' + (i['FILE']) + '_stand.png')
							i['HP'] -= dmg
							self.hits += 1
							self.tdmg += dmg
						else: self.hitisplay(0, None, database.BATTLE[5], (255, 255, 255))
						#CHECK WIN
						if i['HP'] <= 0:
							if dmg >= i['VITALITY']: again = True
							self.ch_ton.play(resources.SOUND['SCREAM_' + i['FILE'].upper()])
							while i['FADE'] > 0:
								i['FADE'] -= 1
								self.run()
							if i['ITEM'] != None:
								prb = round(random.randint(0,100))
								if prb > i['ITEM'][1]:
									self.inv.add(resources.PARTY[resources.FORMATION][0],i['ITEM'][0])
									self.ch_sfx.play(resources.SOUND['ITEM_GET'])
									self.notification('Adquiriu ' + database.ITEMS[i['ITEM'][0]][0],(255, 255, 255))
							i['FIGHTING'] = False
				#MISS
				if gottem == False:
					self.ch_sfx.play(resources.SOUND['MISS'])
					self.hitisplay(5, self.aim, database.BATTLE[4], (200, 200, 200))
				self.mnu = 0
			#BATTLE DIALOG
			elif self.equip[self.turn] == 5:
				self.dialog(database.DIALOGS['BATTLEDIALOG'][resources.PARTY[resources.FORMATION][self.turn]])
				self.mnu = 1
			#RUN AWAY
			elif self.equip[self.turn] == 7:
				self.dialog([self.fig[self.turn]['NAME'] + database.BATTLE[15]])
				run = round(random.randint(0,20)) + self.fig[self.turn]['ATLETISM']
				if run > 10:
					self.ch_msc.fadeout(500)
					self.dialog([database.BATTLE[17]])
					self.transiction(True, 210)
					for i in self.en:
						i['FIGHTING'] = False
					self.turn = 0
					self.mnu = 0
					self.hits = 0
					self.tdmg = 0
					self.hpl = 0
					self.tbt = 0
					self.foe = []
					self.mrc = []
					self.battle = False
					self.opt = 1
					self.player[0]['RECT'].x += 150
					if self.radonoff == True: pygame.mixer.music.unpause()
					self.transiction(False, 0)
				else:
					self.dialog([database.BATTLE[16]])
			#EXTRA ATTACK
			if again == True and self.battle == True:
				self.ch_ton.play(resources.SOUND['ONE_MORE'])
				self.hitisplay(0, self.aim, database.BATTLE[5], (10, 50, 255))
				self.turn -= 1
			if self.turn < len(self.fig):
				self.aim.x = 100 + database.CLASSES[self.fig[self.turn]['CLASS']]['ATTACK'][self.fig[self.turn]['LEVEL']]
		#ENEMIES TURN
		else:
			self.inventory = 0
			self.phone = 0
			self.tbt += round(self.btime/10)
			self.btime = 100
			self.mnu = 3
			count = 0
			for i in self.foe + self.mrc:
				if i['HP'] > 0 and i['FIGHTING'] == True and i['HEALTH'] != 1 and len(self.fig) > 0:
					count += 1
					if count == 6: break
					#CONDITION DAMAGE
					if i['HEALTH'] > 9:
						i['HP'] -= 5
						self.hitisplay(5, i['MASK'], str(5), (200, 0, 0))
					#HABILITY
					prb = []
					for h in i['HABILITIES']:
						prb.append(h[4])
					opt = int(random.randint(0,100))
					rng = 100
					for p in range(len(prb)):
						rng -= prb[p]
						if opt >= rng:
							act = i['HABILITIES'][p].copy()
							break
					dd = i['NAME'] + database.BATTLE[18] + act[0]
					i['SPRITE'] = pygame.image.load('Sprites/frk_' + i['FILE'] + '_attack.png')
					#TARGET RANGE
					if i['TYPE'] != 'mercenary':
						otk = 0
						for d in self.mrc:
							if d['HP'] > 0: otk += 1
						if i['HEALTH'] == 7: pl = int(random.randint(-20,len(self.fig) - 1 + otk))
						else: pl = int(random.randint(-1,len(self.fig) - 1 + otk))
					else:
						otk = 0
						for d in self.foe:
							if d['HP'] > 0: otk += 1
						if i['HEALTH'] == 7: pl = int(random.randint(-20,len(self.fig) - 1 + otk))
						else: pl = int(random.randint(-1,len(self.fig) - 1 + otk))
					#DECREASE STATUS LIMIT
					if act[3] == 2 and self.tatt == 2: act = i['HABILITIES'][0]
					if act[3] == 3 and self.tagi == 2: act = i['HABILITIES'][0]
					#ATTACK
					if pl >= 0:
						if pl >= len(self.fig): act = ['','',-10,1]
						if act[3] == 1:
							#SIMPLE ATTACK
							if act[2] < 0:
								#ATTACK PARTY
								if pl < len(self.fig):
									for a in resources.INVENTORY[pl][:-1]:
										if a[0][0] != '_':
											act[2] += int(database.ITEMS[a[0][0]][5])
											a[0][1] = int(a[0][1])
											a[0][1] -=1
											if a[0][1] == 0:
												self.dialog([a[0][0] + database.BATTLE[36],1])
												a[0] = ['_','0000','_','0000','_','0000']
											a[0][1] = str(a[0][1])
									#FEAR
									if self.fig[pl]['FEAR'] == i['TYPE']: act[2] -= math.floor(act[2]/5)
									act -= i['STRENGHT'] + database.CLASSES[self.fig[pl]['CLASS']]['RESISTANCE']
									self.turn = self.fig[pl]['N']
									self.ch_ton.play(resources.SOUND['SCREAM_' + i['FILE'].upper()])
									self.ch_sfx.play(resources.SOUND['DAMAGE_1'])
									#DODGE
									if self.attackimation(act[5]) == True:
										act[2] -= math.floor(act[2]/5)
										self.hitisplay(5, i['MASK'], 'dodge', (0, 200, 0))
									#HIT
									if -act[2] > 0:
										self.fig[pl]['HP'] += act[2] + self.pres[pl]
										self.hitisplay(-act[2] * 2, None, '', (0,0,0))
									#NO DAMAGE
									else:
										self.fig[pl]['HP'] += -1
										self.hitisplay(2, None, '', (0,0,0))
									self.hpl += act[2]
								else:
									#ATTACK MERCENARY
									if i['TYPE'] != 'mercenary':
										print(i['NAME'] + ' atacou ' + self.mrc[pl - len(self.fig)]['NAME'])
										self.ch_sfx.play(resources.SOUND['HIT'])
										self.mrc[pl - len(self.fig)]['SPRITE'] = pygame.image.load('Sprites/frk_' + (self.mrc[pl - len(self.fig)]['FILE']) + '_damage.png')
										self.hitisplay(10, self.mrc[pl - len(self.fig)]['MASK'], str(act[2]), (0, 200, 0))
										self.mrc[pl - len(self.fig)]['SPRITE'] = pygame.image.load('Sprites/frk_' + (self.mrc[pl - len(self.fig)]['FILE']) + '_stand.png')
										self.mrc[pl - len(self.fig)]['HP'] += act[2]
									#ATTACK FREAK
									else:
										print(i['NAME'] + ' atacou ' + self.foe[pl - len(self.fig)]['NAME'])
										self.ch_sfx.play(resources.SOUND['HIT'])
										self.foe[pl - len(self.fig)]['SPRITE'] = pygame.image.load('Sprites/frk_' + (self.foe[pl - len(self.fig)]['FILE']) + '_damage.png')
										self.hitisplay(10, self.foe[pl - len(self.fig)]['MASK'], str(act[2]), (0, 200, 0))
										self.foe[pl - len(self.fig)]['SPRITE'] = pygame.image.load('Sprites/frk_' + (self.foe[pl - len(self.fig)]['FILE']) + '_stand.png')
										self.foe[pl - len(self.fig)]['HP'] += act[2]
							#SELF HEALING
							elif act[2] > 0:
								self.ch_ton.play(resources.SOUND['HEAL'])
								i['HP'] += act[2]
						elif act[3] == 2:
							#REDUCE DAMAGE
							if act[2] < 0:
								if self.tatt[pl] < 2:
									self.ch_ton.play(resources.SOUND['ATTRIBUTE_LOSS'])
									self.patt[pl] += act[2]
									self.dialog([dd, self.fig[pl]['NAME'] + database.BATTLE[20] + str(act[2]) + database.BATTLE[22],1])
									self.tatt[pl] += 1
							#GROW DAMAGE
							elif act[2] > 0:
								act[2] += act[2]
								self.ton_sfx.play(resources.SOUND['ATTRIBUTE_GAIN'])
								self.dialog([dd, i['NAME'] + database.BATTLE[21] + str(act[2]) + database.BATTLE[22],1])
						elif act[3] == 3:
							#REDUCE AGILITY
							if act[2] < 0:
								self.turn = self.fig[pl]['N']
								if self.tagi[self.turn] < 2:
									self.ch_ton.play(resources.SOUND['ATTRIBUTE_LOSS'])
									self.pagi[self.turn]+=act[2]
									self.dialog([dd, self.fig[pl]['NAME'] + database.BATTLE[20] + str(act[2]) + database.BATTLE[23],1])
									self.tagi[self.turn]+=1
							#GROW AGILITY
							elif act[2] > 0:
								i['AGILITY']+=act[2]
								self.ton_sfx.play(resources.SOUND['ATTRIBUTE_GAIN'])
								self.dialog([dd, i['NAME'] + database.BATTLE[21] + str(act[2]) + database.BATTLE[23],1])
						elif act[3] == 4:
							#REDUCE STRENGHT
							if act[2] < 0:
								self.turn = self.fig[pl]['N']
								if self.tstr[self.turn]<2:
									self.ch_ton.play(resources.SOUND['ATTRIBUTE_LOSS'])
									self.pstr[self.turn] += act[2]
									self.dialog([dd, self.fig[pl]['NAME'] + database.BATTLE[20] + str(act[2]) + database.BATTLE[24],1])
									self.tstr[self.turn] += 1
							#GROW STRENGHT
							elif act[2] > 0:
								i['STRENGHT'] += act[2]
								self.ton_sfx.play(resources.SOUND['ATTRIBUTE_GAIN'])
								self.dialog([dd, i['NAME'] + database.BATTLE[21] + str(act[2]) + database.BATTLE[24],1])
						elif act[3] == 5:
							#REDUCE RESISTANCE
							if act[2] < 0:
								self.turn = self.fig[pl]['N']
								if self.tagi[self.turn] < 2:
									self.ch_ton.play(resources.SOUND['ATTRIBUTE_LOSS'])
									self.pres[self.turn] += act[2]
									self.dialog([dd, self.fig[pl]['NAME'] + database.BATTLE[20] + str(act[2]) + database.BATTLE[25],1])
									self.tres[self.turn] += 1
							#GROW RESISTANCE
							elif act[2] > 0:
								i['RESISTANCE'] += act[2]
								self.ton_sfx.play(resources.SOUND['ATTRIBUTE_GAIN'])
								self.dialog([dd, i['NAME'] + database.BATTLE[21] + str(act[2]) + database.BATTLE[25],1])
						#INPUT CONDITION
						elif act[3] == 6:	
							self.fig[pl]['HEALTH'] = act[2]
							if self.dlgfa > 0:
								if act[2] == 2: self.dialog([dd, self.fig[pl]['NAME'] + database.BATTLE[26],1])
								if act[2] == 3: self.dialog([dd, self.fig[pl]['NAME'] + database.BATTLE[27],1])
								if act[2] == 4: self.dialog([dd, self.fig[pl]['NAME'] + database.BATTLE[28],1])
								if act[2] == 5: self.dialog([dd, self.fig[pl]['NAME'] + database.BATTLE[29],1])
								if act[2] == 6: self.dialog([dd, self.fig[pl]['NAME'] +  database.BATTLE[30],1])
								if act[2] == 7: self.dialog([dd, self.fig[pl]['NAME'] + database.BATTLE[31],1])
								if act[2] == 8: self.dialog([dd, self.fig[pl]['NAME'] + database.BATTLE[32],1])
								if act[2] == 9: self.dialog([dd, self.fig[pl]['NAME'] + database.BATTLE[33],1])
								if act[2] == 10 or act[2] == 11 or act[2] == 12: self.dialog([dd, self.fig[pl]['NAME'] + database.BATTLE[34],1])
								if act[2] == 13: self.dialog([dd, self.fig[pl]['NAME'] + database.BATTLE[35],1])
								self.fig[pl]['HEALTH'] = act[2]
								if self.fig[pl]['HEALTH'] == 5: self.pagi[pl] -= 20
								act[2] == 0
						#ADD ANOMALY
						elif act[3] == 7:
							prb = round(random.randint(0,100))
							if prb > 49:
								wh = round(random.randint(0,len(act[2]) - 1))
								nw = database.FREAKS[act[2][wh]].copy()
								nw['FILE'] = act[2][wh]
								nw['SPRITE'] = pygame.image.load('Sprites/frk_' + (nw['FILE']) + '_stand.png')
								nw['MASK'] = pygame.Rect(230,180,44,85)
								nw['FIGHTING'] = True
								nw['HEALTH'] = 0
								nw['VITALITY'] = nw['HP']
								nw['DIRECTION'] = 1
								nw['FADE'] = 10
								if resources.MAP == nw['HABITAT']:
									nw['AGILITY'] += 2
									nw['HP'] += 5
								self.foe.append(nw)
								if self.dlgfa > 0:
									self.dialog([i['NAME'] + ' usou ' + act[0],1,nw['NAME'] + database.BATTLE[37],1])
							else:
								if self.dlgfa > 0:
									self.dialog([i['NAME'] + ' usou ' + act[0],1,database.BATTLE[38],1])
						#RUN AWAY
						elif act[3] == 9:
							if self.dlgfa > 0: self.dialog([i['NAME'] + ' arregou!',1])
							while i['FADE'] > 0:
								i['FADE'] -= 1
								self.run()
							i['FIGHTING'] = False
							i['HP'] = 0
						#CHARGE ATTACK
						elif act[3] == 10:
							self.ch_ton.play(resources.SOUND['CHARGE'])
							self.attackimation(act[5])
							self.turn = self.fig[pl]['N']
							self.ch_ton.play(resources.SOUND['SCREAM_' + i['FILE'].upper()])
							self.ch_sfx.play(resources.SOUND['DAMAGE_1'])
							if self.attackimation(act[5]) == False:
								act[2] -= int(act[2]/5)
								self.fig[pl]['HP'] += act[2] + self.pres[pl]
								self.hitisplay(-act[2] * 2, None, '', (0,0,0))
								self.hpl += act[2]
							else:
								self.ch_sfx.play(resources.SOUND['HIT'])
								for p in range(dmg * 3):
									self.particles.append({'TYPE': 'blood', 'X': self.aim.x, 'Y': self.aim.y, 'RADIUS': round(random.randint(3,5)), 'DIRECTION': round(random.randint(0,360)), 'SPEED': round(random.randint(2,6))})
								self.hitisplay(10, i['MASK'], str(act[2]), (200, 0, 0))
								if i['HEALTH'] != 1: i['SPRITE'] = pygame.image.load('Sprites/frk_' + (i['FILE'])+ '_stand.png')
								i['HP'] -= act[2]
								self.hits += 1
								self.tdmg += act[2]
							#COUNTER DAMAGE
							if i['HP'] <= 0:
								self.ch_ton.play(resources.SOUND['SCREAM_' + i['FILE'].upper()])
								while i['FADE'] > 0:
									i['FADE'] -= 1
									self.run()
								if i['ITEM'] != None:
									prb = round(random.randint(0,100))
									if prb > i['ITEM'][1]:
										self.inv.add(resources.PARTY[resources.FORMATION][0],i['ITEM'][0])
										self.ch_sfx.play(resources.SOUND['ITEM_GET'])
										self.notification('Adquiriu ' + database.ITEMS[i['ITEM'][0]][0],(255, 255, 255))
								i['FIGHTING'] = False
						#CHECK DEATH
						if pl < len(self.fig) and self.fig[pl]['HP'] <= 0:
							self.mnu = 1
							if self.fig[pl]['BLESS'] == 0:
								self.fig[pl]['HEALTH'] = 15
								self.ch_ton.play(resources.SOUND['INCONSCIOUS'])
							else:
								self.fig[pl]['BLESS'] -= 1
								self.fig[pl]['HP'] = database.CLASSES[self.fig[pl]['CLASS']]['VITALITY'][self.fig[pl]['LEVEL']]
						i['SPRITE'] = pygame.image.load('Sprites/frk_' + (i['FILE']).lower() + '_stand.png')
					#MISS
					else:
						i['SPRITE'] = pygame.image.load('Sprites/frk_' + (i['FILE']).lower() + '_stand.png')
						self.ch_sfx.play(resources.SOUND['MISS'])
				#TURN AROUND
				elif i['HEALTH'] == 1 and self.dlgfa > 0:
					i['SPRITE'] = pygame.image.load('Sprites/frk_' + (i['FILE']) + '_stand.png')
					i['HEALTH'] = 7
			if self.turn > -1:
				self.turn =  0
				self.mnu = 1
				for i in range(len(self.fig)):
					if self.pres[i] > database.CLASSES[self.fig[i]['CLASS']]['RESISTANCE'][self.fig[i]['LEVEL']]:
						self.pres[i] = database.CLASSES[self.fig[i]['CLASS']]['RESISTANCE'][self.fig[i]['LEVEL']]
		#OBSTACLES
		if self.obstacles == True:
			dmg = []
			self.mnu = 3
			for p in range(len(self.fig)):
				dmg.append(5)
				for a in resources.INVENTORY[self.fig[p]['N']][:-1]:
					if a[0][0] != '_':
						dmg[p] += int(database.ITEMS[a[0][0]][5])
						a[0][1] = int(a[0][1])
						a[0][1] -= 1
						if a[0][1] == 0:
							self.dialog([a[0][0] + database.BATTLE[36],1])
							a[0] = ['_','0000','_','_']
						a[0][1] = str(a[0][1])

			if self.attackimation(1) == True:
				for p in range(len(self.fig)): dmg -= int(dmg/5)
				self.hitisplay(5, i['MASK'], 'dodge', (0, 200, 0))
			else:
				for p in range(len(self.fig)): self.fig[p]['HP'] += dmg[p] + self.pres[p]
				self.hitisplay(-dmg[p] * 2, None, '', (0,0,0))
				self.ch_sfx.play(resources.SOUND['DAMAGE_1'])
				self.hpl += dmg[p]
			self.mnu = 1
		#VICTORY
		dth = 0
		for d in self.foe + self.mrc:
			if d['HP'] <= 0: dth += 1
		if dth == len(self.foe) + len(self.mrc) and self.battle == True:
			self.ch_msc.fadeout(500)
			if len(self.foe) >= 10: self.ch_ton.play(resources.SOUND['BATTLE_BOSS_WON'])
			elif len(self.foe) > 0 and self.foe[0]['TYPE'] == 'boss': self.ch_ton.play(resources.SOUND['BATTLE_BOSS_WON'])
			elif self.hpl == 0: self.ch_ton.play(resources.SOUND['BATTLE_PERFECT'])
			else: self.ch_ton.play(resources.SOUND['BATTLE_WON'])
			self.tbt += round(self.btime/10)
			xp = int(((self.hits*self.tdmg)-self.hpl+self.tbt)/len(self.fig))
			self.mnu = 600
			self.transiction(True, 210)
			self.turn = -4
			self.obstacles = False
			self.bbm = 0
			while self.mnu > 0:
				self.mnu -= 60
				self.run()
			self.wait()
			#GREENBLOOD
			btls = None
			for i in resources.PARTY[resources.FORMATION]:
				for it in ['bottle100','bottle250']:
					btls = self.inv.find(i,it)
					if btls != None and int(btls[1]) < database.ITEMS[btls[0]][5]: break
				if btls != None and int(btls[1]) < database.ITEMS[btls[0]][5]: break
			if btls != None:
				btls[1] = int(btls[1])
				gb = btls[1]
				for i in self.foe:
					gb += i['BLOOD']
				while btls[1] < gb:
					if (gb - btls[1]) > 100: btls[1] += 5
					else: btls[1] += 1
					if btls[1] >= database.ITEMS[btls[0]][5]: break
					self.run()
				btls[1] = str(btls[1])
			#PARTY XP
			for i in range(len(resources.PARTY[resources.FORMATION])):
				resources.CHARACTERS[i]['XP'] += xp
				plux = int(100/(resources.CHARACTERS[i]['NEXTLEVEL'][resources.CHARACTERS[i]['LEVEL']]/resources.CHARACTERS[i]['XP']))
			lvlup = False
			self.exvar = -1
			for i in range(len(self.fig)):
				while self.barxp[i] < plux and self.barxp[i] < 100:
					self.barxp[i] += 1
					self.run()
				#LEVEL UP
				if self.barxp[i] >= 100:
					if lvlup == False:
						self.bbg = pygame.image.load('Backgrounds/level_up.png')
						self.ch_ton.play(resources.SOUND['LEVEL_UP'],-1)
						self.transiction(False, 100, 10)
						while True:
							if self.mnu > -700: self.mnu -= 50
							if self.winbar > 100: self.winbar -= 10
							if self.mnu <= -700 and self.winbar <= 100: break
							self.run()
						lvlup = True
					self.exvar += 1
					self.barxp[i] = 0
					resources.CHARACTERS[resources.PARTY[resources.FORMATION][i]]['LEVEL'] += 1
					resources.CHARACTERS[resources.PARTY[resources.FORMATION][i]]['HP'] += resources.CHARACTERS[resources.PARTY[resources.FORMATION][i]]['VITALITY'][resources.CHARACTERS[resources.PARTY[resources.FORMATION][i]]['LEVEL']] - resources.CHARACTERS[resources.PARTY[resources.FORMATION][i]]['VITALITY'][resources.CHARACTERS[resources.PARTY[resources.FORMATION][i]]['LEVEL'] - 1]
					resources.CHARACTERS[resources.PARTY[resources.FORMATION][i]]['XP'] = 0
					self.wait()
			if lvlup == True:
				self.transiction(True, 210, 10)
				self.ch_ton.fadeout(2500)
			else: self.wait()
			self.hits = 0
			self.tdmg = 0
			self.hpl = 0
			self.tbt = 0
			self.foe = []
			self.mrc = []
			self.btime = 100
			self.turn = -1
			self.battle = False
			if self.radonoff == True: pygame.mixer.music.unpause()
			self.player[0]['PAUSE'] = 0
			self.transiction(False, 0)
		#GAME OVER
		dth = 0
		for d in self.fig:
			if d['HP'] <= 0: dth += 1
		if dth == len(self.fig):
			if self.radonoff == True: pygame.mixer.music.stop(); self.radonoff = False
			self.ch_msc.fadeout(500)
			self.ch_ton.play(resources.SOUND['BATTLE_LOST'])
			self.transiction(True, 210)
			self.obstacles = False
			self.bbm = 0
			self.turn = -5
			self.mnu = 600
			acc = 60
			while self.mnu > 0:
				self.mnu -= acc
				acc -= 2
				self.run()
			self.turn = -5
			self.wait()
			resources.load_data()
			resources.PX = 315
			resources.PY = 200
			src = None
			for i in resources.PARTY[resources.FORMATION]:
				src = self.inv.find(i,'credit_card')
				if src == None:
					src = self.inv.find(i,'wallet')
					if src != None:
						src[1] = str(int(scr[1][6:]) - 100) + scr[1][6:]
				else:
					src[1] = str(int(scr[1]) - 100)
			for i in resources.PARTY[resources.FORMATION]:
				resources.CHARACTERS[i]['HP'] = resources.CHARACTERS[i]['VITALITY'][resources.CHARACTERS[i]['LEVEL']]
				resources.CHARACTERS[i]['HEALTH'] = 0
			self.__init__()
			if resources.CHAPTER > 0: self.rendermap('hospital_0')
			self.transiction(False, 0)

	def hitisplay(self, ex, tar, dmg, col):
		self.dmgy = 200
		hitac = 8
		lgy = 1
		inf = 0
		wt = 0
		#SHAKE SCREEN
		if tar == None:
			while ex != 0:
				self.screen.fill((255, 0, 0))
				if ex > 0:
					self.displayx = ex
					self.displayy = ex
					ex = -ex
				elif ex < 0:
					self.displayx = ex
					self.displayy = ex
					ex = -ex
					ex -= 1
				self.run()
			self.displayx = 0
			self.displayy = 0
			self.run()
		#DAMAGE INFORMATION
		else:
			self.dmginfo = pygame.Surface((9 + (len(dmg) * 17),40), pygame.SRCALPHA, 32)
			self.dmginfo.convert_alpha()

			sx = tar.x
			sy = tar.y
			while wt < 10:
				tar.x = sx
				tar.y = sy
				if ex > 0:
					tar.x += ex
					tar.y += ex
					ex = -ex
				elif ex < 0:
					tar.x += ex
					tar.y += ex
					ex = -ex
					ex -= 1
				if inf == 0:
					self.dmgy -= hitac
					hitac -= 1
					lgy += 1
					if hitac == 0: inf = 1
				elif inf == 1:
					self.dmgy += hitac
					hitac += 1
					if hitac == 8: inf = 2
				elif ex == 0:
					wt += 1
				if self.dmginfo != '':
					self.dmginfo.blit(self.fnt['MININFO'].render(dmg, True, (0,0,0)), (11 - lgy, 11 - lgy))
					self.dmginfo.blit(self.fnt['MININFO'].render(dmg, True, col), (10 - lgy, 10 - lgy))
				self.run()
			tar.x = sx
			tar.y = sy
		self.run()
		self.dmginfo = ''

	def attackimation(self, wh):
		self.effttack = wh
		self.effgif = 0
		ddg = False
		counter = False
		if wh != 10:
			while self.effgif < len(resources.SPRITES['ATTACKIMATION_' + str(wh)]):
				for event in pygame.event.get():
					self.pressed = pygame.key.get_pressed()
					if self.pressed[resources.ACT[0]] and self.effgif == len(resources.SPRITES['ATTACKIMATION_' + str(wh)]):
						ddg = True
				self.run()
				self.effgif += 0.5
		else:
			while True:
				for event in pygame.event.get():
					self.pressed = pygame.key.get_pressed()
					if self.pressed[resources.ACT[0]] and self.effgif > 4.0:
						counter = True
				if counter == False: self.effgif += 0.25
				if counter == True: self.effgif -= 0.25

				if self.effgif == len(resources.SPRITES['ATTACKIMATION_' + str(wh)]): ddg = False; break
				elif self.effgif == 0.0: ddg = True; break
				self.run()

		self.effttack = None
		self.effgif = 0

		return ddg

	def rendermap(self, mp):
		if mp == 'rodoviary':
			self.map = pytmx.load_pygame('Maps/' + mp + '.tmx')
			resources.MAP = 0
		elif mp[1:8] == 'highway':
			resources.MAP = int(mp[0]) + 1
			self.map = pytmx.load_pygame('Maps/' + mp[1:11] + '.tmx')
			self.cityname = database.CITIES[resources.MAP - 1]
		else: self.map = pytmx.load_pygame('Maps/' + mp + '.tmx')
		self.room = mp
		self.cam.x = 0
		self.cam.y = 0
		self.tilmap = [[],[],[],[],[],[],[]]
		self.objects = [[0,0,self.player[0]['RECT'].y]]
		self.tilrect = [[],[],[],[],[],[]]
		self.en = []
		self.foe = []
		self.npcs = []
		self.vehicles = []
		self.portals = []
		self.signs = []
		self.tolls = []
		self.lights = []
		self.nodes = []
		self.areas = []
		self.particles = []
		self.loadingif = 0
		self.bbm = 0
		for i in self.player: i['NODES'] = []
		self.phn.mp = None

		#DRAW MAP BOUNDARIES
		self.tilrect[3].append(['WALL',pygame.Rect(-self.map.tilewidth, -self.map.tileheight,self.map.tilewidth * self.map.width,self.map.tileheight)])
		self.tilrect[3].append(['WALL',pygame.Rect(-self.map.tilewidth, (self.map.height * self.map.tileheight) + self.map.tileheight,self.map.tilewidth * self.map.width,self.map.tileheight)])
		self.tilrect[3].append(['WALL',pygame.Rect(-self.map.tilewidth, -self.map.tileheight,self.map.tilewidth,self.map.tileheight * self.map.height)])
		self.tilrect[3].append(['WALL',pygame.Rect((self.map.width * self.map.tilewidth) + self.map.tilewidth,-self.map.tileheight,self.map.tilewidth,self.map.tileheight * self.map.height)])
		#DRAW MAP
		for i in range(3):
			for a in range(2):
				self.tilmap[i].append(pygame.Surface((self.map.width * self.map.tilewidth,self.map.height * self.map.tileheight), pygame.SRCALPHA, 32))
				for x in range(0, self.map.width):
					for y in range(0, self.map.height):
						try: gid = self.map.get_tile_gid(x, y, i)
						except: gid = None
						if gid != None:
							tl = self.map.get_tile_properties_by_gid(gid)
							if tl != None:
								#TILE FRAME ANIMATION
								if tl['frames'] != []: image = self.map.get_tile_image_by_gid(tl['frames'][a].gid)
								else: image = self.map.get_tile_image_by_gid(gid)
								image.convert()
								#TILE IMAGE
								try: t = self.map.get_tile_properties(x, y, i)['TYPE'].upper()
								except: t = 'CLOTH'
								if t.startswith('BACKGROUND'):
									if len(self.tilmap[int(t[10])]) < a + 1:
										self.tilmap[int(t[10])].append(pygame.Surface((self.map.width * self.map.tilewidth,self.map.height * self.map.tileheight), pygame.SRCALPHA, 32))
									if resources.TIME[0] >= 18: fr = 1
									elif resources.TIME[0] >= 6: fr = 0
									else: fr = 1
									if tl['frames'] != []: image = self.map.get_tile_image_by_gid(tl['frames'][fr].gid).convert()
									else: image = self.map.get_tile_image_by_gid(gid).convert()
									self.tilmap[int(t[10])][a].blit(image, (x * self.map.tilewidth - self.cam.x, y * self.map.tileheight - self.cam.y))
								elif t == 'MOON':
									if len(self.tilmap[4]) < a + 1:
										self.tilmap[4].append(pygame.Surface((self.map.width * self.map.tilewidth,self.map.height * self.map.tileheight), pygame.SRCALPHA, 32))
									if resources.TIME[0] >= 18: fr = resources.DATE[4]
									elif resources.TIME[0] >= 6: fr = 0
									else: fr = resources.DATE[4]
									image = self.map.get_tile_image_by_gid(tl['frames'][fr].gid).convert()
									self.tilmap[4][a].blit(image, (x * self.map.tilewidth - self.cam.x, y * self.map.tileheight - self.cam.y))
								elif t not in ['CARRY','HOLD','HIDEON','HIDEOFF']:
									self.tilmap[i][a].blit(image, (x * self.map.tilewidth - self.cam.x, y * self.map.tileheight - self.cam.y))
								#TILRECT
								if i < 2 and a == 0:
									#MOVABLE OBJECTS
									if t in ['CARRY','HOLD']:
										self.tilrect[2].append([t,pygame.Rect(x * self.map.tilewidth, y * self.map.tileheight,self.map.tilewidth,self.map.tileheight),image])
									#WALLS
									elif t == 'WALL':
										bft = self.tilrect[3][len(self.tilrect[3]) - 1]
										if bft[1].y == (y - 1) * self.map.tileheight: bft[1].height += self.map.tileheight
										elif bft[1].height == (y - 1) * self.map.tileheight: bft[1].height += self.map.tileheight
										else: self.tilrect[3].append([t,pygame.Rect(x * self.map.tilewidth, y * self.map.tileheight,self.map.tilewidth,self.map.tileheight)])
									#NORMAL TILE
									elif t.startswith('BACKGROUND') == False and t.startswith('MOON') == False:
										self.tilrect[i].append([t,pygame.Rect(x * self.map.tilewidth, y * self.map.tileheight,self.map.tilewidth,self.map.tileheight)])
								else:
									if t.startswith('HIDE'): self.tilrect[4].append([t,pygame.Rect(x * self.map.tilewidth, y * self.map.tileheight,int(self.map.tilewidth),int(self.map.tileheight))])
								self.loading()
						#NO TILES
						elif i == 0:
							if self.tilrect[3][len(self.tilrect[3]) - 1][0] == 'WALL': self.tilrect[3][len(self.tilrect[3]) - 1][1].width += self.map.tilewidth
							else: self.tilrect[3].append(['WALL',pygame.Rect(x * self.map.tilewidth, y * self.map.tileheight,self.map.tilewidth,self.map.tileheight)])
		#OBJECTS
		for lyr in self.map.layers:
			#NPCS
			if lyr.name == 'NPC':
				for i in lyr:
					obj = self.map.get_object_by_name(i.name)
					npc = {'N': int(i.name[4:]), 'RECT': pygame.Rect(int(obj.x), int(obj.y), int(obj.width), int(obj.height)), 'TYPE': 0, 'INDEX': '000000', 'WHO': '',
					'GIF': 0.0,'BLINK': 100,'HEAD': 'BLANKD_0000','SPRITE': 'STANDD_000','MOVE': 'fixed','DIRECTION': 3,'SPEED': 0, 'PAUSE': 0,
					'JUMP': 0,'GRAVITY': -5,'TIME': 20,'FOLLOW': None,'FOLLEND': 0,'FOLLMOV': '','TALKING': False,'SWIM': None,'HOLD': None}

					add = True
					if obj.type == 'None': npc['TYPE'] = None
					elif obj.type.startswith('scene'): npc['TYPE'] = obj.type
					elif obj.type.startswith('if'):
						if resources.SCENE == int(obj.type[2:]): npc['TYPE'] = 0
						else: add = False
					else: npc['TYPE'] = int(obj.type)

					for pr in obj.properties.items():
						if pr[0] == 'INDEX':
							npc['INDEX'] = pr[1]
							npc['HEAD'] = 'BLANKD_' + pr[1][0:3] + pr[1][5]
							npc['SPRITE'] = 'STANDD_' + pr[1][3:6]
						if pr[0] == 'WHO': npc['WHO'] = pr[1]
						if pr[0] == 'DIRECTION': npc['DIRECTION'] = int(pr[1]); npc['MOVE'] = 'stand'
						if pr[0] == 'MOVE': npc['MOVE'] = pr[1]

					if add == True:
						self.npcs.append(npc)
						self.objects.append([2,int(i.name[4:]),int(obj.y)])
			#VEICHLES
			vhn = -1
			if lyr.name == 'VEHICLES':
				for i in lyr:
					obj = self.map.get_object_by_name(i.name)
					vh = database.VEHICLES['moto_' + str(obj.type)].copy()
					vhn = int(i.name[8:])
					vh['N'] = vhn
					vh['RECT'] = pygame.Rect(int(obj.x), int(obj.y), 60, 10)
					vh['INDEX'] = int(obj.type)
					vh['DIRECTION'] = 1
					for pr in obj.properties.items():
						if pr[0] == 'MOVE': vh['MOVE'] = pr[1]
						if pr[0] == 'DIRECTION': vh['DIRECTION'] = int(pr[1])
					self.vehicles.append(vh)
					self.objects.append([3,int(i.name[8:]),int(obj.y)])
			
				if self.driving > 0:
					vh = database.VEHICLES['moto_0'].copy()
					vh['N'] = vhn + 1
					vh['RECT'] = pygame.Rect(int(self.player[0]['RECT'].x), int(self.player[0]['RECT'].y), 60, 10)
					vh['INDEX'] = 0
					vh['DIRECTION'] = 1
					vh['MOVE'] = 'fixed'
					self.vehicles.append(vh)
					self.objects.append([3,vhn + 1,int(self.player[0]['RECT'].y)])
					self.driving = vhn + 2
			#PORTALS
			if lyr.name == 'PORTAL':
				for i in lyr:
					obj = self.map.get_object_by_name(i.name)
					dt = {'N': int(i.name[7:]), 'RECT': pygame.Rect(int(obj.x), int(obj.y), int(obj.width), int(obj.height)), 'TYPE': int(obj.type), 'PX': obj.properties['PX'], 'PY': obj.properties['PY'], 'MAP': None,
					'OPENING': None,'CLOSURE': None,'MUSIC': None,'MATCH': None}
					for pr in obj.properties.items():
						if pr[0] == 'TIME':
							if obj.properties['TIME'].startswith('key'):
								dt['OPENING'] = obj.properties['TIME'][0:3]
								dt['CLOSURE'] = obj.properties['TIME'][3:7]
							else:
								dt['OPENING'] = [int(obj.properties['TIME'][0:2]),int(obj.properties['TIME'][2:4])]
								dt['CLOSURE'] = [int(obj.properties['TIME'][4:6]),int(obj.properties['TIME'][6:8])]
						if pr[0] == 'MUSIC':
							dt['MUSIC'] = obj.properties['MUSIC']
						if pr[0] == 'MATCH':
							dt['MATCH'] = obj.properties['MATCH']
						if pr[0] == 'MAP':
							dt['MAP'] = obj.properties['MAP']
						if pr[0].startswith('IF'):
							if pr[0][3:6] == 'NOT':
								pass
							elif resources.CHAPTER == int(pr[0][3:5]):
								dt['MAP'] = pr[1]
							else: dt['MAP'] = obj.properties['IF NOT']
					self.portals.append(dt)
					self.objects.append([4,int(i.name[7:]),int(obj.y)])
			#SIGNS
			if lyr.name == 'SIGNS':
				for i in lyr:
					obj = self.map.get_object_by_name(i.name)
					sg = {'N': int(i.name[5:]), 'RECT': pygame.Rect(int(obj.x), int(obj.y), len(obj.type) * 10, int(obj.height)), 'TEXT': obj.type}
					for pr in obj.properties.items():
						if pr[0] == 'ICON': sg['ICON'] = pr[1]
					self.signs.append(sg)
					self.objects.append([5,int(i.name[5:]),int(obj.y)])
			#LIGHTS
			if lyr.name == 'LIGHTS':
				for i in lyr:
					obj = self.map.get_object_by_name(i.name)
					img = pygame.Surface((int(obj.width),int(obj.height)),pygame.SRCALPHA)
					if obj.type == '0':
						pygame.draw.ellipse(img, (255, 255, 255, 100), pygame.Rect(0,0,int(obj.width),int(obj.height)))
					elif obj.type == '1':
						for r in range(math.floor(obj.height/2)):
							srf = pygame.Surface((obj.width,obj.height),pygame.SRCALPHA)
							pygame.draw.circle(srf, (255, 255, 255, r), (math.floor(obj.width/2),math.floor(obj.height/2)), r)
							img.blit(srf,(0,0))
					elif obj.type == '2':
						pygame.draw.ellipse(img, (255, 208, 0, 100), pygame.Rect(0,0,int(obj.width),int(obj.height)))
					self.lights.append({'N': int(i.name[6:]), 'TYPE': obj.type, 'IMAGE': img, 'RECT': pygame.Rect(int(obj.x), int(obj.y), int(obj.width), int(obj.height))})
					self.objects.append([6,int(i.name[6:]),self.map.height * self.map.tileheight])
			#TOLLS
			if lyr.name == 'TOLLS':
				for i in lyr:
					obj = self.map.get_object_by_name(i.name)
					tl = {'N': int(i.name[5:]), 'RECT': pygame.Rect(int(obj.x), int(obj.y), int(obj.width), int(obj.height)), 'CENTER': pygame.Rect(0,0,44,16).center, 'ANGLE': int(obj.rotation), 'TIME': 0}
					self.tolls.append(tl)
					self.objects.append([7,int(i.name[5:]),int(obj.y)])
			#NODES
			if lyr.name == 'NODES':
				for i in lyr:
					obj = self.map.get_object_by_name(i.name)
					self.nodes.append({'N': int(i.name[5:]), 'TYPE': int(obj.type), 'RECT': pygame.Rect(int(obj.x), int(obj.y), int(obj.width), int(obj.height)), 'GOING': int(obj.properties['GOING'])})
					self.objects.append([7,int(i.name[5:]),int(obj.y)])
			#AREAS
			if lyr.name == 'AREAS':
				for i in lyr:
					obj = self.map.get_object_by_name(i.name)
					self.areas.append({'N': int(i.name[5:]), 'RECT': pygame.Rect(int(obj.x), int(obj.y), int(obj.width), int(obj.height))})
			self.loading()
		#ENEMIES
		for prp in self.map.properties.items():
			if prp[0] == 'ENEMIES':
				st = 0
				en = 0
				lst = []
				for i in self.map.properties['ENEMIES']:
					if i == '-': lst.append(self.map.properties['ENEMIES'][st:en]); st += en + 1
					en += 1
				for i in range(round(random.randint(3,10))):
					wh = lst[round(random.randint(0,len(lst) - 1))]
					self.en.append(database.FREAKS[wh].copy())
					self.en[i]['N'] = i
					self.en[i]['FILE'] = wh
					self.en[i]['SPRITE'] = pygame.image.load('Sprites/frk_' + (self.en[i]['FILE']) + '_stand.png')
					siz = pygame.image.load('Sprites/frk_' + self.en[i]['FILE'] + '_mini.png').get_rect()
					self.en[i]['RECT'] = pygame.Rect(self.tilrect[0][round(random.randint(0, len(self.tilrect[0])))][1].x,self.tilrect[0][round(random.randint(0, len(self.tilrect[0])))][1].y,siz.width,siz.height)
					self.en[i]['MASK'] = pygame.Rect(230,180,44,85)
					self.en[i]['DIRECTION'] = 0
					self.en[i]['FIGHTING'] = False
					self.en[i]['HEALTH'] = 0
					self.en[i]['TIME'] = 20
					self.en[i]['FADE'] = 10
					self.en[i]['EFFECT'] = 0.0
					self.en[i]['JUMP'] = 0
					if mp == self.en[i]['HABITAT']:
						self.en[i]['AGILITY'] += 2
						self.en[i]['HP'] += 5
					self.objects.append([1,i,self.en[i]['RECT'].y])
			elif prp[0] == 'SIGNAL':
				self.signal = self.map.properties['SIGNAL']
		self.loadingif = None
		print(self.tilrect[3])

	def notification(self, txt, col):
		self.nottxt = txt
		self.notcol = col
		self.notx = 0
		w = 0
		while self.notx < 180:
			self.run()
			self.notx += 20
		while w < 50:
			self.run()
			w += 1
		self.notx = 0

	def draw(self):
		for i in self.display: i.fill((0,0,0,0))
		if self.battle == True and self.turn < 0: self.hpctrl = []
		elif self.dlgfa < 500: self.hpctrl = []
		else: self.hpctrl = database.HINTS['MENUS']
		lyr2 = False
		#TILEMATION
		if self.player[0]['PAUSE'] < 2: self.tilemation += 0.1
		if self.tilemation >= 2.0: self.tilemation = 0.0
		#TILED MAP
		if self.turn != -6:
			if len(self.tilmap[3]) > 0: self.display[0].blit(self.tilmap[3][math.floor(self.tilemation)], (0, 0))
			if len(self.tilmap[4]) > 0: self.display[0].blit(self.tilmap[4][math.floor(self.tilemation)], (-math.floor(self.cam.x/5), -math.floor(self.cam.y/5)))
			if len(self.tilmap[5]) > 0: self.display[0].blit(self.tilmap[5][math.floor(self.tilemation)], (-math.floor(self.cam.x/2), -math.floor(self.cam.y/2)))
			self.display[0].blit(self.tilmap[0][math.floor(self.tilemation)], (-self.cam.x, -self.cam.y))
			self.display[0].blit(self.tilmap[1][math.floor(self.tilemation)], (-self.cam.x, -self.cam.y))
			for i in self.tilrect[2]: self.display[0].blit(i[2], (i[1].x - self.cam.x, i[1].y - self.cam.y))
		else: self.display[0].fill((250,10,10))
		'''for i in self.tilrect[4]:
			srf = pygame.Surface((20,20))
			srf.blit(self.display,(-i[1].x,-i[1].y))
			self.display[0].blit(srf,(i[1].x + 6,i[1].y + 6))'''
		#DEPTH
		dpth = 0
		for i in range(len(self.objects)):
			if i!= len(self.objects) - 1:
				if self.objects[i][2] > self.objects[i + 1][2]:
					self.objects.insert(i, self.objects[i + 1])
					del self.objects[i + 2]
		#DELETE OBJECTS
		for i in range(len(self.en)):
			if self.en[i]['HP'] <= 0: del self.en[i]; break
		for i in range(len(self.npcs)):
			if self.npcs[i]['DIRECTION'] == 0: del self.npcs[i]; break
		#OVERWORLD
		if self.battle == False:
			#OBJECTS
			for y in self.objects:
				if y[0] == 0:
					#PLAYER
					for i in self.player:
						if self.rectdebug == True: pygame.draw.rect(self.display[0], (0,0,255), pygame.Rect(i['RECT'].x - self.cam.x, i['RECT'].y - self.cam.y, i['RECT'].width, i['RECT'].height))
						self.people(i,True)
						#CONDITIONS
						if resources.CHARACTERS[resources.PARTY[resources.FORMATION][0]]['HEALTH'] > 1:
							if i['SHK'] == 0:
								pygame.draw.rect(self.display[0], (resources.COLOR[0],resources.COLOR[1],resources.COLOR[2]), pygame.Rect(i['RECT'].x - self.cam.x + 10 + i['SHK'],i['RECT'].y - self.cam.y - 40,16,13))
							else: pygame.draw.rect(self.display[0], (255,10,10), pygame.Rect(i['RECT'].x - self.cam.x + 10 + i['SHK'],i['RECT'].y - self.cam.y - 40,16,13))
							self.display[0].blit(pygame.image.load('Sprites/hl_' + str(resources.CHARACTERS[resources.PARTY[resources.FORMATION][0]]['HEALTH']) + '.png'), (i['RECT'].x - self.cam.x + 10 + i['SHK'],i['RECT'].y - self.cam.y - 40))
						#TILE COLISION
						if i['STEP'] > 0: i['STEP'] -= 1
						if self.rectdebug == True:
							for t in self.tilrect[3]:
								if t[0] == 'WALL': pygame.draw.rect(self.display[0],(255,0,0,10),pygame.Rect(t[1].x + 2 - self.cam.x,t[1].y + 2 - self.cam.y,t[1].width - 4,t[1].height - 4))
						for tl in range(2):
							for t in self.tilrect[tl]:
								if self.colide(i['RECT'],t[1]) and i['SPEED'] > 0 and self.dlgfa > 0 and i['PAUSE'] == 0:
									if self.driving == 0:
										if t[0].startswith('JUMP') and i['DIRECTION'] == int(t[0][4]) and i['GRAVITY'] == -5:
											i['GRAVITY'] = 4.5 + float(resources.CHARACTERS[resources.PARTY[resources.FORMATION][p]]['ACROBATICS']/2)
											i['STEP'] = 0
											self.ch_sfx.play(resources.SOUND['FALL'])
										elif t[0] != 'WALL' and t[0] != 'NONE'  and t[0].startswith('JUMP') == False and i['JUMP'] == 0:
											if i['STEP'] == 0 and resources.MAP > 0:
												#self.ch_stp.stop()
												self.ch_stp.play(resources.SOUND['STEP_' + t[0]])
												if i['SPEED'] > 0: i['STEP'] = math.floor(12/i['SPEED'])
											if t[0] == 'WATER':
												if i['SWIM'] == None: i['SWIM'] = 0.0
											else: i['SWIM'] = None
									elif t[0] != 'WALL' and t[0].startswith('JUMP') == False and i['JUMP'] == 0:
										if i['STEP'] == 0 and resources.MAP > 0:
											self.ch_stp.stop()
											self.ch_stp.play(resources.SOUND['STEP_VEHICLE'])
											if i['SPEED'] > 0: i['STEP'] = math.floor(12/i['SPEED'])
						y[2] = i['RECT'].y
				#ENEMIES
				if y[0] == 1:
					for i in self.en:
						if i['N'] == y[1]: self.enemy(i); y[2] = i['RECT'].y
				#NPCS
				elif y[0] == 2:
					for i in self.npcs:
						if i['N'] == y[1]: self.npc(i); y[2] = i['RECT'].y
				#VEHICLES
				elif y[0] == 3:
					for i in self.vehicles:
						if i['N'] == y[1]: self.vehicle(i); y[2] = i['RECT'].y
				#PORTALS
				elif y[0] == 4:
					for i in self.portals:
						if i['N'] == y[1]: self.portal(i); y[2] = i['RECT'].y
				#SIGNS
				elif y[0] == 5:
					for i in self.signs:
						if i['N'] == y[1]:
							if self.colide(i['RECT'], self.cam) and self.turn != -6:
								if resources.MAP != 0:
									sz = self.fnt['DEFAULT'].size(database.SIGNS[i['TEXT']])
									pygame.draw.rect(self.display[0], (250, 250, 250), pygame.Rect(i['RECT'].x - self.cam.x, i['RECT'].y - self.cam.y, math.floor(sz[0]/2) + 10, math.floor(sz[1]/2) + 10))
									self.display[1].blit(self.fnt['DEFAULT'].render(database.SIGNS[i['TEXT']], True, (0,0,0)), ((5 + i['RECT'].x - self.cam.x) * 2,(5 + i['RECT'].y - self.cam.y) * 2))
								else: self.display[1].blit(self.fnt['DEFAULT'].render(i['TEXT'], True, (250,250,250)), ((i['RECT'].x - self.cam.x - math.floor(self.cam.x/5)) * 2,(i['RECT'].y - self.cam.y - math.floor(self.cam.y/5)) * 2))
							y[2] = i['RECT'].y
				#TOLLS
				elif y[0] == 7:
					for i in self.tolls:
						if i['N'] == y[1]:
							srf = pygame.Surface((44,44), pygame.SRCALPHA)
							trs = pygame.transform.rotate(pygame.image.load('Sprites/toll.png'),i['ANGLE'] + 90)
							#i['CENTER'] = trs.get_rect(center = i['CENTER'].center)
							srf.blit(trs,(0,0))
							self.display[0].blit(srf,(i['RECT'].x - self.cam.x,i['RECT'].y - self.cam.y))
							if i['TIME'] > 0: i['TIME'] -= 1
							if self.colide(self.player[0]['RECT'],i['RECT']):
								if i['TIME'] == 0:
									if resources.MONEY >= 10:
										self.ch_sfx.play(resources.SOUND['BUY'])
										resources.MONEY -= 10
										i['TIME'] = 180
										print(resources.MONEY)
									elif self.facing(self.player[0],i['RECT']) == 2:
										self.player[0]['SPEED'] = 0
							y[2] = i['RECT'].y
			#NODES DEBUG
			if self.rectdebug == True:
				for i in self.nodes: pygame.draw.rect(self.display[0], (250,250,10),pygame.Rect(i['RECT'].x - self.cam.x, i['RECT'].y - self.cam.y, i['RECT'].width, i['RECT'].height))
			#OVER TILES & CLOUDS
			if resources.MAP > 0:
				self.display[0].blit(self.tilmap[2][math.floor(self.tilemation)], (-self.cam.x, -self.cam.y))
			else:
				self.bbm += 0.2
				if math.floor(self.bbm) > (self.map.width * self.map.tilewidth): self.bbm = 0.0
				self.display[0].blit(self.tilmap[2][math.floor(self.tilemation)], (math.floor(self.bbm) - self.cam.x, -self.cam.y))
				self.display[0].blit(self.tilmap[2][math.floor(self.tilemation)], (math.floor(self.bbm) - (self.map.width * self.map.tilewidth) - self.cam.x, -self.cam.y))
			'''for t in self.tilrect[4 + math.floor(self.tilemation)]:
				if self.colide(t[1],self.cam): self.display[0].blit(t[2], (t[1].x - self.cam.x, t[1].y - self.cam.y))'''
			#DAYTIME & WEATHER
			if resources.TIME[0] >= 18: tim = 100
			elif resources.TIME[0] >= 6: tim = 0
			else: tim = 100
			srf = pygame.Surface((self.displayzw,self.displayzh))
			srf.set_alpha(tim)
			srf.fill((0, 58, 160))
			if self.map.properties['INTERIOR'] == '0': self.display[0].blit(srf, (0,0))
			if len(self.tilmap[6]) > 0: self.display[0].blit(self.tilmap[6][math.floor(self.tilemation)], (0, 0))
			#LIGHTS
			for y in self.objects:
				if y[0] == 6:
					for i in self.lights:
						if i['N'] == y[1]:
							if self.colide(i['RECT'], self.cam):
								self.display[0].blit(i['IMAGE'], (i['RECT'].x - self.cam.x,i['RECT'].y - self.cam.y))
			#RAIN
			if self.map.properties['INTERIOR'] == '0' and resources.WEATHER == 1 and resources.MAP > 0:
				if len(self.particles) < 50:
					for i in range(5):
						self.particles.append({'TYPE': 'raindrop', 'X': round(random.randint(0,self.cam.width + int(self.cam.width/4))), 'Y': -int(self.cam.height/2),
							'RADIUS': 2, 'DIRECTION': 90, 'SPEED': 15, 'TIME': round(random.randint(10,60)), 'GIF': 0})
						for p in range(len(self.particles)):
							if self.particles[p]['TYPE'] == 'raindrop' and self.particles[p]['GIF'] > 8:
								del self.particles[p]; break

				if len(self.particles) > 0:
					for p in self.particles:
						if p['TYPE'] == 'raindrop':
							rd = False
							if p['TIME'] <= 0:
								rd = True
								for i in self.areas:
									if self.colide(i['RECT'],pygame.Rect(p['X'],p['Y'],p['RADIUS'],p['RADIUS'])):
										rd = False
										break
							if rd == False:
								p['TIME'] -= 1
								p['X'] += int(math.cos(p['DIRECTION']) * p['SPEED'])
								p['Y'] += int(math.sin(p['DIRECTION']) * p['SPEED'])
								img = pygame.Surface((p['RADIUS'],p['RADIUS']))
								img.fill((0, 148, 255))
								img.set_alpha(120)
								self.display[0].blit(img, (p['X'],p['Y']))
								if p['TIME'] == 0:
									p['X'] = p['X'] + self.cam.x
									p['Y'] = p['Y'] + self.cam.y
							elif p['GIF'] <= 8:
								self.display[0].blit(pygame.image.load('Sprites/raindrop_' + str(p['GIF']) + '.png'), (p['X'] - self.cam.x + 4,p['Y'] -self.cam.y + 6))
								p['GIF'] += 1
			#HIDE PLACES
			if self.tilhide == False and self.tilalpha > 0: self.tilalpha -= 20
			if self.tilhide == True and self.tilalpha < 255: self.tilalpha += 20
			if self.tilalpha < 0: self.tilalpha = 0
			if self.tilalpha > 255: self.tilalpha = 255
			al = 255 - self.tilalpha
			for i in self.tilrect[4]:
				srf = pygame.Surface((i[1].width,i[1].height))
				if i[0].endswith('ON'): srf.set_alpha(al); srf.fill((0,0,0)); self.display[0].blit(srf, (i[1].x - self.cam.x,i[1].y - self.cam.y))
				if i[0].endswith('OFF'): srf.set_alpha(self.tilalpha); srf.fill((0,0,0)); self.display[0].blit(srf, (i[1].x - self.cam.x,i[1].y - self.cam.y))
			#MINI MAP
			if resources.MINIMAP == True:
				try:
					xx = 100 + ((200/self.phn.mp.get_height()) * self.player[0]['RECT'].x * self.phn.mp.get_width()/(self.map.width * self.map.tilewidth))
					yy = 100 + ((200/self.phn.mp.get_height()) * self.player[0]['RECT'].y * self.phn.mp.get_height()/(self.map.height * self.map.tileheight))
					pygame.draw.rect(self.display[0], (0, 0, 0), pygame.Rect(0,self.displayzh - (106 * int(self.displayzh/400)),106 * int(self.displayzw/600),106 * int(self.displayzh/400)))
					self.display[0].blit(self.phn.map(True, self.map, self.tilrect, self.player[0], self.en, self.signs, xx, yy, 200, self.signal), (3 * int(self.displayzh/400),self.displayzh - (103 * int(self.displayzh/400))))
				except: pass
			#DRIVING BARS
			if self.driving > 0:
				pygame.draw.rect(self.display[0], (10,10,10), pygame.Rect(20,20,100,20))
				if resources.GAS >= 1: pygame.draw.rect(self.display[0], (255,155,66), pygame.Rect(20,20,int(100/(self.vehicles[self.driving - 1]['CAPACITY']/round(resources.GAS))),20))
				pygame.draw.rect(self.display[0], (10,10,10), pygame.Rect(20,42,100,20))
				if self.player[0]['SPEED'] > 0: pygame.draw.rect(self.display[0], (0,255,0), pygame.Rect(20,42,int(100/(20/self.player[0]['SPEED'])),20))
				self.hpctrl = database.HINTS['VEHICLE_CONTROLS']
			#BLACK BARS
			if self.winbar > 0:
				#MYSTERIOUS FREAK
				if self.turn == -6:
					if self.winbar < 175:
						pygame.draw.rect(self.display[0], (0, 0, 0), pygame.Rect(0,0,self.displayzw,self.winbar))
						pygame.draw.rect(self.display[0], (0, 0, 0), pygame.Rect(0,self.displayzh,self.displayzw,-self.winbar))
					else:
						pygame.draw.rect(self.display[0], (0, 0, 0), pygame.Rect(0,0,600,175))
						pygame.draw.rect(self.display[0], (0, 0, 0), pygame.Rect(0,400,600,-165))
						pygame.draw.rect(self.display[0], (0, 0, 0), pygame.Rect(0,175,-410 + (self.winbar * 3),60))
						pygame.draw.rect(self.display[0], (0, 0, 0), pygame.Rect(280,0,320,self.winbar))
						pygame.draw.rect(self.display[0], (0, 0, 0), pygame.Rect(280,400,320,-self.winbar))
						self.display[0].blit(pygame.image.load('Sprites/aim_mysterious.png'), (-410 + (self.winbar * 3), 175))
						self.display[0].blit(self.fnt['MININFO'].render(self.cityname, True, (250,250,250)), (320, 200))
				#REGULAR BARS
				else:
					pygame.draw.rect(self.display[0], (0, 0, 0), pygame.Rect(0,0,self.displayzw,self.winbar))
					pygame.draw.rect(self.display[0], (0, 0, 0), pygame.Rect(0,self.displayzh,self.displayzw,-self.winbar))
			#RADIOPLAY
			if self.radonoff == True:
				rdsrf = pygame.Surface((360,50))
				rdsrf.fill((255, 0, 135))
				if self.msc < 0:
					ttsz = math.floor(self.fnt['DEFAULT'].size('?????')[0]/2)
					rdsrf.blit(self.fnt['DEFAULT'].render('?????', True, (0, 0, 0)), (-self.rdscroll * 2, 5 * 2))
				else:
					ttsz = math.floor(self.fnt['DEFAULT'].size(resources.RADIO[str(math.floor(self.fm/20))][self.msc][:-4])[0]/2)
					rdsrf.blit(self.fnt['DEFAULT'].render(resources.RADIO[str(math.floor(self.fm/20))][self.msc][:-4], True, (0, 0, 0)), (-self.rdscroll * 2, 5 * 2))
				self.display[1].blit(rdsrf, (0,0))
				self.rdscroll += 1
				if self.rdscroll > ttsz:
					self.rdscroll = -180
				lyr2 = True
				if pygame.mixer.music.get_busy() == False and self.msc > -2:
					self.msc += 1
					if self.msc > len(resources.RADIO[str(round(self.fm/20))]) - 1: self.msc = 0
					if resources.RADIO[str(round(self.fm/20))] != []:
						pygame.mixer.music.load('Songs/FM_' + str(round(self.fm/20)) + '/' + resources.RADIO[str(round(self.fm/20))][self.msc])
						pygame.mixer.music.play()
			#CITY NAME
			if self.cityname != '' and self.winbar >= 50 and self.turn != -6:
				self.display[0].blit(self.fnt['MONOTYPE'].render(self.cityname, True, (250,250,250)), (420, 360))
			#PORTALGO
			if self.portalgo != {}:
				if self.rectdebug == True: pygame.draw.rect(self.display[0], (255,0,0), pygame.Rect(self.portalgo[0]['RECT'].x, self.portalgo[0]['RECT'].y, self.portalgo[0]['RECT'].width, self.portalgo[0]['RECT'].height))
				if self.portalgo[0]['RECT'].width == 24: self.display[0].blit(pygame.image.load('Sprites/door_01.png'), (self.portalgo[0]['RECT'].x, self.portalgo[0]['RECT'].y))
				if self.portalgo[0]['RECT'].width == 48: self.display[0].blit(pygame.image.load('Sprites/door_11.png'), (self.portalgo[0]['RECT'].x, self.portalgo[0]['RECT'].y))
				self.portalgo[1]['RECT'].x = self.portalgo[0]['RECT'].x + self.cam.x
				self.portalgo[1]['RECT'].y = self.portalgo[0]['RECT'].y + self.cam.y + 20
				self.people(self.portalgo[1],True)
				for i in self.portals:
					if self.portalgo[0]['MATCH'] != None and i['MATCH'] == self.portalgo[0]['MATCH']:
						self.cam.x += int((i['RECT'].x  - self.cam.x - self.displayzw/2)/15)
						self.cam.y += int((i['RECT'].y  - self.cam.y - self.displayzh/2)/15)
						chk = 0
						if i['RECT'].x - self.cam.x < self.portalgo[0]['RECT'].x:
							self.portalgo[0]['RECT'].x -= 10
							if i['RECT'].x - self.cam.x >= self.portalgo[0]['RECT'].x and chk == 0: chk += 1
						elif i['RECT'].x - self.cam.x > self.portalgo[0]['RECT'].x and chk == 0:
							self.portalgo[0]['RECT'].x += 10
							if i['RECT'].x - self.cam.x <= self.portalgo[0]['RECT'].x and chk == 0: chk += 1
						elif chk == 0: chk += 1
						if i['RECT'].y - self.cam.y < self.portalgo[0]['RECT'].y:
							self.portalgo[0]['RECT'].y -= 10
							if i['RECT'].y - self.cam.y >= self.portalgo[0]['RECT'].y and chk == 1: chk += 1
						elif i['RECT'].y - self.cam.y > self.portalgo[0]['RECT'].y and chk != 2:
							self.portalgo[0]['RECT'].y += 10
							if i['RECT'].y - self.cam.y <= self.portalgo[0]['RECT'].y and chk == 1: chk += 1
						elif chk == 1: chk += 1

						if chk == 2: self.portalgo[0]['MATCH'] = None
						#if self.colide(self.portalgo['RECT'],i['RECT']):
						#	self.portalgo['MATCH'] = None
		#HEALTH DAMAGE
		u = 0
		for i in resources.PARTY[resources.FORMATION]:
			if resources.CHARACTERS[i]['HEALTH'] in [4,5,6,7,16,17,18,19,20,21] and self.dlgfa > 0:
				self.player[u]['DMGTIM'] -= 1
				if self.player[u]['DMGTIM'] == 0:
					self.player[u]['DMGTIM'] = 100
					self.player[u]['SHK'] = 3
					resources.CHARACTERS[i]['HP'] -= 1
					if resources.CHARACTERS[i]['HEALTH'] == 17:
						chc = round(random.randint(0,100))
						if chc > 70: resources.CHARACTERS[i]['HEALTH'] = 0
					'''dth = 0
					for d in self.fig:
						if d['HP'] <= 0: dth += 1
					if dth == len(self.fig):'''
					if resources.CHARACTERS[i]['HP'] <= 0:
						resources.CHARACTERS[i]['HEALTH'] = 0
						if self.radonoff == True: pygame.mixer.music.unpause(); self.radonoff = False
						self.ch_msc.fadeout(500)
						self.ch_ton.play(resources.SOUND['BATTLE_LOST'])
						self.transiction(True, 210)
						self.battle = True
						self.turn = -5
						self.mnu = 600
						acc = 60
						while self.mnu > 0:
							self.mnu -= acc
							acc -= 2
							self.run()
						self.turn = -5
						self.wait()
						resources.load_data()
						resources.PX = 315
						resources.PY = 200
						resources.MONEY -= 100 * len(resources.PARTY[resources.FORMATION])
						for w in resources.PARTY[resources.FORMATION]:
							resources.CHARACTERS[w]['HP'] = resources.CHARACTERS[w]['VITALITY'][resources.CHARACTERS[w]['LEVEL']]
							resources.CHARACTERS[w]['HEALTH'] = 0
						self.__init__()
						self.rendermap('hospital_1')
						self.transiction(False, 0)

					self.ch_ton.play(resources.SOUND['DAMAGE_1'])
				if self.player[u]['SHK'] > 0: self.player[u]['SHK'] = -self.player[u]['SHK']
				elif self.player[u]['SHK'] < 0: self.player[u]['SHK'] = -self.player[u]['SHK'] - 1
			u += 1
		#BATTLE
		if self.battle == True:
			#BACKGROUND
			if self.turn == -4:
				self.display[0].blit(self.bbg, (self.bbm, 0))
				self.display[0].blit(self.bbg, (self.bbm - 600, 0))
				self.bbm += 5
				if self.bbm > 600: self.bbm = 0
			elif self.bbg != '':
				self.display[0].blit(self.bbg, (self.bbm, 0))
				if self.obstacles == True:
					self.display[0].blit(self.bbg, (self.bbm - 600, 0))
					self.bbm += 5
					if self.bbm > 600: self.bbm = 0
			#FOES
			foelst = []
			maxhgt = 0
			count = 0
			oldlst = self.foe + self.mrc
			oldsiz = len(oldlst)
			while len(foelst) < oldsiz:
				count = 0
				maxhgt = 0
				for i in oldlst:
					if float(i['HEIGHT'].replace(',','.')) > maxhgt:
						maxhgt = count
					count += 1
				foelst.append(oldlst[maxhgt])
				del oldlst[maxhgt]
			count = 0
			for i in foelst[::-1]:
				if count == 5: break
				if i['FADE'] > 0 and i['HEALTH'] != 9:
					i['FIGHTING'] = True
					if i['MASK'].x < 600:
						if self.mnu == 2 and self.equip[self.turn] < 4 and i['HEALTH'] != 1:
							if i['DIRECTION'] == 1: i['MASK'].x += i['AGILITY']
							if i['DIRECTION'] == 5: i['MASK'].x -= i['AGILITY']

							if i['MASK'].x < 100: i['DIRECTION'] = 1
							if i['MASK'].x > 500: i['DIRECTION'] = 5
						if i['FADE'] < 10: i['SPRITE'].blit(pygame.image.load('Sprites/eff_death_' + str(i['FADE']) + '.png'), (0,0), special_flags=pygame.BLEND_SUB)
						self.display[0].blit(i['SPRITE'], (i['MASK'].x, i['MASK'].y))

						if i['HEALTH'] > 2:
							self.display[0].blit(resources.SPRITES['EFFECT_' + str(i['HEALTH'])][math.floor(i['EFFECT'])], (i['MASK'].x + 5, i['MASK'].y - 10))
							i['EFFECT'] += 0.5
							if i['EFFECT'] >= len(resources.SPRITES['EFFECT_' + str(i['HEALTH'])]): i['EFFECT'] = 0.0
						count += 1
					else: i['MASK'].x -= i['AGILITY']
			#SKIP PLAYER & BLINDNESS
			if self.mnu < 3 and self.turn >= 0 and self.turn < len(self.fig):
				print('pulou o turno' + str(self.turn))
				if self.fig[self.turn]['HP'] <= 0: self.turn += 1
				if self.fig[self.turn]['HEALTH'] in [8,13,14,15]: self.turn += 1
				if self.fig[self.turn]['HEALTH'] == 12: self.display[0].fill((0,0,0))
				if self.turn >= len(self.fig): self.fight()
			#BLACK BARS
			pygame.draw.rect(self.display[0], (0, 0, 0), pygame.Rect(0,0,self.displayzw,self.winbar))
			pygame.draw.rect(self.display[0], (0, 0, 0), pygame.Rect(0,self.displayzh,self.displayzw,-self.winbar))
			#ENEMIES COUNT
			if self.winbar <= 100 and self.turn != -4:
				ce = 0
				if len(self.mrc) == 0:
					for i in self.foe:
						if i['HP'] > 0: ce += 1
					self.display[0].blit(self.fnt['MININFO'].render(str(ce) + '/' + str(len(self.foe)), True, (255,255,255)), (500, -70 + self.winbar))
				else:
					for i in self.foe:
						if i['HP'] > 0: ce += 1
					self.display[0].blit(self.fnt['MININFO'].render(str(ce) + '/' + str(len(self.foe)), True, (255,255,255)), (500, -85 + self.winbar))
					ce = 0
					for i in self.mrc:
						if i['HP'] > 0: ce += 1
					self.display[0].blit(self.fnt['MININFO'].render(str(ce) + '/' + str(len(self.mrc)), True, (255,255,255)), (500, -50 + self.winbar))
				#PLAYER BARS
				p = 0
				low = False
				while p < len(resources.PARTY[resources.FORMATION]):
					#NAME
					ctr = resources.PARTY[resources.FORMATION][p]
					if p == self.turn:
						pygame.draw.rect(self.display[0], (resources.COLOR[0],resources.COLOR[1],resources.COLOR[2]), pygame.Rect(p * 120, self.winbar - 100,120,100))
						self.display[0].blit(self.fnt['MININFO'].render(resources.CHARACTERS[ctr]['NAME'].lower(), True, (0,0,0)), (10 + p * 120, -90 + self.winbar))
					else: 
						self.display[0].blit(self.fnt['MININFO'].render(resources.CHARACTERS[ctr]['NAME'].lower(), True, (resources.COLOR[0],resources.COLOR[1],resources.COLOR[2])), (10 + p * 120, -90 + self.winbar))
					#VITALITY GRAY
					pygame.draw.rect(self.display[0], (10, 10, 10), pygame.Rect(10 + p * 120, -60 + self.winbar,100,20))
					if resources.CHARACTERS[ctr]['HP'] > 0:
						minush = int(98/(database.CLASSES[resources.CHARACTERS[ctr]['CLASS']]['VITALITY'][resources.CHARACTERS[ctr]['LEVEL']]/resources.CHARACTERS[ctr]['HP']))
					else: minush = 0
					if self.barhp[p] > minush:
						self.ch_sfx.play(resources.SOUND['HP_LOSS'])
						self.barhp[p] -= 1
					pygame.draw.rect(self.display[0], (50, 50, 50), pygame.Rect(11 + p * 120, -59 + self.winbar,98,18))
					if low == True:
						if self.ch_ton.get_busy() == False: self.ch_ton.play(resources.SOUND['HP_LOW'])
					if self.barhp[p] > 0: pygame.draw.rect(self.display[0], (255,255,0), pygame.Rect(11 + p * 120, -59 + self.winbar,self.barhp[p],18))
					#LIFE BAR
					if self.equip[p] == 6 and self.turn > p: hpcol = (100, 100, 100)
					elif resources.CHARACTERS[ctr]['HP'] > database.CLASSES[resources.CHARACTERS[ctr]['CLASS']]['VITALITY'][resources.CHARACTERS[ctr]['LEVEL']]/5: hpcol = (0, 255, 0)
					elif resources.CHARACTERS[ctr]['HP'] > 0:
						hpcol = (255, 0, 0)
						low = True
					else: hpcol = (255, 0, 0)
					if resources.CHARACTERS[ctr]['HP'] > 0:
						pygame.draw.rect(self.display[0], hpcol, pygame.Rect(11 + p * 120, -59 + self.winbar,int(98/(database.CLASSES[resources.CHARACTERS[ctr]['CLASS']]['VITALITY'][resources.CHARACTERS[ctr]['LEVEL']]/resources.CHARACTERS[ctr]['HP'])),18))
					#CONDITION ICON
					if resources.CHARACTERS[ctr]['HEALTH'] > 1:
						self.display[0].blit(pygame.image.load('Sprites/hl_' + str(resources.CHARACTERS[ctr]['HEALTH']) + '.png'), (14 + p * 120, -56 + self.winbar))
					#AMMO BAR
					if self.equip[p] < 4:
						if int(resources.INVENTORY[ctr][4][self.equip[p] + 1][1]) > 0:
							try: minush = int(98/(database.ITEMS[resources.INVENTORY[ctr][4][self.equip[p] + 1][0]][5]['CAPACITY']/int(resources.INVENTORY[ctr][4][self.equip[p] + 1][1])))
							except: minush = 0
						else: minush = 0
						if self.barpp[p][self.equip[p]] > minush:
							self.barpp[p][self.equip[p]] -= 1
						pygame.draw.rect(self.display[0], (10, 10, 10), pygame.Rect(10 + p * 120, -30 + self.winbar,100,20))
						pygame.draw.rect(self.display[0], (50, 50, 50), pygame.Rect(11 + p * 120, -29 + self.winbar,98,18))
						if self.barpp[p][self.equip[p]] > 0:
							pygame.draw.rect(self.display[0], (0, 100, 255), pygame.Rect(11 + p * 120, -29 + self.winbar,self.barpp[p][self.equip[p]],18))
					p += 1
				if self.turn < len(resources.PARTY[resources.FORMATION]) and self.turn >= 0:
					#TIME BAR:
					if self.btime > 0:
						pygame.draw.rect(self.display[0], (resources.COLOR[0],resources.COLOR[1],resources.COLOR[2]), pygame.Rect(0,402 - self.winbar,int(600/(100/self.btime)),10))
					if ce > 0 and self.mnu < 3 and self.turn < len(self.fig): self.btime -= 0.5
					if self.btime == 0:
						self.turn = len(self.fig)
						self.mnu = 1
						self.fight()
					#OPTIONS
					if self.mnu == 1:
						x = 0
						for i in resources.INVENTORY[resources.PARTY[resources.FORMATION][self.turn]][4][1:]:
							if self.equip[self.turn] == x: pygame.draw.rect(self.display[0], (resources.COLOR[0], resources.COLOR[1], resources.COLOR[2]), pygame.Rect(118 + x * 35,338,32,32))
							else: pygame.draw.rect(self.display[0], (255,255,255), pygame.Rect(118 + x * 35,338,32,32))
							pygame.draw.rect(self.display[0], (0, 0, 0), pygame.Rect(120 + x * 35,340,28,28))
							if resources.INVENTORY[resources.PARTY[resources.FORMATION][self.turn]][4][x + 1][0] != '_':
								self.display[0].blit(pygame.image.load('Sprites/Items/it_' + resources.INVENTORY[resources.PARTY[resources.FORMATION][self.turn]][4][x + 1][0] + '.png'), (120 + x * 35, 440 - self.winbar))
							x += 1
						if self.equip[self.turn] == 4:
							pygame.draw.rect(self.display[0], (resources.COLOR[0], resources.COLOR[1], resources.COLOR[2]), pygame.Rect(304,438 - self.winbar,30,30))
							self.hpctrl = database.HINTS['BATTLE_TACTICS']
						else: pygame.draw.rect(self.display[0], (255, 255, 255), pygame.Rect(304,438 - self.winbar,30,30))
						self.display[0].blit(pygame.image.load('Sprites/e_tactical.png'), (304, 438 - self.winbar))
						if self.equip[self.turn] == 5:
							pygame.draw.rect(self.display[0], (resources.COLOR[0], resources.COLOR[1], resources.COLOR[2]), pygame.Rect(339,438 - self.winbar,30,30))
							self.hpctrl = database.HINTS['BATTLE_DIALOG']
						else: pygame.draw.rect(self.display[0], (255, 255, 255), pygame.Rect(339,438 - self.winbar,30,30))
						self.display[0].blit(pygame.image.load('Sprites/e_talk.png'), (339, 438 - self.winbar))
						if self.equip[self.turn] == 6:
							pygame.draw.rect(self.display[0], (resources.COLOR[0], resources.COLOR[1], resources.COLOR[2]), pygame.Rect(374,438 - self.winbar,30,30))
							self.hpctrl = database.HINTS['BATTLE_GUARD']
						else: pygame.draw.rect(self.display[0], (255, 255, 255), pygame.Rect(374,438 - self.winbar,30,30))
						self.display[0].blit(pygame.image.load('Sprites/e_guard.png'), (374, 438 - self.winbar))
						if self.equip[self.turn] == 7:
							pygame.draw.rect(self.display[0], (resources.COLOR[0], resources.COLOR[1], resources.COLOR[2]), pygame.Rect(409,438 - self.winbar,30,30))
							self.hpctrl = database.HINTS['BATTLE_RUN']
						else: pygame.draw.rect(self.display[0], (255, 255, 255), pygame.Rect(409,438 - self.winbar,30,30))
						self.display[0].blit(pygame.image.load('Sprites/e_run.png'), (409, 438 - self.winbar))
						self.display[0].blit(pygame.image.load('Sprites/e_invphn.png'), (442, 438 - self.winbar))
					#AIM BAR
					elif self.mnu == 2:
						if self.equip[self.turn] < 4:
							if resources.CHARACTERS[resources.PARTY[resources.FORMATION][self.turn]]['HEALTH'] == 9:
								prb = random.randint(0,10)
								if prb > 5: self.aim.x += round(random.randint(30,60))
								if prb < 5: self.aim.x -= round(random.randint(30,60))
							else: self.aim.x += 20 - self.pagi[self.turn]
							if self.aim.x > 500 - self.patt[self.turn]:
								self.aim.x = 100 + self.patt[self.turn]
							chk = False
							for i in resources.INVENTORY[resources.PARTY[resources.FORMATION][self.turn]][4][self.equip[self.turn] + 1][1:]:
								if isinstance(i,str) and i.startswith('aim') == True: chk = True; break
							if chk == True:
								self.display[0].blit(pygame.image.load('Sprites/aim_' + str(database.ITEMS[i][5]) + '.png'), (self.aim.x - 15, self.aim.y))
							else:
								self.display[0].blit(pygame.image.load('Sprites/aim_0.png'), (self.aim.x-15, self.aim.y))
							#self.display[0].blit(pygame.image.load('Sprites/' + resources.INVENTORY[resources.PARTY[resources.FORMATION][self.turn]][4][self.equip[self.turn] + 1][0] + '.png'), (150 + int(self.aim.x/2), 255))
							self.hpctrl = database.HINTS['BATTLE_SHOT']
						#TACTICS
						elif self.equip[self.turn] == 4:
							x = 0
							for i in resources.TACTICAL:
								if self.opt == x: pygame.draw.rect(self.display[0], (255, 0, 0), pygame.Rect(118 + x * 35,338,32,32))
								else: pygame.draw.rect(self.display[0], (255, 255, 255), pygame.Rect(118 + x * 35,338,32,32))
								pygame.draw.rect(self.display[0], (0, 0, 0), pygame.Rect(120 + x * 35,340,28,28))
								x += 1
			#PARTICLES
			if len(self.particles) > 0:
				for p in range(len(self.particles)):
					if self.particles[p]['TYPE'] == 'blood' and self.particles[p]['RADIUS'] <= 0.0:
						del self.particles[p]; break
				for p in self.particles:
					if p['TYPE'] == 'blood':
						p['X'] += int(math.cos(p['DIRECTION']) * p['SPEED'])
						p['Y'] += int(math.sin(p['DIRECTION']) * p['SPEED'])
						pygame.draw.circle(self.display[0], p['COLOR'], (p['X'],p['Y']), math.ceil(p['RADIUS']))
						p['RADIUS'] -= 0.25
						if p['RADIUS'] < 0.0: p['RADIUS'] = 0.0
			#INFOHIT
			if self.dmginfo != '':
				self.display[0].blit(self.dmginfo, (self.aim.x, self.dmgy))
			#ATTACKIMATION
			if self.effttack != None:
				srf = pygame.Surface((self.displayzw,self.displayzh))
				srf.set_alpha(100)
				srf.fill((0, 0, 0))
				self.display[0].blit(srf, (0,0))
				self.display[0].blit(resources.SPRITES['ATTACKIMATION_' + str(self.effttack)][math.floor(self.effgif)], (200,200))
			#WIN SCREEN
			if self.winbar >= 100:
				if self.turn == -4:
					#LABEL
					if self.hpl < 0: self.display[0].blit(self.fnt['MININFO'].render(database.BATTLE[6], True, (255,255,255)), (130 + self.mnu, 70))
					else: self.display[0].blit(self.fnt['MININFO'].render(database.BATTLE[7], True, (255,255,255)), (130 + self.mnu, 70))
					#GREENBLOOD
					btls = None
					for i in resources.PARTY[resources.FORMATION]:
						for it in ['bottle100','bottle250']:
							btls = self.inv.find(i,it)
							if btls != None and int(btls[1]) < database.ITEMS[btls[0]][5]: break
						if btls != None and int(btls[1]) < database.ITEMS[btls[0]][5]: break
					if btls != None:
						if int(btls[1]) > 0 and int(200/(database.ITEMS[btls[0]][5]/int(btls[1]))) >= 1:
							pygame.draw.rect(self.display[0], (0, 255, 100), pygame.Rect(460 + self.mnu,300 - int(200/(database.ITEMS[btls[0]][5]/int(btls[1]))),30,int(200/(database.ITEMS[btls[0]][5]/int(btls[1])))))
							if int(btls[1]) < 90:
								pygame.draw.ellipse(self.display[0], (32, 219, 166), pygame.Rect(460 + self.mnu,291 - int(200/(database.ITEMS[btls[0]][5]/int(btls[1]))),30,13))
							pygame.draw.rect(self.display[0], (255, 255, 255), pygame.Rect(500 + self.mnu,280 - int(200/(database.ITEMS[btls[0]][5]/int(btls[1]))),50,20))
							self.display[1].blit(self.fnt['DEFAULT'].render(str(btls[1]) + 'ml', True, (0,0,0)), ((505 + self.mnu) * 2, (285 - int(200/(database.ITEMS[btls[0]][5]/int(btls[1])))) * 2))
						self.display[0].blit(pygame.image.load('Sprites/gbbar.png'), (460 + self.mnu, 100))
					#PARTY XP
					for i in range(len(resources.PARTY[resources.FORMATION])):
						if self.mnu > 0: mvx = self.mnu
						else: mvx = 0
						self.display[0].blit(pygame.image.load('Sprites/who_' + str(resources.PARTY[resources.FORMATION][i]) + '.png'), (100 + mvx, 120 + i * 30))
						pygame.draw.rect(self.display[0], (50, 50, 50), pygame.Rect(130 + mvx,120 + i * 30,100,20))
						if self.barxp[i] > 0: pygame.draw.rect(self.display[0], (0, 255, 100), pygame.Rect(130 + mvx,120 + i * 30,self.barxp[i],20))
					#LEVEL UP
					ch = resources.CHARACTERS[resources.PARTY[resources.FORMATION][self.exvar]]
					if ch['LEVEL'] > 0:
						self.display[0].blit(self.fnt['MININFO'].render(ch['NAME'].lower(), True, (255,255,255)), (800 + self.mnu, 30))
						self.display[1].blit(self.fnt['DEFAULT'].render(database.BATTLE[14] + str(ch['LEVEL']) + ' !', True, (255,255,255)), ((800 + self.mnu) * 2, 140))
						#self.display[1].blit(self.fnt['DEFAULT'].render(database.BATTLE[39] + ' +' + str(ch['STRENGHT'][ch['LEVEL']] - ch['STRENGHT'][ch['LEVEL'] - 1]), True, (255,255,255)), ((1000 + self.mnu) * 2, 260))
						pygame.draw.rect(self.display[0], (50, 50, 50), pygame.Rect(1000 + self.mnu,120,100,15))
						pygame.draw.rect(self.display[0], (255, 255, 0), pygame.Rect(1000 + self.mnu,120,math.floor(100/(100/database.CLASSES[ch['CLASS']]['STRENGHT'][ch['LEVEL']])),15))
						if database.CLASSES[ch['CLASS']]['STRENGHT'][ch['LEVEL'] - 1] > 0: pygame.draw.rect(self.display[0], (0, 255, 100), pygame.Rect(1000 + self.mnu,120,math.floor(100/(100/database.CLASSES[ch['CLASS']]['STRENGHT'][ch['LEVEL'] - 1])),15))
						#self.display[1].blit(self.fnt['DEFAULT'].render(database.BATTLE[40] + ' +' + str(ch['ATTACK'][ch['LEVEL']] - ch['ATTACK'][ch['LEVEL'] - 1]), True, (255,255,255)), ((1000 + self.mnu) * 2, 290))
						pygame.draw.rect(self.display[0], (50, 50, 50), pygame.Rect(1000 + self.mnu,145,100,15))
						pygame.draw.rect(self.display[0], (255, 255, 0), pygame.Rect(1000 + self.mnu,145,math.floor(100/(100/database.CLASSES[ch['CLASS']]['ATTACK'][ch['LEVEL']])),15))
						if database.CLASSES[ch['CLASS']]['ATTACK'][ch['LEVEL'] - 1] > 0: pygame.draw.rect(self.display[0], (0, 255, 100), pygame.Rect(1000 + self.mnu,145,math.floor(100/(100/database.CLASSES[ch['CLASS']]['ATTACK'][ch['LEVEL'] - 1])),15))
						#self.display[1].blit(self.fnt['DEFAULT'].render(database.BATTLE[41] + ' +' + str(ch['AGILITY'][ch['LEVEL']] - ch['AGILITY'][ch['LEVEL'] - 1]), True, (255,255,255)), ((1000 + self.mnu) * 2, 320))
						pygame.draw.rect(self.display[0], (50, 50, 50), pygame.Rect(1000 + self.mnu,170,100,15))
						pygame.draw.rect(self.display[0], (255, 255, 0), pygame.Rect(1000 + self.mnu,170,math.floor(100/(100/database.CLASSES[ch['CLASS']]['AGILITY'][ch['LEVEL']])),15))
						if database.CLASSES[ch['CLASS']]['AGILITY'][ch['LEVEL'] - 1] > 0: pygame.draw.rect(self.display[0], (0, 255, 100), pygame.Rect(1000 + self.mnu,170,math.floor(100/(100/database.CLASSES[ch['CLASS']]['AGILITY'][ch['LEVEL'] - 1])),15))
						#self.display[1].blit(self.fnt['DEFAULT'].render(database.BATTLE[42] + ' +' + str(ch['RESISTANCE'][ch['LEVEL']] - ch['RESISTANCE'][ch['LEVEL'] - 1]), True, (255,255,255)), ((1000 + self.mnu) * 2, 350))
						pygame.draw.rect(self.display[0], (50, 50, 50), pygame.Rect(1000 + self.mnu,195,100,15))
						pygame.draw.rect(self.display[0], (255, 255, 0), pygame.Rect(1000 + self.mnu,195,math.floor(100/(100/database.CLASSES[ch['CLASS']]['RESISTANCE'][ch['LEVEL']])),15))
						if database.CLASSES[ch['CLASS']]['RESISTANCE'][ch['LEVEL'] - 1] > 0: pygame.draw.rect(self.display[0], (0, 255, 100), pygame.Rect(1000 + self.mnu,195,math.floor(100/(100/database.CLASSES[ch['CLASS']]['RESISTANCE'][ch['LEVEL'] - 1])),15))
						#self.display[1].blit(self.fnt['DEFAULT'].render(database.BATTLE[43] + ' +' + str(ch['VITALITY'][ch['LEVEL']] - ch['VITALITY'][ch['LEVEL'] - 1]), True, (255,255,255)), ((1000 + self.mnu) * 2, 380))
						pygame.draw.rect(self.display[0], (50, 50, 50), pygame.Rect(1000 + self.mnu,220,100,15))
						pygame.draw.rect(self.display[0], (255, 255, 0), pygame.Rect(1000 + self.mnu,220,math.floor(100/(100/database.CLASSES[ch['CLASS']]['VITALITY'][ch['LEVEL']])),15))
						if database.CLASSES[ch['CLASS']]['VITALITY'][ch['LEVEL'] - 1] > 0: pygame.draw.rect(self.display[0], (0, 255, 100), pygame.Rect(1000 + self.mnu,220,math.floor(100/(100/database.CLASSES[ch['CLASS']]['VITALITY'][ch['LEVEL'] - 1])),15))
				#LOST SCREEN
				elif self.turn == -5:
					self.display[0].blit(self.fnt['MININFO'].render(database.BATTLE[8], True, (255,255,255)), (200 + self.mnu, 70))
					self.display[1].blit(self.fnt['DEFAULT'].render('-$' + str(resources.MONEY), True, (255,255,255)), ((200 + self.mnu) * 2, 240))
		#INVENTORY
		if self.invfade < 1050:
			if self.inventory == 2: t = 1
			else: t = 0
			isrf = self.inv.show(self.opt, self.lopt, self.mnu, self.exvar, t)
			self.display[0].blit(isrf[0], (610 - self.invfade,60))
			self.display[1].blit(isrf[1], ((620 - self.invfade) * 2,140))
			lyr2 = True
		if self.inventory > 0:
			if self.inv.itmov == '': self.hpctrl = database.HINTS['INVENTORY_ITEMS']
			elif self.inv.itmov[0] != 0: self.hpctrl = database.HINTS['INVENTORY_HOLD']
			else: self.hpctrl = database.HINTS['INVENTORY_ACCESORIES']
			if self.invfade < 500: self.invfade += 50
		else:
			if self.invfade < 1050: self.invfade += 50
		#SHOP
		if self.shp == True:
			if self.mnu == 0:
				self.display[0].blit(self.shpmnu.products(self.opt, self.lopt, self.products), (100,60))
			if self.mnu == 1:
				self.display[0].blit(self.shpmnu.buy(self.opt, self.lopt, self.basket), (100,60))
			if self.mnu == 2:
				lst = []
				if self.opt == 0: lst = self.products
				else: lst = self.basket[self.opt - 1]
				ssrf = self.shpmnu.mercator(self.opt, self.lopt, lst, self.promo)
				self.display[0].blit(ssrf[0], (100,60))
				self.display[1].blit(ssrf[1], (220,140))
			if self.mnu == 3 or self.mnu == 11 or self.mnu == 12:
				self.display[0].blit(self.shpmnu.bank(self.opt, self.lopt, self.mnu, self.extract), (100,60))
			lyr2 = True
		#PHONE
		pps = math.floor(self.displayzw/2) - math.floor(self.phn.scr[1].get_width()/4)
		if self.phofa > 0:
			self.display[0].blit(pygame.image.load('Backgrounds/phone.png'), (pps - 10, 400 - self.phofa))
			if self.battle == False: pygame.draw.rect(self.display[0], (10,10,10), pygame.Rect(pps,430 - self.phofa,math.floor(self.phn.scr[1].get_width()/2),250))
		if self.phone > 0:
			if self.phofa == 320: self.ch_sfx.play(resources.SOUND['PHONE_UNLOCK'])
			if self.phofa < 360: self.phofa += 40
		else:
			if self.phofa == 360: self.ch_sfx.play(resources.SOUND['PHONE_LOCK'])
			if self.phofa > 0: self.phofa -= 40
		if self.phofa == 360 and self.phn.battery > 0:
			bsrf = self.phn.bar(self.signal)
			self.display[0].blit(bsrf[0], (pps,70))
			self.display[1].blit(bsrf[1], (pps * 2,140))
			if self.battle == False:
				if self.phone == 1: srf = self.phn.apps(self.opt, self.lopt); self.hpctrl = database.HINTS['PHONE_APPS']
				elif self.phone == 2: srf = self.phn.map(False, self.map, self.tilrect, self.player[0], self.en, self.signs, self.opt, self.lopt, self.mnu, self.signal); self.hpctrl = database.HINTS['PHONE_MAP']
				elif self.phone == 3: srf = self.phn.contacts(self.opt, self.lopt, self.mnu); self.hpctrl = database.HINTS['PHONE_CONTACTS']
				elif self.phone == 4: srf = self.phn.email(self.opt, self.lopt, self.mnu, self.signal); self.hpctrl = database.HINTS['PHONE_EMAIL']
				elif self.phone == 5: srf = self.phn.news(self.lopt, self.mnu, self.signal); self.hpctrl = database.HINTS['PHONE_NEWS']
				elif self.phone == 6: srf = self.phn.radio(self.fm, self.msc); self.hpctrl = database.HINTS['PHONE_RADIO']
				elif self.phone == 7: srf = self.phn.camera(self.lopt, self.signal); self.hpctrl = database.HINTS['PHONE_CAMERA']
				elif self.phone == 8: srf = self.phn.bestiary(self.opt, self.lopt, self.mnu, self.signal); self.hpctrl = database.HINTS['PHONE_BESTIARY']
				elif self.phone == 9: srf = self.phn.task(self.opt, self.lopt, self.mnu); self.hpctrl = database.HINTS['PHONE_TASKS']
				elif self.phone == 10: srf = self.phn.status(self.opt); self.hpctrl = database.HINTS['PHONE_STATUS']
				elif self.phone == 11: srf = self.phn.tactics(self.opt, self.lopt, self.mnu, self.signal); self.hpctrl = database.HINTS['PHONE_TACTICS']
				elif self.phone == 12: srf = self.phn.achievements(self.lopt, self.signal); self.hpctrl = database.HINTS['PHONE_ACHIEVEMENTS']
				elif self.phone == 13: srf = self.phn.ranking(self.opt, self.signal); self.hpctrl = database.HINTS['PHONE_RANKING']
				elif self.phone == 14: srf = self.phn.help(self.lopt, self.mnu); self.hpctrl = database.HINTS['PHONE_MANUAL']
				elif self.phone == 15: srf = self.phn.settings(self.lopt, self.mnu, self.opt); self.hpctrl = database.HINTS['PHONE_SETTINGS']
				elif self.phone == 16: srf = self.phn.info(self.lopt); self.hpctrl = database.HINTS['PHONE_ABOUT']
				elif self.phone == 17 and self.nb != '': srf = self.phn.call(self.opt, self.nb); self.hpctrl = database.HINTS['PHONE_CALLING']
			else: self.phn.photo(self.bbg, self.foe, pps); self.hpctrl = database.HINTS['PHONE_PHOTO']
			self.display[0].blit(srf[0], (pps,88))
			self.display[1].blit(srf[1], (pps * 2,176))
			if self.rectdebug == True:
				for i in self.phn.optrects: pygame.draw.rect(self.display[1], (255,0,0), i)
		elif self.phofa == 360:
			self.display[0].blit(pygame.image.load('Backgrounds/battery_low.png'), (pps + 60, 510 - self.phofa))
			if self.battle == True: pygame.draw.rect(self.display[0], (10,10,10), pygame.Rect(pps,430 - self.phofa,180,250))
			lyr2 = True
		#NAMING
		if self.nmenu.show == True:
			self.display[0].blit(self.nmenu.run()[0], (200, 100))
			self.display[1].blit(self.nmenu.run()[1], (420, 220))
			if self.nmenu.ninput == True: self.hpctrl = database.HINTS['NAMING']
			lyr2 = True
		#DIALOG
		if self.dlgfa < 500 and resources.SCENE != -1 and self.nmenu.show == False:
			if self.dlg != []:
				self.dlgy = 0
				sd = False
				opt = 1
				ind = 0
				for i in self.dlg:
					if i == 0: sd = not sd
				for i in self.dlg[::-1]:
					if isinstance(i,str):
						txt = self.fnt['DEFAULT'].render(i, True, (255, 255, 255))
						txtsz = math.floor(self.fnt['DEFAULT'].size(i)[0]/2) + 10
					if i != 1 and i != 0 and len(i) != 0:
						if sd == False:
							pygame.draw.rect(self.display[0], (0, 0, 0), pygame.Rect(20,200 - self.dlgy,5 + txtsz,25))
							pygame.draw.rect(self.display[0], (resources.COLOR[0],resources.COLOR[1],resources.COLOR[2]), pygame.Rect(20,225 - self.dlgy,5 + txtsz,5))
							pygame.draw.polygon(self.display[0], (resources.COLOR[0],resources.COLOR[1],resources.COLOR[2]), ((25,225 - self.dlgy),(45,225 - self.dlgy),(25,235 - self.dlgy)))
							pygame.draw.polygon(self.display[0], (0, 0, 0), ((25,221 - self.dlgy),(45,221 - self.dlgy),(25,231 - self.dlgy)))
							lyr2 = True
						else:
							if self.lopt == opt:
								pygame.draw.rect(self.display[0], (resources.COLOR[0],resources.COLOR[1],resources.COLOR[2]), pygame.Rect(578 - txtsz,200 - self.dlgy,5 + txtsz,25))
								pygame.draw.rect(self.display[0], (0, 0, 0), pygame.Rect(578 - txtsz,225 - self.dlgy,5 + txtsz,5))
								pygame.draw.polygon(self.display[0], (0, 0, 0), ((558,225 - self.dlgy),(578,225 - self.dlgy),(578,235 - self.dlgy)))
								pygame.draw.polygon(self.display[0], (resources.COLOR[0],resources.COLOR[1],resources.COLOR[2]), ((558,221 - self.dlgy),(578,221 - self.dlgy),(578,231 - self.dlgy)))
							else:
								pygame.draw.rect(self.display[0], (0, 0, 0), pygame.Rect(578 - txtsz,200 - self.dlgy,5 + txtsz,25))
								pygame.draw.rect(self.display[0], (resources.COLOR[0],resources.COLOR[1],resources.COLOR[2]), pygame.Rect(578 - txtsz,225 - self.dlgy,5 + txtsz,5))
								pygame.draw.polygon(self.display[0], (resources.COLOR[0],resources.COLOR[1],resources.COLOR[2]), ((558,225 - self.dlgy),(578,225 - self.dlgy),(578,235 - self.dlgy)))
								pygame.draw.polygon(self.display[0], (0, 0, 0), ((558,221 - self.dlgy),(578,221 - self.dlgy),(578,231 - self.dlgy)))
							opt += 1
					if i == 0:
						if sd == False: sd = True
						elif sd == True: sd = False
					elif isinstance(i, str):
						if sd == False: self.display[1].blit(txt, (30 * 2, (207 - self.dlgy) * 2))
						else: self.display[1].blit(txt, ((588 - txtsz) * 2, (207 - self.dlgy) * 2))
						self.dlgy += 40
					ind += 1
		#EASTER EGG
		if self.cityname == 'TWNN': self.display[0].blit(pygame.image.load('Sprites/TWNN.png'), (35,0))
		#NOTIFICATIONS
		if self.notx > 0:
			ch = resources.CHARACTERS[resources.PARTY[resources.FORMATION][0]]
			#HP BAR
			if self.nottxt.startswith('hp_'):
				self.display[0].blit(pygame.image.load('Sprites/who_' + resources.PARTY[resources.FORMATION][0] + '.png'), (-90 + self.notx,45))
				pygame.draw.rect(self.display[0], (255,255,255), pygame.Rect(-170 + self.notx,40,160,30))
				pygame.draw.rect(self.display[0], (0,0,0), pygame.Rect(-168 + self.notx,42,156,26))
				pygame.draw.rect(self.display[0], (10,10,10), pygame.Rect(-60 + self.notx,45,70,20))
				pygame.draw.rect(self.display[0], (255,255,0), pygame.Rect(-60 + self.notx,45,int(70/(database.CLASSES[ch['CLASS']]['VITALITY'][ch['LEVEL']]/ch['HP'])),20))
				pygame.draw.rect(self.display[0], (0,255,0), pygame.Rect(-60 + self.notx,45,int(70/(database.CLASSES[ch['CLASS']]['VITALITY'][ch['LEVEL']]/ch['HP'] - int(self.nottxt[3:]))),20))
			#MORALITY BAR
			elif self.nottxt.startswith('ml_'):
				pygame.draw.rect(self.display[0], (255,255,255), pygame.Rect(-170 + self.notx,40,160,30))
				pygame.draw.rect(self.display[0], (0,0,0), pygame.Rect(-168 + self.notx,42,156,26))
				if resources.CHARACTERS[resources.PARTY[resources.FORMATION][0]]['MORALITY'] > 0:
					pygame.draw.rect(self.display[0], (255,255,0), pygame.Rect(-90 + self.notx,45,int(70/(10/ch['MORALITY'])),20))
					pygame.draw.rect(self.display[0], (0,175,0), pygame.Rect(-90 + self.notx,45,int(70/(10/ch['MORALITY'] - int(self.nottxt[3:]))),20))
				if resources.CHARACTERS[resources.PARTY[resources.FORMATION][0]]['MORALITY'] < 0:
					pygame.draw.rect(self.display[0], (255,255,0), pygame.Rect(-int(70/(10/ch['MORALITY'])) - 160 + self.notx,45,int(70/(10/ch['MORALITY'])),20))
					pygame.draw.rect(self.display[0], (175,0,0), pygame.Rect(-int(70/(10/ch['MORALITY'])) - 160 + self.notx,45,int(70/(10/ch['MORALITY'] - int(self.nottxt[3:]))),20))
				pygame.draw.line(self.display[0], (255,255,255), (-90 + self.notx,42),(-90 + self.notx,68),2)
			#MESSAGE
			else:
				sz = math.floor(self.fnt['DEFAULT'].size(self.nottxt)[0]/2) + 30
				if self.notcol != (0,0,0): pygame.draw.rect(self.display[0], (0,0,0), pygame.Rect(-183 + self.notx,27,sz,56))
				else: pygame.draw.rect(self.display[0], (255,255,255), pygame.Rect(-183 + self.notx,27,sz,56))
				pygame.draw.rect(self.display[0], self.notcol, pygame.Rect(-180 + self.notx,30,sz - 6,50))
				self.display[1].blit(self.fnt['DEFAULT'].render(self.nottxt, True, (0, 0, 0)), ((-170 + self.notx) * 2, 45 * 2))
		#TUTORIALS
		if self.tutorial['OUTPUT'] != []:
			nxt = False
			if self.tutorial['GO'] > 0 and self.phone == self.tutorial['GO']: self.tutorial['TIME'] = self.tutorial['WAIT']; nxt = True

			if self.tutorial['TIME'] < self.tutorial['WAIT']:
				if self.tutorial['FADE'] < 200: self.tutorial['FADE'] += 20
			elif self.tutorial['TIME'] >= self.tutorial['WAIT']: nxt = True
			if nxt == True:
				if self.tutorial['NEXT'] != '':
					self.tutorial = {'TEXT': database.TUTORIALS[self.tutorial['NEXT']].copy(), 'OUTPUT': [], 'FADE': 200, 'TIME': 0, 'WAIT': 300, 'NEXT': '','GO': 0}
					for j in self.tutorial['TEXT']:
						if isinstance(j,list):
							if j[0] == 'phone':
								self.tutorial['GO'] = j[1]
								if len(j) > 2: self.tutorial['NEXT'] = j[2]
							if j[0] == 'wait':
								self.tutorial['WAIT'] = j[1]
								if len(j) > 2: self.tutorial['NEXT'] = j[2]
							if j[0] == 'image':
								self.tutorial['OUTPUT'].append(j)
						else: self.tutorial['OUTPUT'].append(j)
				else:
					self.tutorial['GO'] = 0
					if self.tutorial['FADE'] > 0: self.tutorial['FADE'] -= 10
					else: self.tutorial['OUTPUT'] = []

			if self.tutorial['GO'] == 0: self.tutorial['TIME'] += 1
			pygame.draw.rect(self.display[0], (250,250,250), pygame.Rect(578 - self.tutorial['FADE'],18,self.tutorial['FADE'] + 4,int(self.tutorial['FADE']/2) + 4))
			pygame.draw.rect(self.display[0], (10,10,10), pygame.Rect(580 - self.tutorial['FADE'],20,self.tutorial['FADE'],int(self.tutorial['FADE']/2)))
			lyr2 = True
			if self.tutorial['FADE'] == 200:
				x = 0
				y = 0
				sid = 0
				end = 0
				ky = [resources.UP[0],resources.DOWN[0],resources.LEFT[0],resources.RIGHT[0],resources.ACT[0],resources.RUN[0],resources.BAG[0],resources.PHONE[0]]
				for j in self.tutorial['OUTPUT']:
					if isinstance(j,str): self.display[1].blit(self.fnt['DEFAULT'].render(j, True, (250, 250, 250)), (770 + x,50 + y))
					elif isinstance(j,list) and j[0] == 'image': self.display[0].blit(pygame.image.load('Sprites/' + j[1] + '.png'), (520 + x,25 + y))
					elif j == 0:
						for i in range(end): sid += 1
						x = 0
						y += 20
					else:
						if ky[j - 1] == pygame.K_LSHIFT: out = 'À'
						elif ky[j - 1] == pygame.K_RSHIFT: out = 'À'
						elif ky[j - 1] == pygame.K_LCTRL: out = 'Á'
						elif ky[j - 1] == pygame.K_RCTRL: out = 'Á'
						elif ky[j - 1] == pygame.K_LALT: out = 'Â'
						elif ky[j - 1] == pygame.K_RALT: out = 'Â'
						elif ky[j - 1] == pygame.K_BACKSPACE: out = 'Ã'
						elif ky[j - 1] == pygame.K_RETURN: out = 'Ä'
						elif ky[j - 1] == pygame.K_UP: out = 'È'
						elif ky[j - 1] == pygame.K_LEFT: out = 'É'
						elif ky[j - 1] == pygame.K_DOWN: out = 'Ê'
						elif ky[j - 1] == pygame.K_RIGHT: out = 'Ë'
						else: out = pygame.key.name(ky[j - 1]).upper()
						self.display[0].blit(self.fnt['CONTROLKEYS'].render(out, True, (250, 250, 250)), (385 + x,30 + y))
						for l in self.tutorial['OUTPUT'][sid:end]:
							if l in ['m','w','M','Q','T','U','V','W','Y','?']: x += 8
							elif l in ['f','r']: x += 6
							elif l in ['J']: x += 5
							elif l in ['l']: x += 4
							elif l in ['i','I','!','.',',']: x += 2
							else: x += 7
					end += 1
		#CHAPTER NAME
		if resources.SCENE == -1:
			srf = pygame.Surface((self.displayzw,self.displayzh))
			srf.set_alpha(200)
			srf.fill((221, 0, 0))
			self.display[0].blit(srf, (0,0))
			pygame.draw.rect(self.display[0], (250,250,250), pygame.Rect(0,160,600,80))
			self.display[0].blit(self.fnt['MININFO'].render(database.CHAPTERS[resources.CHAPTER][0].lower(), True, (10, 10, 10)), (10, 200))
			pygame.draw.rect(self.display[0], (resources.COLOR[0],resources.COLOR[1],resources.COLOR[2]), pygame.Rect(0,167,600,3))
			pygame.draw.rect(self.display[0], (10,10,10), pygame.Rect(0,170,600,22))
			pygame.draw.rect(self.display[0], (resources.COLOR[0],resources.COLOR[1],resources.COLOR[2]), pygame.Rect(0,192,600,3))
			self.display[1].blit(self.fnt['DEFAULT'].render(database.CHAPTERS[resources.CHAPTER][1], True, (250, 250, 250)), (20, 350))
			lyr2 = True
		#HELP CONTROLS
		if self.hpctrl != []:
			hpsz = 0
			for i in self.hpctrl[::-1]:
				if isinstance(i,str):
					hptxt = self.fnt['DEFAULT'].render(' ' + i + ' ', True, (250, 250, 250))
					hpsz += self.fnt['DEFAULT'].size(' ' + i + ' ')[0]
					self.display[1].blit(hptxt, (self.windoww - 40 - hpsz, self.windowh - 40))
				elif isinstance(i,int):
					ky = [resources.UP[0],resources.DOWN[0],resources.LEFT[0],resources.RIGHT[0],resources.ACT[0],resources.RUN[0],resources.BAG[0],resources.PHONE[0]]
					if ky[i] == pygame.K_LSHIFT: out = 'À'
					elif ky[i] == pygame.K_RSHIFT: out = 'À'
					elif ky[i] == pygame.K_LCTRL: out = 'Á'
					elif ky[i] == pygame.K_RCTRL: out = 'Á'
					elif ky[i] == pygame.K_LALT: out = 'Â'
					elif ky[i] == pygame.K_RALT: out = 'Â'
					elif ky[i] == pygame.K_BACKSPACE: out = 'Ã'
					elif ky[i] == pygame.K_RETURN: out = 'Ä'
					elif ky[i] == pygame.K_UP: out = 'È'
					elif ky[i] == pygame.K_LEFT: out = 'É'
					elif ky[i] == pygame.K_DOWN: out = 'Ê'
					elif ky[i] == pygame.K_RIGHT: out = 'Ë'
					else: out = pygame.key.name(ky[i]).upper()
					hpsz += self.fnt['CONTROLKEYS'].size(out)[0] + 20
					self.display[0].blit(self.fnt['CONTROLKEYS'].render(out, True, (250, 250, 250)), (self.displayzw - 20 - math.floor(hpsz/2), self.displayzh - 20))
		#CAMERA X
		if (self.map.width * self.map.tilewidth) > self.displayzw:
			if self.portalgo == {}:
				#PLAYERS CAMERA
				if self.speakin == 0:
					camx = 0
					for i in self.player: camx += i['RECT'].x
					self.cam.x += int(((camx/len(self.player))  - self.cam.x - self.displayzw/2)/15)
				#DIALOG CAMERA
				else: self.cam.x += int((self.speakin.x  - self.cam.x - self.displayzw/2)/15)
			if self.cam.x < 0: self.cam.x = 0
			if self.cam.x > (self.map.width * self.map.tilewidth) - self.displayzw: self.cam.x = (self.map.width * self.map.tilewidth) - self.displayzw
		else: self.cam.x = -int((self.displayzw - (self.map.width * self.map.tilewidth))/2)
		#CAMERA Y
		if (self.map.height * self.map.tileheight) > self.displayzh:
			if self.portalgo == {}:
				#PLAYERS CAMERA
				if self.speakin == 0:
					camy = 0
					for i in self.player: camy += i['RECT'].y
					self.cam.y += int(((camy/len(self.player))  - self.cam.y - self.displayzh/2)/15)
				#DIALOG CAMERA
				else: self.cam.y += int((self.speakin.y  - self.cam.y - self.displayzh/2)/15)
			if self.cam.y < 0: self.cam.y = 0
			if self.cam.y > (self.map.height * self.map.tileheight) - self.displayzh: self.cam.y = (self.map.height * self.map.tileheight) - self.displayzh
		else: self.cam.y = -int((self.displayzh - (self.map.height * self.map.tileheight))/2)
		#UPDATE SCREEN & PAUSE SOUND
		if pygame.display.get_active():
			if self.ch_msc.get_busy() == False: self.ch_msc.unpause()
			if self.ch_rad.get_busy() == False: self.ch_rad.unpause()
			if self.ch_rng.get_busy() == False: self.ch_rng.unpause()
			#UPDATE SCREEN
			if self.scrmov == None:
				self.screen.blit(pygame.transform.scale(self.display[0], (self.windoww, self.windowh)), (self.displayx, self.displayy))
				self.screen.blit(pygame.transform.scale(self.display[1], (self.windoww, self.windowh)), (self.displayx, self.displayy))
			else:
				self.scrspd += 2
				self.scrmov += self.scrspd
				if self.scrmov > self.windowh: self.scrmov = 0
				self.screen.blit(pygame.transform.scale(self.display[0], (self.windoww, self.windowh)), (self.displayx, self.displayy + self.scrmov - self.windowh - 20))
				self.screen.blit(pygame.transform.scale(self.display[0], (self.windoww, self.windowh)), (self.displayx, self.displayy + self.scrmov))
			#MOUSE
			if resources.MOUSE == True:
				self.screen.blit(pygame.image.load('Sprites/cursor_' + str(resources.CURSOR) + '.png'), pygame.mouse.get_pos())
			#FLIP
			pygame.display.flip()
		else:
			self.ch_msc.pause()
			self.ch_rad.pause()
			self.ch_rng.pause()

	def loading(self):
		for event in pygame.event.get():
			#EXIT
			if event.type == pygame.QUIT:
				self.classrun = 0
				resources.recent_data(1,resources.ID)
				pygame.quit()
				sys.exit()
				exit()
			#RESIZE
			if event.type == pygame.VIDEORESIZE:
				self.windowh = event.h
				sh = int(event.h/4)
				self.windoww = 6 * sh
				self.screen = pygame.display.set_mode((self.windoww, self.windowh), pygame.RESIZABLE)
				self.FPS = int(event.w/20)
		self.screen.fill((0,0,0),pygame.Rect(1120,720,30,30))
		if self.loadingif != None:
			self.loadingif += 0.01
			if str(self.loadingif)[2] == '0': upd = True
			else: upd = False
			if self.loadingif >= 8.0: self.loadingif = 0.0
		if upd == True:
			self.screen.blit(pygame.image.load('Sprites/loading_' + str(math.floor(self.loadingif)) + '.png'), (1120, 720))
			pygame.display.update(pygame.Rect(1120,720,30,30))

	def crash(self):
		again = False
		while again == False:
			for event in pygame.event.get():
				#EXIT
				if event.type == pygame.QUIT:
					self.classrun = 0
					resources.recent_data(1,resources.ID)
					pygame.quit()
					sys.exit()
					exit()
				#RESIZE
				if event.type == pygame.VIDEORESIZE:
					self.windowh = event.h
					sh = int(event.h/4)
					self.windoww = 6 * sh
					self.screen = pygame.display.set_mode((self.windoww, self.windowh), pygame.RESIZABLE)
					self.FPS = int(event.w/20)
				#SKIP
				if event.type == pygame.KEYDOWN:
					again = True
			self.screen.fill((0,0,0))

			et, ev, eb = sys.exc_info()
			tlist = []
			for t in traceback.extract_tb(eb):
				tlist.append((t[0],t[1],t[2],t[3]))

			fnt = pygame.font.SysFont('Calibri', 15)
			self.screen.blit(fnt.render(str(et.__name__),True,(10,250,10)),(10,20))
			self.screen.blit(fnt.render(str(ev),True,(10,250,10)),(10,40))
			y = 60
			for j in tlist:
				self.screen.blit(fnt.render(str(j),True,(10,250,10)),(10,y))
				y += 20
			pygame.display.flip()

	def run(self):
		if self.FPS > 0: self.glock.tick(self.FPS)
		if self.nmenu.show == False:
			self.events()
		self.draw()
		#WAITIME
		for i in range(len(self.waitlst)):
			if self.waitlst[i][1] < self.waitime:
				del self.waitlst[i]
				break
		for i in self.waitlst:
			if i[1] == self.waitime:
				#SUNNY WEATHER
				if i[0] == 'sun':
					resources.WEATHER = 0
					self.waitlst.append(['rain',self.waitime + 3600])
				#RAINY WEATHER
				elif i[0] == 'rain':
					resources.WEATHER = 1
					self.waitlst.append(['sun',self.waitime + 3600])
				#REPELLENT EFFECT
				elif i[0].startswith('repellent'):
					resources.CHARACTERS[int(i[0][9])]['HEALTH'] = 0
				#CALLING
				elif i[0].startswith('cal'):
					self.ch_ton.play(resources.SOUND['CALLING'],-1)
					self.ch_rng.play(resources.SOUND['RINGTONE_' + str(self.phn.pbg)],-1)
					if self.radonoff == True: pygame.mixer.music.pause()
					if self.phone > 0: self.phone = 17
					self.nb = i[0][3:]
					self.waitlst.append(['cutcal',self.waitime + 1200])
				#CUTTING CALL
				elif i[0].startswith('cutcal'):
					if self.nb != '':
						self.ch_ton.stop()
						self.ch_rng.stop()
						self.nb = ''
						if self.phone == 17: self.phone = 1
				#DELIVERY
				elif i[0] == 'delivery':
					if self.dlgfa > 0:
						self.dialog([(30,pygame.Rect(self.player[0]['RECT'].x - 430,self.player[0]['RECT'].y,0,0),i[2]['INDEX'],i[2]['WHO'],i[2]['TYPE']),
							(24,'n',(self.player[0]['RECT'].x - 30,self.player[0]['RECT'].y),3)])
				#RADIOEE
				elif i[0].startswith('radioee'):
					self.ch_ton.stop()
					pygame.mixer.music.load('Music/' + i[2] + '.mp3')
					pygame.mixer.music.play()
					self.msc = -1
				#TIME WARNING
				elif i[0].startswith('advice'):
					if self.dlgfa > 0:
						self.dialog(database.DIALOGS['ADVICE'])
		#FOOD WASTE AND CLOTH DIRT
		u = 0
		for b in resources.INVENTORY:
			for j in b:
				for i in j:
					if i[0].startswith('food') == True and i[0].endswith('wasted') == False:
						if int(i[1][2:4]) <= resources.DATE[1]:
							if int(i[1][0:2]) <= resources.DATE[0]:
								i[0] += '_wasted'
					elif i[0].startswith('clth') == True:
						if int(i[1]) > 0: i[1] = str(int(i[1]) - 1)
						if int(i[1]) == 0: resources.CHARACTERS[u]['HEALTH'] = 3
			u += 1
		#SECONDS
		self.waitime += 1
		battery = self.inv.find(resources.PARTY[resources.FORMATION][0],'phone')
		#NORMAL
		if self.sleepin == False:
			resources.TIME[2] += 1
			#BASIC NECESITIES
			for p in resources.PARTY[resources.FORMATION]:
				if resources.CHARACTERS[p]['HUNGER'] == 0: resources.CHARACTERS[p]['HEALTH'] = 6
				else: resources.CHARACTERS[p]['HUNGER'] -= 1
				if resources.CHARACTERS[p]['THIRST'] == 0: resources.CHARACTERS[p]['HEALTH'] = 7
				else: resources.CHARACTERS[p]['THIRST'] -= 1
				if resources.CHARACTERS[p]['SLEEP'] == 0: resources.CHARACTERS[p]['HEALTH'] = 8
				else: resources.CHARACTERS[p]['SLEEP'] -= 10 + resources.CHARACTERS[p]['STAMINA']
			if self.phone > 0 and battery != None:
				if resources.CHAPTER > 0: battery[1] = str(int(battery[1]) - 1)
				elif resources.SCENE > 0: battery[1] = str(int(battery[1]) - 1)
		#SLEEP
		else:
			resources.TIME[1] += 5
			for p in resources.PARTY[resources.FORMATION]:
				if resources.CHARACTERS[p]['HP'] < database.CLASSES[resources.CHARACTERS[p]['CLASS']]['VITALITY'][resources.CHARACTERS[p]['LEVEL']]:
					resources.CHARACTERS[p]['HP'] += 1
				if resources.CHARACTERS[p]['SLEEP'] < 10000: resources.CHARACTERS[p]['SLEEP'] += 50 + (resources.CHARACTERS[p]['STAMINA'] * 10)
		print(resources.CHARACTERS[1]['HUNGER'])
		print(resources.CHARACTERS[1]['THIRST'])
		print(resources.CHARACTERS[1]['SLEEP'])
		#BATTERY
		if battery != None:
			self.phn.battery = int(battery[1])
			if int(battery[1]) < 0:
				if self.radonoff == True:
					self.radonoff = False
					self.ch_ton.stop()
					pygame.mixer.music.stop()
				battery[1] = '0'
		#MINUTES
		if resources.TIME[2] >= 60:
			resources.TIME[1] += 1
			resources.TIME[2] = 0
		#HOURS
		if resources.TIME[1] >= 60:
			resources.TIME[0] += 1
			resources.TIME[1] = 0
			if self.sleepin == True:
				for u in resources.PARTY[resources.FORMATION]:
					if resources.CHARACTERS[u]['HEALTH'] in (4,5,9,10,11):
						resources.CHARACTERS[u]['HEALTH'] = 0
			#DAYTIME CHANGE
			if resources.TIME[0] in [6,18]: self.rendermap(self.room)
		#DAYS
		if resources.TIME[0] >= 24:
			resources.DATE[0] += 1
			resources.DATE[3] += 1
			resources.TIME[0] = 0
		#WEEKS
		if resources.DATE[3] > 7:
			resources.DATE[3] = 1
			resources.DATE[4] += 1
		if resources.DATE[4] > 8:
			resources.DATE[4] = 1
		#MONTHS
		if resources.DATE[1] in [1,3,5,7,8,10,12]:	
			if resources.DATE[0] > 31:
				resources.DATE[1] += 1
				resources.DATE[0] = 1
		elif resources.DATE[1] in [4,6,9,11]:	
			if resources.DATE[0] > 30:
				resources.DATE[1] += 1
				resources.DATE[0] = 1
		elif resources.DATE[1] == 2:	
			if resources.DATE[0] > 28:
				resources.DATE[1] += 1
				resources.DATE[0] = 1
		#YEARS
		if resources.DATE[1] > 12:
			resources.DATE[2] += 1
			resources.DATE[1] = 1
		#RADIOEE
		if self.radonoff == True:
			for i in database.RADIOEE:
				if int(i[2][0:2]) == resources.TIME[0] and int(i[2][2:4]) == resources.TIME[1]:
					if i[1] == None: ply = True
					elif int(i[1][0:2]) == resources.DATE[0] and int(i[1][2:4]) == resources.DATE[1]: ply = True
					else: ply = False
					if ply == True and self.msc != -2:
						self.msc = -2
						pygame.mixer.music.stop()
						self.ch_ton.play(resources.SOUND['NOISE'],-1)
						self.waitlst.append(['radioee',self.waitime + 60,i[0]])
		#GAMETIME
		resources.GAMETIME += self.glock.get_rawtime()

l = Loading()
while l.classrun == True: l.run()
t = Title()
while True:
	if resources.GAMETIME != 0:
		while t.classrun == True: t.run()
	else: resources.new_data()
	g = Game()
	if resources.GAMETIME > 0: g.transiction(False, 0)
	while g.classrun == 1:
		try: g.run()
		except: g.crash()
	if g.classrun == 0: break
	if g.classrun == 2:
		pygame.mixer.stop()
		t.ton.play(resources.SOUND['NOISE'],-1)
		t.classrun = True
		t.winbar = 50
		t.wait = 100
		t.mnu = 7
		t.tv = 0
