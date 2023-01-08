from .const import PERUSB_SIGNAL, POS_DEVNAME, POS_PUDO, PERUSB_MODULE, SIGNAL_MAX_NUM, PERUSB_QUANTITY_UNIT, PERUSB_QUANTITY, ValIndex, ValIndexPM2
from enum import Enum

def data_line_convert(data_array: list[str], signal_number: int):
    ret_val = None
    if data_array[POS_DEVNAME] == "SE1-PM1":
        temp_hb_energy1 = int(data_array[POS_PUDO + 7]) % 16
        temp_hb_energy2 = int(data_array[POS_PUDO + 8]) % 16
        temp_hb_energy3 = int(data_array[POS_PUDO + 8]) / 16
        if signal_number == 7:
            ret_val = (
                              (temp_hb_energy3 * 100000000)
                              + int(data_array[POS_PUDO + 17])
                              + int(data_array[POS_PUDO + 18]) * 256
                              + int(data_array[POS_PUDO + 19]) * 65536
                              + int(data_array[POS_PUDO + 20]) * 16777216
                      ) / 1000 + (
                              (temp_hb_energy2 * 100000000)
                              + int(data_array[POS_PUDO + 13])
                              + int(data_array[POS_PUDO + 14]) * 256
                              + int(data_array[POS_PUDO + 15]) * 65536
                              + int(data_array[POS_PUDO + 16]) * 16777216
                      ) / 1000 + (
                              (temp_hb_energy1 * 100000000)
                              + int(data_array[POS_PUDO + 9])
                              + int(data_array[POS_PUDO + 10]) * 256
                              + int(data_array[POS_PUDO + 11]) * 65536
                              + int(data_array[POS_PUDO + 12]) * 16777216
                      ) / 1000
        elif signal_number == 6:
            ret_val = (int(data_array[POS_PUDO + 5]) + int(data_array[POS_PUDO + 6]) * 256) / 1000 + (
                        int(data_array[POS_PUDO + 3]) + int(data_array[POS_PUDO + 4]) * 256) / 1000 + (
                                  int(data_array[POS_PUDO + 1]) + int(data_array[POS_PUDO + 2]) * 256) / 1000
        elif signal_number == 5:
            ret_val = (
                              (temp_hb_energy3 * 100000000)
                              + int(data_array[POS_PUDO + 17])
                              + int(data_array[POS_PUDO + 18]) * 256
                              + int(data_array[POS_PUDO + 19]) * 65536
                              + int(data_array[POS_PUDO + 20]) * 16777216
                      ) / 1000
        elif signal_number == 4:
            ret_val = (
                              (temp_hb_energy2 * 100000000)
                              + int(data_array[POS_PUDO + 13])
                              + int(data_array[POS_PUDO + 14]) * 256
                              + int(data_array[POS_PUDO + 15]) * 65536
                              + int(data_array[POS_PUDO + 16]) * 16777216
                      ) / 1000
        elif signal_number == 3:
            ret_val = (
                              (temp_hb_energy1 * 100000000)
                              + int(data_array[POS_PUDO + 9])
                              + int(data_array[POS_PUDO + 11]) * 65536
                              + int(data_array[POS_PUDO + 12]) * 16777216
                      ) / 1000
        elif signal_number == 2:
            ret_val = (int(data_array[POS_PUDO + 5]) + int(data_array[POS_PUDO + 6]) * 256) / 1000
        elif signal_number == 1:
            ret_val = (int(data_array[POS_PUDO + 3]) + int(data_array[POS_PUDO + 4]) * 256) / 1000
        elif signal_number == 0:
            ret_val = (int(data_array[POS_PUDO + 1]) + int(data_array[POS_PUDO + 2]) * 256) / 1000
        return ret_val

    elif data_array[POS_DEVNAME] == "SE1-PM2":

        if signal_number == 12:
            ret_val = (int(data_array[POS_PUDO + 29]) +
                       int(data_array[POS_PUDO + 30]) * 256 +
                       int(data_array[POS_PUDO + 31]) * 65536 +
                       int(data_array[POS_PUDO + 32]) * 16777216) / 1000 + (int(data_array[POS_PUDO + 25]) +
                                                                            int(data_array[POS_PUDO + 26]) * 256 +
                                                                            int(data_array[POS_PUDO + 27]) * 65536 +
                                                                            int(data_array[
                                                                                    POS_PUDO + 28]) * 16777216) / 1000 + (
                                  int(data_array[POS_PUDO + 21]) +
                                  int(data_array[POS_PUDO + 22]) * 256 +
                                  int(data_array[POS_PUDO + 23]) * 65536 +
                                  int(data_array[POS_PUDO + 24]) * 16777216) / 1000
        elif signal_number == 11:
            ret_val = (int(data_array[POS_PUDO + 16]) +
                       int(data_array[POS_PUDO + 17]) * 256 +
                       int(data_array[POS_PUDO + 18]) * 65536 +
                       int(data_array[POS_PUDO + 19]) * 16777216) / 1000 + (int(data_array[POS_PUDO + 12]) +
                                                                            int(data_array[POS_PUDO + 13]) * 256 +
                                                                            int(data_array[POS_PUDO + 14]) * 65536 +
                                                                            int(data_array[
                                                                                    POS_PUDO + 15]) * 16777216) / 1000 + (
                                  int(data_array[POS_PUDO + 8]) +
                                  int(data_array[POS_PUDO + 9]) * 256 +
                                  int(data_array[POS_PUDO + 10]) * 65536 +
                                  int(data_array[POS_PUDO + 11]) * 16777216) / 1000
        elif signal_number == 10:
            ret_val = (int(data_array[POS_PUDO + 5]) +
                       int(data_array[POS_PUDO + 6]) * 256) / 1000 + (int(data_array[POS_PUDO + 3]) +
                                                                      int(data_array[POS_PUDO + 4]) * 256) / 1000 + (
                                  int(data_array[POS_PUDO + 1]) +
                                  int(data_array[POS_PUDO + 2]) * 256) / 1000
        elif signal_number == 9:
            ret_val = int(data_array[POS_PUDO + 33])
        elif signal_number == 8:
            ret_val = (int(data_array[POS_PUDO + 29]) +
                       int(data_array[POS_PUDO + 30]) * 256 +
                       int(data_array[POS_PUDO + 31]) * 65536 +
                       int(data_array[POS_PUDO + 32]) * 16777216) / 1000
        elif signal_number == 7:
            ret_val = (int(data_array[POS_PUDO + 25]) +
                       int(data_array[POS_PUDO + 26]) * 256 +
                       int(data_array[POS_PUDO + 27]) * 65536 +
                       int(data_array[POS_PUDO + 28]) * 16777216) / 1000
        elif signal_number == 6:
            ret_val = (int(data_array[POS_PUDO + 21]) +
                       int(data_array[POS_PUDO + 22]) * 256 +
                       int(data_array[POS_PUDO + 23]) * 65536 +
                       int(data_array[POS_PUDO + 24]) * 16777216) / 1000
        elif signal_number == 5:
            ret_val = (int(data_array[POS_PUDO + 16]) +
                       int(data_array[POS_PUDO + 17]) * 256 +
                       int(data_array[POS_PUDO + 18]) * 65536 +
                       int(data_array[POS_PUDO + 19]) * 16777216) / 1000
        elif signal_number == 4:
            ret_val = (int(data_array[POS_PUDO + 12]) +
                       int(data_array[POS_PUDO + 13]) * 256 +
                       int(data_array[POS_PUDO + 14]) * 65536 +
                       int(data_array[POS_PUDO + 15]) * 16777216) / 1000
        elif signal_number == 3:
            ret_val = (int(data_array[POS_PUDO + 8]) +
                       int(data_array[POS_PUDO + 9]) * 256 +
                       int(data_array[POS_PUDO + 10]) * 65536 +
                       int(data_array[POS_PUDO + 11]) * 16777216) / 1000
        elif signal_number == 2:
            ret_val = (int(data_array[POS_PUDO + 5]) + int(data_array[POS_PUDO + 6]) * 256) / 1000
        elif signal_number == 1:
            ret_val = (int(data_array[POS_PUDO + 3]) + int(data_array[POS_PUDO + 4]) * 256) / 1000
        else:
            ret_val = (int(data_array[POS_PUDO + 1]) + int(data_array[POS_PUDO + 2]) * 256) / 1000
        return ret_val

    elif data_array[POS_DEVNAME] == "SE1-PM3":
        temp_hb_energy1 = int(data_array[POS_PUDO + 7]) % 16
        temp_hb_energy2 = int(data_array[POS_PUDO + 8]) % 16
        temp_hb_energy3 = int(data_array[POS_PUDO + 8]) / 16
        if signal_number == 7:
            ret_val = (
                              (temp_hb_energy3 * 100000000)
                              + int(data_array[POS_PUDO + 17])
                              + int(data_array[POS_PUDO + 18]) * 256
                              + int(data_array[POS_PUDO + 19]) * 65536
                              + int(data_array[POS_PUDO + 20]) * 16777216
                      ) / 10000 + (
                              (temp_hb_energy2 * 100000000)
                              + int(data_array[POS_PUDO + 13])
                              + int(data_array[POS_PUDO + 14]) * 256
                              + int(data_array[POS_PUDO + 15]) * 65536
                              + int(data_array[POS_PUDO + 16]) * 16777216
                      ) / 10000 + (
                              (temp_hb_energy1 * 100000000)
                              + int(data_array[POS_PUDO + 9])
                              + int(data_array[POS_PUDO + 10]) * 256
                              + int(data_array[POS_PUDO + 11]) * 65536
                              + int(data_array[POS_PUDO + 12]) * 16777216
                      ) / 10000
        elif signal_number == 6:
            ret_val = (int(data_array[POS_PUDO + 5]) + int(data_array[POS_PUDO + 6]) * 256) / 10 + (
                        int(data_array[POS_PUDO + 3]) + int(data_array[POS_PUDO + 4]) * 256) / 10 + (
                                  int(data_array[POS_PUDO + 1]) + int(data_array[POS_PUDO + 2]) * 256) / 10
        elif signal_number == 5:
            ret_val = (
                              (temp_hb_energy3 * 100000000)
                              + int(data_array[POS_PUDO + 17])
                              + int(data_array[POS_PUDO + 18]) * 256
                              + int(data_array[POS_PUDO + 19]) * 65536
                              + int(data_array[POS_PUDO + 20]) * 16777216
                      ) / 10000
        elif signal_number == 4:
            ret_val = (
                              (temp_hb_energy2 * 100000000)
                              + int(data_array[POS_PUDO + 13])
                              + int(data_array[POS_PUDO + 14]) * 256
                              + int(data_array[POS_PUDO + 15]) * 65536
                              + int(data_array[POS_PUDO + 16]) * 16777216
                      ) / 10000
        elif signal_number == 3:
            ret_val = (
                              (temp_hb_energy1 * 100000000)
                              + int(data_array[POS_PUDO + 9])
                              + int(data_array[POS_PUDO + 11]) * 65536
                              + int(data_array[POS_PUDO + 12]) * 16777216
                      ) / 10000
        elif signal_number == 2:
            ret_val = (int(data_array[POS_PUDO + 5]) + int(data_array[POS_PUDO + 6]) * 256) / 10
        elif signal_number == 1:
            ret_val = (int(data_array[POS_PUDO + 3]) + int(data_array[POS_PUDO + 4]) * 256) / 10
        elif signal_number == 0:
            ret_val = (int(data_array[POS_PUDO + 1]) + int(data_array[POS_PUDO + 2]) * 256) / 10
        return ret_val


