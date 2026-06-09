"""
ECG Biosensor Platform — KiCad Netlist Generator v3
Generates netlist directly without skidl to avoid duplicate component issues.
Shrimaan Rapuru | The Early College at Guilford | Summer 2026
"""

import datetime

netlist = '''<?xml version="1.0" encoding="UTF-8"?>
<export version="E">
  <design>
    <source>ecg_biosensor.net</source>
    <date>{date}</date>
    <tool>ECG Biosensor Python Generator v3</tool>
  </design>
  <components>
    <comp ref="U1">
      <value>AD8232ACPZ-R7</value>
      <footprint>ecg_kicad:LFCSP-20_L4.0-W4.0-P0.50-TL-EP2.7</footprint>
      <description>ECG Analog Front-End</description>
    </comp>
    <comp ref="C1">
      <value>100nF</value>
      <footprint>ecg_kicad:C0805</footprint>
      <description>VCC Decoupling Capacitor</description>
    </comp>
    <comp ref="C2">
      <value>100nF</value>
      <footprint>ecg_kicad:C0805</footprint>
      <description>VCC Decoupling Capacitor</description>
    </comp>
    <comp ref="C3">
      <value>10uF</value>
      <footprint>ecg_kicad:C0603</footprint>
      <description>Bulk Power Filter Capacitor</description>
    </comp>
    <comp ref="R1">
      <value>10k</value>
      <footprint>ecg_kicad:R0603</footprint>
      <description>Reference Voltage Divider Top</description>
    </comp>
    <comp ref="R2">
      <value>10k</value>
      <footprint>ecg_kicad:R0603</footprint>
      <description>Reference Voltage Divider Bottom</description>
    </comp>
    <comp ref="J1">
      <value>PJ-320A</value>
      <footprint>ecg_kicad:AUDIO-TH_PJ-320A_C49284721</footprint>
      <description>3.5mm Electrode Jack</description>
    </comp>
    <comp ref="J2">
      <value>Arduino_Header_1x9</value>
      <footprint>ecg_kicad:HDR-TH_40P-P2.54-V-M-1</footprint>
      <description>Arduino Connection Header</description>
    </comp>
  </components>
  <nets>
    <net code="1" name="VCC">
      <node ref="U1" pin="16"/>
      <node ref="U1" pin="20"/>
      <node ref="U1" pin="13"/>
      <node ref="C1" pin="1"/>
      <node ref="C2" pin="1"/>
      <node ref="C3" pin="1"/>
      <node ref="R1" pin="1"/>
      <node ref="J2" pin="1"/>
    </net>
    <net code="2" name="GND">
      <node ref="U1" pin="21"/>
      <node ref="U1" pin="14"/>
      <node ref="C1" pin="2"/>
      <node ref="C2" pin="2"/>
      <node ref="C3" pin="2"/>
      <node ref="R2" pin="2"/>
      <node ref="J2" pin="2"/>
    </net>
    <net code="3" name="ECG_INP">
      <node ref="U1" pin="2"/>
      <node ref="J1" pin="1"/>
    </net>
    <net code="4" name="ECG_INN">
      <node ref="U1" pin="3"/>
      <node ref="J1" pin="2"/>
    </net>
    <net code="5" name="RLD">
      <node ref="U1" pin="5"/>
      <node ref="U1" pin="4"/>
      <node ref="J1" pin="3"/>
    </net>
    <net code="6" name="ECG_OUT">
      <node ref="U1" pin="10"/>
      <node ref="J2" pin="3"/>
    </net>
    <net code="7" name="LO_PLUS">
      <node ref="U1" pin="12"/>
      <node ref="J2" pin="4"/>
    </net>
    <net code="8" name="LO_MINUS">
      <node ref="U1" pin="11"/>
      <node ref="J2" pin="5"/>
    </net>
    <net code="9" name="REFIN">
      <node ref="U1" pin="17"/>
      <node ref="R1" pin="2"/>
      <node ref="R2" pin="1"/>
    </net>
    <net code="10" name="REFOUT">
      <node ref="U1" pin="8"/>
    </net>
    <net code="11" name="IAOUT">
      <node ref="U1" pin="18"/>
    </net>
  </nets>
</export>
'''.format(date=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

with open('ecg_biosensor.net', 'w') as f:
    f.write(netlist)

print("SUCCESS: ecg_biosensor.net generated")
print()
print("Component list:")
print("  U1  AD8232ACPZ-R7        ECG analog front-end (LFCSP-20)")
print("  C1  100nF 0805           VCC decoupling")
print("  C2  100nF 0805           VCC decoupling")
print("  C3  10uF  0603           Bulk power filter")
print("  R1  10kOhm 0603          Reference divider top")
print("  R2  10kOhm 0603          Reference divider bottom")
print("  J1  PJ-320A              3.5mm electrode jack")
print("  J2  1x9 pin header       Arduino connection")
print()
print("Net list:")
print("  VCC      U1.16 U1.20 U1.13 C1.1 C2.1 C3.1 R1.1 J2.1")
print("  GND      U1.21 U1.14 C1.2 C2.2 C3.2 R2.2 J2.2")
print("  ECG_INP  U1.2 J1.1")
print("  ECG_INN  U1.3 J1.2")
print("  RLD      U1.5 U1.4 J1.3")
print("  ECG_OUT  U1.10 J2.3  (Arduino A0)")
print("  LO_PLUS  U1.12 J2.4  (Arduino D10)")
print("  LO_MINUS U1.11 J2.5  (Arduino D11)")
print("  REFIN    U1.17 R1.2 R2.1")
print()
print("Import into KiCad PCB Editor:")
print("  File -> Import -> Netlist -> ecg_biosensor.net -> Update PCB")