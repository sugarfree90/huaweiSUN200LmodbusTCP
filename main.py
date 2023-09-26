# requires huawei-solar-v1 library to connect to the inverter
# i repeat, huawei-solar-v1, not current version
# class dataItem refreshes the values according to the config in initialization function
# updateInterval - how often to read the value
# updateInChange - update if new value is different from previous
# meanValue - send mean value calculated from values recorded since last reading
# tested and developed on SUN2000-6KTL-M0 software version V100R001C00SPC153

import huawei_solar
import time
import statistics


# how often (in seconds) to read the values from inverter
dataRefreshTime = 5

dataList = [
    "reactive_power",
    "power_factor",
    "efficiency",
    "grid_frequency",
    "grid_voltage",
    "grid_current",
    "line_voltage_A_B",
    "line_voltage_B_C",
    "line_voltage_C_A",
    "phase_A_voltage",
    "phase_B_voltage",
    "phase_C_voltage",
    "phase_A_current",
    "phase_B_current",
    "phase_C_current",
    "input_power",
    "grid_exported_energy",
    "internal_temperature",
    "device_status",
    "daily_yield_energy",
    "active_power"
]

class dataItem():

    def __init__(self, name, updateInterval = 60, updateOnChange = False, meanValue = False):
        self.name = name
        self.updateInterval = updateInterval
        self.updateOnChange = updateOnChange
        self.previousValue = 0
        self.currentValue = 0
        self.lastUpdateTimestamp = 0
        self.meanValue = meanValue
        self.meanTable = []
    
    def refresh(self):
        if self.updateOnChange:
            tmpVal = inverter.get(self.name).value
            if tmpVal != self.currentValue or time.time() - self.lastUpdateTimestamp >= self.updateInterval:
                self.lastUpdateTimestamp = time.time()
                self.previousValue = self.currentValue
                self.currentValue = tmpVal
                print("refreshed by change "+self.name+" value: "+str(self.currentValue))
        else:
            if self.meanValue:
                self.meanTable.append(inverter.get(self.name).value)
                if time.time() - self.lastUpdateTimestamp >= self.updateInterval:
                    self.lastUpdateTimestamp = time.time()
                    self.previousValue = self.currentValue
                    self.currentValue = statistics.mean(self.meanTable)
                    self.meanTable = []
                    print("refreshed by time "+self.name+" mean value: "+str(self.currentValue))
            else:
                if time.time() - self.lastUpdateTimestamp >= self.updateInterval:
                    self.lastUpdateTimestamp = time.time()
                    self.previousValue = self.currentValue
                    self.currentValue = inverter.get(self.name).value
                    print("refreshed by time "+self.name+" value: "+str(self.currentValue))

dataTimer = 0

print(dir(inverter.get("reactive_power").value))
inverter = huawei_solar.HuaweiSolar('192.168.200.1', port=6607, slave=0)

itemList = []
itemList.append(dataItem("reactive_power", 120, False, True))
itemList.append(dataItem("power_factor", 120, False, True))
itemList.append(dataItem("efficiency", 60, False, True))
itemList.append(dataItem("grid_frequency", 120, False, True))
itemList.append(dataItem("grid_voltage", 60, False, True))
itemList.append(dataItem("grid_current", 60, False, True))
itemList.append(dataItem("line_voltage_A_B", 60, False, True))
itemList.append(dataItem("line_voltage_B_C", 60, False, True))
itemList.append(dataItem("line_voltage_C_A", 60, False, True))
itemList.append(dataItem("phase_A_voltage", 60, False, True))
itemList.append(dataItem("phase_B_voltage", 60, False, True))
itemList.append(dataItem("phase_C_voltage", 60, False, True))
itemList.append(dataItem("phase_A_current", 60, False, True))
itemList.append(dataItem("phase_B_current", 60, False, True))
itemList.append(dataItem("phase_C_current", 60, False, True))
itemList.append(dataItem("input_power", 60, False, True))
itemList.append(dataItem("grid_exported_energy", 60, False))
itemList.append(dataItem("internal_temperature", 60, False, True))
itemList.append(dataItem("device_status", 600, True))
itemList.append(dataItem("daily_yield_energy", 60, False))
itemList.append(dataItem("active_power", 600, True))


while True:
    time.sleep(0.1)
    if time.time() - dataTimer >= dataRefreshTime:
        for item in itemList:
            item.refresh()