class Unit(str):
    kW = "kW"
    kWh = "kWh"
    Wh = "Wh"
    W = "W"


def get_meta(device_name: str) -> tuple[list[str], list[Unit]]:
    SINAL_NAMES = []
    SINAL_UNITS = []
    index_module = PERUSB_MODULE.index(device_name)
    if index_module == -1:
        raise ValueError("Unknown device type: " + device_name)

#    //signal_number_max = 8
    signal_number_max = PERUSB_SIGNAL[2*index_module]-1;

    for i in range(signal_number_max):
        SINAL_NAMES.append(PERUSB_QUANTITY[index_module * SIGNAL_MAX_NUM + i])
        SINAL_UNITS.append(PERUSB_QUANTITY_UNIT[index_module * SIGNAL_MAX_NUM + i])

    return SINAL_NAMES, SINAL_UNITS


def convert_units(value: float, unit: Unit) -> float:
    if unit in [Unit.Wh, Unit.W]:
        return value
    elif unit in [Unit.kW, Unit.kWh]:
        return value * 1000


def get_device_attrs(device_name: str) -> list(Enum):
    if device_name == "SE1-PM1":
        return [
            ValIndex.ENERGY1,
            ValIndex.ENERGY2,
            ValIndex.ENERGY3,
            ValIndex.POWER1,
            ValIndex.POWER2,
            ValIndex.POWER3,
            ValIndex.TOTAL_ENERGY,
            ValIndex.TOTAL_POWER
        ]
    if device_name == "SE1-PM2":
        return [
            ValIndexPM2.ENERGY1T1,
            ValIndexPM2.ENERGY2T1,
            ValIndexPM2.ENERGY3T1,
            ValIndexPM2.TOTAL_ENERGYT1,
            ValIndexPM2.POWER1,
            ValIndexPM2.POWER2,
            ValIndexPM2.POWER3,
            ValIndexPM2.TOTAL_POWER
        ]
    return []