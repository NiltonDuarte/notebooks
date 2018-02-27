# -*- coding: utf-8 -*-

import json
from collections import namedtuple


class VNet:
  def __init__(self,name, switches, links, hosts):
    self.name = name
    self.switches = switches
    self.links = links
    self.hosts = hosts

  def reprJSON(self):
    return dict(name=self.name, switches = self.switches, links = self.links, hosts = self.hosts)

class Switch:
  def __init__(self, id, dpid, whx):
    self.id = id
    self.dpid = dpid
    self.whx = whx

  def reprJSON(self):
    return dict(id = self.id, dpid = self.dpid, whx = self.whx)

class Link:
  def __init__(self, id, switch1, switch2):
    self.id = id
    self.switch1 = switch1
    self.switch2 = switch2

  def reprJSON(self):
    return dict(id = self.id, switch1 = self.switch1.id, switch2 = self.switch2.id)

class Host:
  def __init__(self, id, switch):
    self.id = id
    self.switch = switch

  def reprJSON(self):
    return dict(id = self.id, switch = self.switch.id)

class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj,'reprJSON'):
            return obj.reprJSON()
        else:
            return json.JSONEncoder.default(self, obj)

def myVNetDecoder(jStr):
  jdict = json.loads(jStr)
  #print dict
  sws = {}
  for sw in jdict["switches"]:
    sws[sw["id"]]=Switch(sw["id"], sw["dpid"], sw["whx"])
  #print sws
  ls = {}
  for l in jdict["links"]:
    ls[l["id"]]=Link(l["id"], sws[l["switch1"]], sws[l["switch2"]])
  #print ls
  hs = {}
  for h in jdict["hosts"]:
    hs[h["id"]]=Host(h["id"], sws[h["switch"]])
  #print hs
  return VNet(jdict["name"], sws.values(), ls.values(), hs.values())





s1 = Switch("s1", "000001", "whx-rj")
s2 = Switch("s2", "000002", "whx-sp")
l1 = Link("l1", s1, s2)
h1 = Host("h1", s1)
h2 = Host("h2", s2)
h11 = Host("h11", s1)
vnet = VNet("vnet1", [s1, s2], [l1], [h1, h11, h2])

jStr = json.dumps(vnet.__dict__, cls=MyEncoder)
print "Original Obj dump ",jStr

jvnet= myVNetDecoder(jStr)

jStr2 = json.dumps(jvnet.__dict__, cls=MyEncoder)
print "Decoded Obj dump ",jStr2


