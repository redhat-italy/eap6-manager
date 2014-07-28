#!/usr/bin/python
__author__ = "Samuele Dell'Angelo (Red Hat)"

import urwid
import urwid.raw_display
from activecmd import StartInstanceCommand, StopInstanceCommand, StartClusterCommand, DeployCommand, \
    RestartClusterCommand, InsertJvmOptClusterCommand, CreateInstanceCommand, InsertJvmOptCommand, \
    RestartInstanceCommand, StopClusterCommand
from base import EapManagerException
from passivecmd import CheckThreadStatsCommand, CheckJgoupsMulticastRecCommand, CheckJgoupsMulticastSendCommand, \
    CheckHttpStatsCommand




from utils.Propertymanager import PropertyManager
from passivecmd.CheckDsCommand import CheckDSCommand
from activecmd.CreateSGCommand import CreateSGCommand
from passivecmd.CheckDsStatsCommand import CheckDSStatsCommand

COMMANDS = { "deploy" : DeployCommand(), "deploy Drain Mode" : DeployCommand() }
STSTCOMMANDS = {'startCluster' : StartClusterCommand() , 'stopCluster' : StopClusterCommand() , 'restartCluster' : RestartClusterCommand()
    ,'startInstance' : StartInstanceCommand() , 'stopInstance' : StopInstanceCommand() , 'restartInstance' : RestartInstanceCommand()}
ADMINCOMMANDS = {"create cluster" : CreateSGCommand(), "create instance" : CreateInstanceCommand(),
                "insert JVM Options" : InsertJvmOptCommand(), "insert JVM Options per Cluster" : InsertJvmOptClusterCommand()}
MONITORCOMMANDS = {"check datasource" : CheckDSCommand(), "check datasource statistics" : CheckDSStatsCommand(), "check thread stats" : CheckThreadStatsCommand(),
                   "check http statistics" : CheckHttpStatsCommand(), "check Jgroups Receive" : CheckJgoupsMulticastRecCommand(),
                   "check jgroups Send" : CheckJgoupsMulticastSendCommand()}

def exit_on_q(key):
    if key in ('q', 'Q'):
        raise urwid.ExitMainLoop()

def exit_program(key):
    raise urwid.ExitMainLoop()

class MenuButton(urwid.Button):
    def __init__(self, caption, callback):
        super(MenuButton, self).__init__("")
        urwid.connect_signal(self, 'click', callback)
        self._w = urwid.AttrMap(urwid.SelectableIcon(
            [u'  \N{BULLET} ', caption], 2), None, 'selected')

class SubMenu(urwid.WidgetWrap):
    def __init__(self, caption, choices):
        super(SubMenu, self).__init__(MenuButton(
            [caption, u"\N{HORIZONTAL ELLIPSIS}"], self.open_menu))
        line = urwid.Divider(u'\N{LOWER ONE QUARTER BLOCK}')
        listbox = urwid.ListBox(urwid.SimpleFocusListWalker([urwid.AttrMap(urwid.Text([u"\n  ", caption]), 'heading'),
                                                             urwid.AttrMap(line, 'line'),
                                                             urwid.Divider()] + choices + [urwid.Divider()]))
        self.menu = urwid.AttrMap(listbox, 'options')

    def open_menu(self, button):
        top.open_box(self.menu)

class Choice(urwid.WidgetWrap):
    _command = None
    def __init__(self, caption, command):
        super(Choice, self).__init__(
            MenuButton(caption, self.item_chosen))
        self.caption = caption
        self._command = command

    def item_chosen(self, button):
        urwid.RealTerminal()
        self._command.execute(jbossHome, controller, user, password)
        #response = urwid.Text([u'  You chose ', self.caption, u'\n'])
        #done = MenuButton(self.caption, self._command)
        #response_box = urwid.Filler(urwid.Pile([response, done]))
        #top.open_box(urwid.AttrMap(response_box, 'options'))

class HorizontalBoxes(urwid.Columns):
    def __init__(self):
        super(HorizontalBoxes, self).__init__([], dividechars=1)

    def open_box(self, box):
        if self.contents:
            del self.contents[self.focus_position + 1:]
        self.contents.append((urwid.AttrMap(box, 'options', focus_map),
                              self.options('given', 24)))
        self.focus_position = len(self.contents) - 1

def commandList(dictionary):
    cList = []
    for key in dictionary.keys():
        cList.append(Choice(key,dictionary[key]))
    return cList

menu_top = SubMenu(u'Main Menu', [
    SubMenu(u'Deploy Commands', commandList(COMMANDS)),
    SubMenu(u'Start/Stop Commands', commandList(STSTCOMMANDS)),
    SubMenu(u'Admin Commands', commandList(ADMINCOMMANDS)),
    SubMenu(u'Monitoring Commands', commandList(MONITORCOMMANDS)),
    ])

palette = [
    (None,  'light gray', 'black'),
    ('heading', 'black', 'light gray'),
    ('line', 'black', 'light gray'),
    ('options', 'dark gray', 'black'),
    ('focus heading', 'white', 'dark red'),
    ('focus line', 'black', 'dark red'),
    ('focus options', 'black', 'light gray'),
    ('selected', 'white', 'dark blue')]
focus_map = {
    'heading': 'focus heading',
    'options': 'focus options',
    'line': 'focus line'}

pm = PropertyManager("Domains/domains.properties")

jbossHome = pm.getValue("jboss.home")
controller = pm.getValue("controller")
user = pm.getValue("user")
password = pm.getValue("password")

txt = urwid.Text(('banner', u" JBoss EAP 6 Script collection "), align='center')
map1 = urwid.AttrMap(txt, 'streak')
fill = urwid.Filler(map1, 'top')
map2 = urwid.AttrMap(fill, 'bg')



top = HorizontalBoxes()
top.open_box(menu_top.menu)
frame = urwid.Frame(header=txt,body=urwid.Filler(top, 'middle', 10))

loop = urwid.MainLoop(frame, palette, unhandled_input=exit_on_q)
loop.run()
