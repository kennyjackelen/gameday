#!/usr/bin/env python
import xml.etree.ElementTree as ET
from pymongo import MongoClient
import os
import sys

class PitchType:
  Ball = 'B'
  Strike = 'S'
  InPlay = 'X'

class DB:
  def __init__(self):
    self.client = MongoClient()
    self.gameday = self.client['gameday']   # open gameday database
    self.pitches = self.gameday['pitches']  # open pitches collection
  def AddPitch(self, pitch):
    self.pitches.insert(pitch)

database = DB()

gameID = ''
inning = 0
top = True
outs = 0
balls = 0
strikes = 0

def Main():
  global gameID
  filename = sys.argv[1]
  if not os.path.exists(filename):
    print 'File does not exist!'
    return
  gameID = os.path.basename(os.path.abspath(os.path.join(filename,'../..')))  # go up two directories and grab the base dir name
  print gameID
  #LoadGame('../data/pitches/year_2013/month_07/day_07/gid_2013_07_07_atlmlb_phimlb_1/inning/inning_all.xml')
  LoadGame(filename)

def LoadGame(filename):
  tree = ET.parse(filename)
  root = tree.getroot()
  ParseGame(root)

def ParseGame(xmlRoot):
  for inningTag in xmlRoot:
    if inningTag.tag == 'inning':
      ParseInning(inningTag)

def ParseInning(inningTag):
  global inning
  inning = inningTag.attrib['num']
  #print 'Inning ' + inningTag.attrib['num']
  for halfInning in inningTag:
    if halfInning.tag == 'top' or halfInning.tag == 'bottom':
      ParseHalfInning(halfInning)

def ParseHalfInning(halfInningTag):
  global top
  top = (halfInningTag.tag == 'top')
  for atBat in halfInningTag:
    if atBat.tag == 'atbat':
      ParseAtBat(atBat)

def ParseAtBat(atBatTag):
  global balls,strikes
  balls = 0
  strikes = 0
  for pitch in atBatTag:
    if pitch.tag == 'pitch':
      ParsePitch(pitch,atBatTag)

def ParsePitch(pitchTag,atBatTag):
  global balls,strikes,database
  result = pitchTag.attrib['type']
  pitchTag.attrib['balls'] = balls
  pitchTag.attrib['strikes'] = strikes
  pitchTag.attrib['inning'] = inning
  pitchTag.attrib['top'] = top
  pitchTag.attrib['batter'] = atBatTag.attrib['batter']
  pitchTag.attrib['pitcher'] = atBatTag.attrib['pitcher']
  pitchTag.attrib['p_throws'] = atBatTag.attrib['p_throws']
  pitchTag.attrib['stand'] = atBatTag.attrib['stand']
  pitchTag.attrib['event'] = atBatTag.attrib['event']
  pitchTag.attrib['gameID'] = gameID
  #print pitchTag.attrib
  database.AddPitch(pitchTag.attrib)
  #print str(balls) + '-' + str(strikes) + ': ' + result
  if result == PitchType.Ball:
    balls += 1
  elif strikes < 2 and result == PitchType.Strike:
    strikes += 1

Main()