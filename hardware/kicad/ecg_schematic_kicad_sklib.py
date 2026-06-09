from collections import defaultdict
from skidl import Pin, Part, Alias, SchLib, SKIDL, TEMPLATE

from skidl.pin import pin_types

SKIDL_lib_version = '0.0.1'

ecg_schematic_kicad = SchLib(tool=SKIDL).add_parts(*[
        Part(**{ 'name':'C', 'dest':TEMPLATE, 'tool':SKIDL, 'aliases':Alias({'C'}), 'ref_prefix':'C', 'fplist':None, 'footprint':'ecg_kicad:C0805', 'keywords':None, 'description':'', 'datasheet':None, 'pins':[
            Pin(num='1',name='P',func=pin_types.PASSIVE),
            Pin(num='2',name='N',func=pin_types.PASSIVE)] }),
        Part(**{ 'name':'R', 'dest':TEMPLATE, 'tool':SKIDL, 'aliases':Alias({'R'}), 'ref_prefix':'R', 'fplist':None, 'footprint':'ecg_kicad:R0603', 'keywords':None, 'description':'', 'datasheet':None, 'pins':[
            Pin(num='1',name='P',func=pin_types.PASSIVE),
            Pin(num='2',name='N',func=pin_types.PASSIVE)] }),
        Part(**{ 'name':'PJ320A', 'dest':TEMPLATE, 'tool':SKIDL, 'aliases':Alias({'PJ320A'}), 'ref_prefix':'J', 'fplist':None, 'footprint':'ecg_kicad:AUDIO-TH_PJ-320A_C49284721', 'keywords':None, 'description':'', 'datasheet':None, 'pins':[
            Pin(num='1',name='T',func=pin_types.PASSIVE),
            Pin(num='2',name='R1',func=pin_types.PASSIVE),
            Pin(num='3',name='S',func=pin_types.PASSIVE)] }),
        Part(**{ 'name':'Conn1x9', 'dest':TEMPLATE, 'tool':SKIDL, 'aliases':Alias({'Conn1x9'}), 'ref_prefix':'J', 'fplist':None, 'footprint':'ecg_kicad:HDR-TH_40P-P2.54-V-M-1', 'keywords':None, 'description':'', 'datasheet':None, 'pins':[
            Pin(num='1',name='P1',func=pin_types.PASSIVE),
            Pin(num='2',name='P2',func=pin_types.PASSIVE),
            Pin(num='3',name='P3',func=pin_types.PASSIVE),
            Pin(num='4',name='P4',func=pin_types.PASSIVE),
            Pin(num='5',name='P5',func=pin_types.PASSIVE),
            Pin(num='6',name='P6',func=pin_types.PASSIVE),
            Pin(num='7',name='P7',func=pin_types.PASSIVE),
            Pin(num='8',name='P8',func=pin_types.PASSIVE),
            Pin(num='9',name='P9',func=pin_types.PASSIVE)] }),
        Part(**{ 'name':'AD8232ACPZ-R7', 'dest':TEMPLATE, 'tool':SKIDL, 'aliases':Alias({'AD8232ACPZ-R7'}), 'ref_prefix':'U', 'fplist':None, 'footprint':'ecg_kicad:LFCSP-20_L4.0-W4.0-P0.50-TL-EP2.7', 'keywords':None, 'description':'', 'datasheet':None, 'pins':[
            Pin(num='1',name='HPDRIVE',func=pin_types.BIDIR),
            Pin(num='2',name='+IN',func=pin_types.INPUT),
            Pin(num='3',name='-IN',func=pin_types.INPUT),
            Pin(num='4',name='RLDFB',func=pin_types.INPUT),
            Pin(num='5',name='RLD',func=pin_types.OUTPUT),
            Pin(num='6',name='SW',func=pin_types.BIDIR),
            Pin(num='7',name='OPAMP+',func=pin_types.INPUT),
            Pin(num='8',name='REFOUT',func=pin_types.OUTPUT),
            Pin(num='9',name='OPAMP-',func=pin_types.INPUT),
            Pin(num='10',name='OUT',func=pin_types.OUTPUT),
            Pin(num='11',name='LOD-',func=pin_types.OUTPUT),
            Pin(num='12',name='LOD+',func=pin_types.OUTPUT),
            Pin(num='13',name='SDN#',func=pin_types.INPUT),
            Pin(num='14',name='AC/DC#',func=pin_types.INPUT),
            Pin(num='15',name='FR',func=pin_types.INPUT),
            Pin(num='16',name='+VS',func=pin_types.PWRIN),
            Pin(num='17',name='REFIN',func=pin_types.INPUT),
            Pin(num='18',name='IAOUT',func=pin_types.OUTPUT),
            Pin(num='19',name='HPSENSE',func=pin_types.INPUT),
            Pin(num='20',name='EP',func=pin_types.PWRIN),
            Pin(num='21',name='GND',func=pin_types.PWRIN)] })])