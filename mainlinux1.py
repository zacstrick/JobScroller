#JobScroller by Zac Strickland

#Scrolls through cleverly placed CSV files on a network drive and shows them to the world on a monitor you have hanging out on the shop floor
#V1.1 now sorts based on date line

import PySimpleGUI as sg
import csv
import os.path
from os import path
from itertools import cycle

##STATIC VARS##
pathe = '/mnt/Schedules/'

bigname = sg.popup_get_text("What department is this display for?\n5AXIS, 3AXIS, LATHE, or HORIZONTAL", default_text=('3AXIS'))

tickspeed = sg.popup_get_text("How fast do you want to change between machines?", default_text=(2))

machines = os.listdir(f'{pathe}{bigname}')

cycmach = cycle(machines)

def nextmach():
    return next(cycmach)


if bigname == None:
    exit()

if not path.exists(f'{pathe}{bigname}'):
    sg.popup_no_titlebar("I didn't find that one, try a different directory or check your connection.")
    exit()



def csvpruner(pathe, bigname, machine):
    with open(f'{pathe}{bigname}/{machine}', 'r') as csv_file:
        openedcsv = csv.reader(csv_file)
        next(openedcsv)
        return openedcsv


##COLUMN LAYOUTS##
jobno = [[sg.Text('Job Number', font=('arial', 12, 'bold'))], [sg.Text('', size=(20,60), key='jobno')]]
pono  = [[sg.Text('PO Number', font=('arial', 12, 'bold'))], [sg.Text('', size=(20,60), key='pono')]]
quan  = [[sg.Text('Quantity', font=('arial', 12, 'bold'))], [sg.Text('', size=(20,60), key='quan')]]
dued  = [[sg.Text('Due Date', font=('arial', 12, 'bold'))], [sg.Text('', size=(20,60), key='dued')]]
pano  = [[sg.Text('Part Number', font=('arial', 12, 'bold'))], [sg.Text('', size=(25,60), key='pano')]]
mat   = [[sg.Text('Material', font=('arial', 12, 'bold'))], [sg.Text('', size=(20,60), key='mat')]]
matloc = [[sg.Text('Material Location', font=('arial', 12, 'bold'))], [sg.Text('', size=(20,60), key='matloc')]]
esthrs = [[sg.Text('Estimated Hours', font=('arial', 12, 'bold'))], [sg.Text('', size=(20,60), key='esthrs')]]
veri  = [[sg.Text('Vericut Complete?', font=('arial', 12, 'bold'))], [sg.Text('', size=(20,60), key='veri')]]
tool  = [[sg.Text('Tools Ready?', font=('arial', 12, 'bold'))], [sg.Text('', size=(20,60), key='tool')]]


##MAIN LAYOUT##
layout = [ [sg.Text(f'{bigname}', font=('arial', 30, 'bold'))], [sg.Text(f'', key='MACH', size=(22,1), font=('arial', 22, 'bold'))], 
        [sg.Column(jobno, pad=(20,0)), sg.Column(pono, pad=(20,0)), sg.Column(quan, pad=(20,0)), sg.Column(dued, pad=(20,0)), sg.Column(pano, pad=(20,0), size=(250,600)), sg.Column(mat, pad=(20,0)), sg.Column(matloc), sg.Column(esthrs), sg.Column(veri, pad=(20,0)), sg.Column(tool, pad=(20,0))]]   

counter = 0

window = sg.Window(f'{bigname}', layout, size=(1920,1080))

while True:
    event, values = window.Read(timeout=int(tickspeed)*1000, timeout_key='tick')

    if event == None:
        break

    elif event == 'tick':
        machy = nextmach()
        (lilname, ext) = os.path.splitext(machy)
        window['MACH'].Update(lilname)

        linelist = []
        jobnol = []
        ponol = []
        quanl = []
        duedl = []
        panol = []
        matl = []
        matlocl = []
        esthrsl = []
        veril = []
        tooll = []

        csv_file = open(f'{pathe}{bigname}/{machy}', 'r')
        openedcsv = csv.reader(csv_file)
        next(openedcsv)
        
        
        for line in openedcsv:
            linelist.append(line)
            

        linelist.sort(key=lambda x: x[3])

        for line in linelist:
            jobnol.append(line[0])
            ponol.append(line[1])
            quanl.append(line[2])
            duedl.append(line[3])
            panol.append(line[4])
            matl.append(line[5])
            matlocl.append(line[6])
            esthrsl.append(line[7])
            veril.append(line[8])
            tooll.append(line[9])

        jobnoln = '\n'.join(jobnol)
        ponoln = '\n'.join(ponol)
        quanln = '\n'.join(quanl)
        duedln = '\n'.join(duedl)
        panoln = '\n'.join(panol)
        matln = '\n'.join(matl)
        matlocln = '\n'.join(matlocl)
        esthrsln = '\n'.join(esthrsl)
        veriln = '\n'.join(veril)
        toolln = '\n'.join(tooll)

        window['jobno'].Update(jobnoln)
        window['pono'].Update(ponoln)
        window['quan'].Update(quanln)
        window['dued'].Update(duedln)
        window['pano'].Update(panoln)
        window['mat'].Update(matln)
        window['matloc'].Update(matlocln)
        window['esthrs'].Update(esthrsln)
        window['veri'].Update(veriln)
        window['tool'].Update(toolln)

        csv_file.close()


        
        

window.close()