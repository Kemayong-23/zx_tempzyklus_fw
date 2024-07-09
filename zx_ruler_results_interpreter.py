"""
This module defines function to interpret the ZX result
CEK
Created: 31.07.2023
Last modify: 01.09.2023
"""


def twos_complement_hex_to_signed_int(hex_string, number_of_bits):
    """
    This function converts a hex string to a signed int with two complement method
    :param hex_string: Hex value in string
    :param number_of_bits: Number of bit
    :return: signed int value
    """
    # Convert the hex string to integer
    signed_int_value = int(hex_string, base=16)
    # print(signed_int_value)

    # Check if the bit far left (number_of_bits - 1) is set
    if signed_int_value & (1 << (number_of_bits - 1)):
        # if set, subtract the maximum (2^(number_of_bits))
        signed_int_value -= 1 << number_of_bits
    return signed_int_value


def convert_ld_temp_in_deg(ld_temp):
    """
    Convert the Temperature of the GET_LD_TEMP from hex in deg
    :param ld_temp: ld temp hex code
    :return: NONE
    """

    # Set the return value
    temp_ntc_deg_value_string = "CRC Error"

    if "\x00" in ld_temp:
        # Set the return value to wrong Hex value
        temp_ntc_deg_value_string = "Wrong Hex value"

    else:
        if len(ld_temp) > 6:

            # Get the ntc temp hex value
            temp_ntc_hex_value = ld_temp[2:6]
            # Convert the ntc temp from hex to deg
            temp_ntc_deg_value = twos_complement_hex_to_signed_int(temp_ntc_hex_value, 16) / 100
            # make the string line for with the converted value
            temp_ntc_deg_value_string = str(round(temp_ntc_deg_value, 2))
            # temp_ntc_deg_value_string_with_comma = ",".join(temp_ntc_deg_value_string.split("."))
            # print(temp_ntc_deg_value_string_with_comma)

    # Return the string line
    return temp_ntc_deg_value_string


def get_errors_and_warnings_from_status_response(status_response):
    """
    This function get the errors and warnings from the status response
    :param status_response: Status response
    :return:
    """
    # List to store the errors
    errors_in_response = []
    # List to store the warnings
    warnings_in_response = []
    # List to store the errors and warnings
    errors_and_warnings = []

    # Dictionary (key:value) with errors
    error_dict = {0: "ERROR_FLASH_CHECK",
                  1: "ERROR_EEPROM_CHECK",
                  2: "ERROR_RAM_CHECK",
                  3: "ERROR_BOOT_CHECK",
                  4: "ERROR_WRONG_VIN_VOLTAGE",
                  5: "ERROR_VLD_LEVEL_CHECK",
                  6: "ERROR_SYNCRONISATION_CHECK",
                  7: "ERROR_COMPARATOR_CHECK",
                  8: "ERROR_VIN_OUT_OF_RANGE",
                  9: "ERROR_TWI_ERROR",
                  10: "ERROR_UART_ERROR",
                  11: "ERROR_HEARBEAT_MISSING",
                  12: "ERROR_MISSING_CALIB",
                  13: "ERROR_OVER_CURRENT",
                  14: "ERROR_UNDER_CURRENT",
                  15: "ERROR_LD_NTC_PROBLEM",
                  16: "ERROR_LD_OVERTEMP",
                  17: "ERROR_LD_UNDERTEMP",
                  18: "ERROR_MEMORY_FAIL",
                  19: "ERROR_EXTRAPOLATION_RANGE",
                  20: "ERROR_P_SET",
                  21: "ERROR_CALIBRATION_TABLE",
                  22: "ERROR_TABLE_INDICES_FAIL",
                  23: "ERROR_OPERATION_CURRENT_FAIL",
                  24: "ERROR_INTERPOLATION_TABLE",
                  25: "ERROR_SMCU_CALIBRATION",
                  26: "ERROR_PERIPHERAL_CHECK",
                  27: "ERROR_CMD_EXECUTION",
                  28: "ERROR_BYPASS_TRANSISTOR",
                  29: "ERROR_WRONG_LASER_HEAD"}

    # Dictionary (key:value) with warnings
    warning_dict = {0: "WARNING_LD_NTC_PROBLEM",
                    1: "WARNING_LD_OVERTEMP",
                    2: "WARNING_LD_UNDERTEMP",
                    3: "WARNING_LD_SMALL_POWER_FACTOR",
                    4: "WARNING_LD_BIG_POWER_FACTOR",
                    5: "WARNING_CANT_SET_POWER_FACTOR",
                    6: "WARNING_WRONG_COMMAND",
                    7: "WARNING_COMMAND_VALUE_OOR",
                    8: "WARNING_ACCESS_VIOLATION",
                    9: "WARNING_CAN_NOT_SET_RUNNING_MODE",
                    10: "WARNING_OVER_24_HOURS_ONTIME",
                    11: "WARNING_EXTRAPOLATION",
                    12: "WARNING_CAL_T_MIN_MAX_LIMIT",
                    13: "WARNING_END_OF_LIFE"}

    # Set the return value
    errors_and_warnings_as_string = "CRC Error"

    if "\x00" in status_response:
        # Set the return value to wrong Hex value
        errors_and_warnings_as_string = "Wrong Hex value"

    else:
        # Check if valid status response
        if len(status_response) > 6:

            # Get the error code from the status response
            error_code = status_response[4:12]

            # Check if no errors (protect against empty lines)
            if str(error_code).count('0') == len(error_code):

                errors_in_response.append("No Errors")

            else:

                # Convert the error code from hex to int
                error_code_int = int(error_code, base=16)

                # Convert from int to bin then str
                error_code_bin_string = str(bin(error_code_int))

                # Convert each single character as element of a list
                error_code_bin_string_list = []
                for character in error_code_bin_string:
                    error_code_bin_string_list.append(character)

                # remove the preceding "0b"
                error_code_bin_string_list = error_code_bin_string_list[2:]

                # Reverse the order of the elements in the list before interation
                error_code_bin_string_list.reverse()

                # Search the high bits and get the corresponding errors from the dict
                for error_key, error_bit_str in enumerate(error_code_bin_string_list):
                    if error_bit_str == "1":
                        errors_in_response.append(error_dict.get(error_key))

            errors_in_response_as_string = " | ".join(errors_in_response)
            # Add the error list to the error and warnings list
            errors_and_warnings.append(errors_in_response_as_string)

            # Get the warning code from the status response
            warning_code = status_response[12:20]

            # Check if no warnings
            if warning_code.count('0') == len(warning_code):
                warnings_in_response.append("No Warnings")

            else:
                # Convert the warning code from hex to int
                warning_code_int = int(warning_code, base=16)

                # Convert from int to bin then str
                warning_code_bin_string = str(bin(warning_code_int))

                # Convert each single character as element of a list
                warning_code_bin_string_list = []
                for character in warning_code_bin_string:
                    warning_code_bin_string_list.append(character)

                # remove the preceding "0b"
                warning_code_bin_string_list = warning_code_bin_string_list[2:]

                # Reverse the order of the elements in the list before interation
                warning_code_bin_string_list.reverse()

                # Search the high bits and get the corresponding warnings from the dict
                for warning_key, warning_bit_str in enumerate(warning_code_bin_string_list):
                    if warning_bit_str == "1":
                        warnings_in_response.append(warning_dict.get(warning_key))

            warnings_in_response_as_string = " | ".join(warnings_in_response)
            # Add the warning to the error and warnings list
            errors_and_warnings.append(warnings_in_response_as_string)

            # Errors and Warning as string
            errors_and_warnings_as_string = " | ".join(errors_and_warnings)

    # Return errors and warnings
    return errors_and_warnings_as_string


def get_laser_on_or_off(laser_status_response):
    """
    Give the status of the GET_LASER_ON_OFF: if ON or OFF
    :param laser_status_response: path of the file with LD_TEMP in Hex
    :return: Returns a string representing the laser status
    """

    # Set the return value
    laser_on_off_block = "CRC Error"

    if "\x00" in laser_status_response:
        # Set the return value to wrong Hex value
        laser_on_off_block = "Wrong Hex value"

    else:
        # Check if valid status response
        if len(laser_status_response) > 6:

            # Get the code from the status response
            value_block = laser_status_response[2:4]
            # Convert the value bloch as string
            value_block_as_int = int(value_block, base=16)

            if value_block_as_int != 0:
                laser_on_off_block = "ON"
            else:
                laser_on_off_block = "OFF"

    return laser_on_off_block


def interpret_get_smcu_status(smcu_status):
    """
    This function interprets the hex code of GET_SMCU_STATUS
    :param smcu_status: Status of the SMCU in Hex code
    :return:
    """

    # Parameter to calculate the ADC LD_TEMP
    u_ref = 2.06  # [V] Reference voltage
    dac_max = 65535  # [-] DAC max value for 16 bits (2^16 = 65535)

    # List to store the interpretation of each single blocks
    smcu_status_interpreted_as_list = []

    # Define some dictionaries

    # Dictionary (key:value) with start up states
    start_up_states_dict = {"10": "STARTUP_TESTS_ONGOING",
                            "20": "STARTUP_TESTS_FINISHED",
                            "30": "STARTUP_COMP_TEST_FINISHED",
                            "40": "STARTUP_COMP_READY"}

    # Dictionary (key:value) with operation state
    operation_states_dict = {"00": "OP_STAT_STARTUP_IDLE",
                             "01": "OP_STAT_STARTUP_USERCOMM_SELECTED",
                             "02": "OP_STAT_STARTUP_WAIT_FOR_SMCU",
                             "03": "OP_STAT_STARTUP_TEST_FIRST_OPV_VALUE",
                             "04": "OP_STAT_STARTUP_TEST_SECOND_OPV_VALUE",
                             "10": "OP_STAT_STANDBY",
                             "20": "OP_STAT_READY_OPERATION",
                             "28": "OP_STAT_USER_SERVICE",
                             "40": "OP_STAT_FACTORY_SERVICE",
                             "60": "OP_STAT_LD_TEST",
                             "80": "OP_STAT_FAILURE"}

    # Set the return value
    smcu_status_interpreted_as_string = "CRC Error"

    if "\x00" in smcu_status:
        # Set the return value to wrong Hex value
        smcu_status_interpreted_as_string = "Wrong Hex value"

    else:
        # Check if valid SMCU status
        if len(smcu_status) > 6:

            # Get code values

            # Get the start-up state in Hex
            start_up_state_hex = smcu_status[2:4]
            # Get the corresponding string value for the start-up state
            start_up_state_string = start_up_states_dict.get(start_up_state_hex)
            # Add to the interpretation list
            smcu_status_interpreted_as_list.append(start_up_state_string)
            # print(start_up_state_hex)

            # Get the operation states in hex
            operation_state_hex = smcu_status[4:6]
            # Convert to int
            # operation_state_int = int(operation_state_hex, base=16)
            # Get the corresponding operation state as string from the dictionary
            operation_state_string = operation_states_dict.get(operation_state_hex, str(operation_state_hex)
                                                               + ": Not existing")
            # Add to the interpretation list
            smcu_status_interpreted_as_list.append(operation_state_string)
            # print(operation_state_hex)

            # Get the ld_temp1 in Hex
            ntc_temp_hex = smcu_status[6:10]
            # Convert the ld_temp1 in decimal
            ntc_temp_decimal = int(ntc_temp_hex, base=16)
            # Calculate the adc LD_TEMP1 in V
            dac_ld_temp = u_ref * (ntc_temp_decimal / dac_max)
            # make the string line for the list with interpretation
            dac_ld_temp_string = f"{round(dac_ld_temp, 2)} V"
            # Add to the interpretation list
            smcu_status_interpreted_as_list.append(str(dac_ld_temp_string))

            # Get the si temp in hex
            si_temp_hex = smcu_status[10:14]
            # convert the si temp to decimal
            si_temp_decimal = twos_complement_hex_to_signed_int(si_temp_hex, 16) / 100
            # make the string line for the list with interpretation
            si_temp_decimal_string = f"{round(si_temp_decimal, 2)} degC"
            # Add to the interpretation list
            smcu_status_interpreted_as_list.append(str(si_temp_decimal_string))
            # print(smcu_status_interpreted_as_list)

            # Join the elements of the interpretation list in a single string line
            smcu_status_interpreted_as_string = " | ".join(smcu_status_interpreted_as_list)

    # Return a single string line with the interpretation results
    return smcu_status_interpreted_as_string


def convert_temp_adc_in_deg(temp_adc):

    """
    Convert the Temperature of the GET_TEMP_ADC from hex in deg
    :param temp_adc: ld temp hex code
    :return: NONE
    """

    # Set the return value
    temp_adc_deg_value_string = "CRC Error"

    # Check if the character NUL = \x00 is contained in the Hex value
    if "\x00" in temp_adc:
        # Set the return value to wrong Hex value
        temp_adc_deg_value_string = "Wrong Hex value"

    else:

        if len(temp_adc) > 6:

            # Get the temp adc hex value
            temp_adc_hex_value = temp_adc[2:6]
            # Convert the temp adc from hex to deg
            # print(temp_adc_hex_value)

            temp_adc_deg_value = int(temp_adc_hex_value, 16) / 100
            # print(temp_adc_deg_value)
            # make the string line for with the converted value
            temp_adc_deg_value_string = f"{round(temp_adc_deg_value, 2)}mV"

    # Return the string line
    return temp_adc_deg_value_string


def convert_current(current):
    """
    Convert the Temperature of the GET_CURRENT from hex in deg
    :param current: current hex code
    :return: LD_CURRENT_as_string
    """

    # Se the return value
    current_as_string = "CRC Error"

    # Check if the character NUL = \x00 is contained in the Hex value
    if "\x00" in current:
        # Set the return value to wrong Hex value
        current_as_string = "Wrong Hex value"

    else:
        if len(current) > 6:

            # Get the ld_current value
            current_value = current[2:6]
            # Convert the ld_current from hex to deg
            current_as_decimal = int(current_value, base=16)
            # print(current_as_decimal)
            # make the string line for with the converted value
            current_as_string = f"{round(current_as_decimal, 2)} mA"

    # Return the string line
    return current_as_string


def convert_status_byte(status_resp):
    """
    Converts the status of the GET_STATUS from hex code in to the corresponding string
    :param status_resp: Response with the status hex code
    :return: A String corresponding to the hex Code
    """
    # Lists to store the interpretation of each single blocks
    status_byte_response = []
    status_byte_as_bin_string_list = []

    # Dictionary (key:value) with Status Byte
    status_dict = {0: "STATUS_BUSY",
                   1: "STATUS_CRC_ERROR",
                   2: "STATUS_PASSWORD_ERROR",
                   3: "STATUS_TELEGRAM_ERROR",
                   4: "STATUS_WARNING",
                   5: "STATUS_ERROR",
                   6: "STATUS_PASSWORD_SET",
                   7: "STATUS_NO_DATA"}

    # Get the status byte from the status response
    status_byte = status_resp[:2]
    # print(type(status_byte))
    # print(status_byte)

    # Set the return value
    status_byte_as_string = ""

    # Check if the Hex contain NUL = \x00
    if "\x00" in status_byte:
        # Set the return value to wrong Hex value
        status_byte_as_string = "Wrong Hex value"

    else:
        if status_byte == "":
            return "No Value"
        else:
            if status_byte != "00":

                status_byte_as_int = int(status_byte, base=16)
                # print(status_byte_as_int)

                status_bytes_as_bin_string = str(bin(status_byte_as_int))

                # Convert each single character of status_byte_as_string as element of a list
                for character in status_bytes_as_bin_string:
                    status_byte_as_bin_string_list.append(character)

                # Reverse the order of the elements in the list before interation
                status_byte_as_bin_string_list.reverse()
                # print("status byte as bin list reversed:", status_byte_as_bin_string_list)

                # remove "ob" at the End with 2 times pop
                status_byte_as_bin_string_list.pop()
                status_byte_as_bin_string_list.pop()

                # Search the high bits and get the corresponding status from the dict
                for status_key, status_bit_str in enumerate(status_byte_as_bin_string_list):
                    if status_bit_str == "1":
                        status_byte_response.append(status_dict.get(int(status_key)))

                status_byte_as_string = " | ".join(status_byte_response)

            else:
                status_byte_as_string = "STATUS_OK"

    return status_byte_as_string


def interpret_get_mode(mode):
    """
    This function interprets the hex code of GET_MODE
    :param mode: mode in Hex code
    :return:
    """

    # List to store the interpretation of each single blocks
    mode_as_bin_string_list = []
    mode_response = []

    # Define some dictionaries

    # Dictionary (key:value) with operation state
    mode_dict = {0: "external_dig_modulation_on",
                 1: "future_use_1",
                 2: "extern_analog_modulation_on",
                 3: "OVTMP_shutdown_on",
                 4: "fail_out_signalling_on",
                 5: "fail_in_GPIO_on",
                 6: "future_use_2",
                 7: "future_use_3"}

    # Set the return value
    mode_as_string = "CRC Error"

    if "\x00" in mode:
        # Set the return value to wrong Hex value
        mode_as_string = "Wrong Hex value"

    else:
        # Check if valid mode
        if len(mode) > 6:

            # Get the mode in Hex
            mode_hex = mode[2:4]
            # Get the mode in dezimal
            mode_as_int = int(mode_hex, base=16)
            # Get the mode as string
            mode_as_bin_string = str(bin(mode_as_int))

            # Convert each single character of mode_as_string as element of a list
            for character in mode_as_bin_string:
                mode_as_bin_string_list.append(character)

            # Reverse the order of the elements in the list before interation
            mode_as_bin_string_list.reverse()

            # remove "ob" at the End with 2 times pop
            mode_as_bin_string_list.pop()
            mode_as_bin_string_list.pop()

            # Search the high bits and get the corresponding status from the dict
            for mode_key, mode_str in enumerate(mode_as_bin_string_list):
                if mode_str == "1":
                    mode_response.append(mode_dict.get(int(mode_key)))

            mode_as_string = " | ".join(mode_response)

    return mode_as_string


def interpret_get_config_mode(config_mode):
    """
    This function interprets the hex code of GET_MODE
    :param config_mode: config_mode in Hex code
    :return:
    """

    # Set the return value
    config_mode_response = "CRC Error"

    # List to store the interpretation of each single blocks
    config_mode_as_list = []

    # Dictionary (key:value) with operation mode
    config_mode_dict = {0: "MODULATION_FAIL_OUT",
                        1: "MODULATION_FAIL_IN",
                        2: "RS232_COM_DIG_IN",
                        3: "TWI_COM_DIG_IN",
                        4: "RS232_COM_FAIL_IN",
                        5: "TWI_COM_FAIL_IN",
                        6: "RS232_COM_FAIL_OUT",
                        7: "TWI_COM_FAIL_OUT",
                        8: "ZX20S_AT_CONFIG",
                        9: "ZXS_OEM_CONFIG"}

    # Check if the character NUL = \x00 is contained in the Hex value
    if "\x00" in config_mode:
        # Set the return value to wrong Hex value
        config_mode_response = "Wrong Hex value"

    else:
        # Check if valid config_mode
        if len(config_mode) > 6:

            # Get the config_mode in Hex
            config_mode_hex = config_mode[2:4]
            # Convert to int
            config_mode_as_int = int(config_mode_hex, base=16)
            # Get the corresponding operation config_mode as string from the dictionary
            config_mode_string = config_mode_dict.get(config_mode_as_int)
            # Add to the interpretation list
            config_mode_as_list.append(config_mode_string)
            # Join the elements of the interpretation list in a single string line
            config_mode_response = " | ".join(config_mode_as_list)

    # Return a single string line with the interpretation results
    return config_mode_response


def interpret_get_fw_version(fw_version):
    """
    FW
    :param fw_version:
    :return: mmcu_fw_version, smcu_fw_version
    """

    # Set the return value
    fw_version_string = "CRC Error"

    if "\x00" in fw_version:
        # Set the return value to wrong Hex value
        fw_version_string = "Wrong Hex value"

    else:
        if len(fw_version) > 6:

            """ Conversion of MMCU FW Version"""
            # Get the hex value
            mmcu_fw_version_major_hex = fw_version[2:4]
            # Convert in decimal
            mmcu_fw_version_major_decimal = int(mmcu_fw_version_major_hex, base=16)
            mmcu_fw_version_major_string = str(round(mmcu_fw_version_major_decimal))

            # Get the hex value
            mmcu_fw_version_minor_hex = fw_version[4:6]
            # Convert in decimal
            mmcu_fw_version_minor_decimal = int(mmcu_fw_version_minor_hex, base=16)
            mmcu_fw_version_minor_string = str(round(mmcu_fw_version_minor_decimal))

            # Get the mmcu_fw_version hex value
            mmcu_fw_version_intern_hex = fw_version[6:8]
            # Convert the mmcu_fw_version in decimal
            mmcu_fw_version_intern_decimal = int(mmcu_fw_version_intern_hex, base=16)
            mmcu_fw_version_intern_string = str(round(mmcu_fw_version_intern_decimal))

            mmcu_fw_version_string = "MMCU:  " + mmcu_fw_version_major_string + "." + mmcu_fw_version_minor_string + \
                                     "." + mmcu_fw_version_intern_string

            """ Conversion of SMCU FW Version"""
            # Get the hex value
            smcu_fw_version_major_hex = fw_version[12:14]
            # Convert in decimal
            smcu_fw_version_major_decimal = int(smcu_fw_version_major_hex, base=16)
            smcu_fw_version_major_string = str(round(smcu_fw_version_major_decimal))

            # Get the hex value
            smcu_fw_version_minor_hex = fw_version[14:16]
            # Convert in decimal
            smcu_fw_version_minor_decimal = int(smcu_fw_version_minor_hex, base=16)
            smcu_fw_version_minor_string = str(round(smcu_fw_version_minor_decimal))

            # Get the hex value
            smcu_fw_version_intern_hex = fw_version[16:18]
            # Convert in decimal
            smcu_fw_version_intern_decimal = int(smcu_fw_version_intern_hex, base=16)
            smcu_fw_version_intern_string = str(round(smcu_fw_version_intern_decimal))

            smcu_fw_version_string = "SMCU:  " + smcu_fw_version_major_string + "." + smcu_fw_version_minor_string + \
                                     "." + smcu_fw_version_intern_string

            fw_version_string = " | ".join([mmcu_fw_version_string, smcu_fw_version_string])

    # Return the string line
    return fw_version_string


def convert_current_dac_adc(current_dac):
    """
    Convert the Temperature of the GET_CURRENT_DAC_ADC from hex in deg
    :param current_dac: current hex code
    :return: NONE
    """

    # Parameter to calculate the current DAC
    u_ref = 3.3  # [V] Reference voltage
    dac_max = 4096  # [-] DAC max value for 12 bits (2^12 = 4096)
    r_shunt = 4.8   # [Ohm] Shunt resistor (2,4  + 2,4)
    xr_opv = (3.3 / 8)  # 3,3k / 8k
    # adc_temp_as_list = []

    # Set the return value
    current_dac_as_string = "CRC Error"

    # Check if the Hex contain NUL = \x00
    if "\x00" in current_dac:
        # Set the return value to wrong Hex value
        current_dac_adc_as_string = "Wrong Hex value"

    else:
        if len(current_dac) > 6:

            # Get the current dac hex value
            current_dac_value = current_dac[2:6]
            # Convert the current dac from hex to deg
            current_dac_as_int = int(current_dac_value, 16)
            dac_temp2 = ((u_ref * xr_opv * (current_dac_as_int / dac_max)) / r_shunt) * 1000
            # make the string line for with the converted value [mA]
            current_dac_as_string = str(round(dac_temp2, 2))
            # print(current_dac_as_string)

    # Return the string line
    return current_dac_as_string


def convert_power_out_abs(power_out_abs):
    """
    power
    :param power_out_abs: power
    :return: power_out_abs_as_string
    """

    power_out_abs_string = "CRC Error"

    if len(power_out_abs) > 6:

        # Get the power_out_abs hex value
        power_out_abs_hex = power_out_abs[2:6]
        # Convert the power_out_abs in decimal
        power_out_abs_decimal = int(power_out_abs_hex, base=16) / 100

        power_out_abs_string = f"{round(power_out_abs_decimal)} mw"

        # Return the string line
    return power_out_abs_string


def convert_power_val_in_perc(power_val_in_perc):
    """
    power
    :param power_val_in_perc:
    :return: power_val_in_perc_string
    """

    power_val_in_perc_string = "CRC Error"

    # Check if the character NUL = \x00 is contained in the Hex value
    if "\x00" in power_val_in_perc:
        # Set the return value to wrong Hex value
        power_val_in_perc_string = "Wrong Hex value"

    else:
        if len(power_val_in_perc) > 6:

            # Get the power_val_in_perc hex value
            power_val_in_perc_hex = power_val_in_perc[2:4]
            # Convert the power_val_in_perc in decimal
            power_val_in_perc_decimal = int(power_val_in_perc_hex, base=16) / 100

            power_val_in_perc_string = f"{round(power_val_in_perc_decimal)}  "

            # Return the string line
    return power_val_in_perc_string


def convert_ld_lifetime(ld_lifetime):
    """
    :param ld_lifetime:
    :return: ld_lifetime_string
    """

    ld_lifetime_string = "CRC Error"

    if len(ld_lifetime) > 6:

        # Get the ld_lifetime hours hex value
        ld_lifetime_in_hour_hex = ld_lifetime[2:6]
        # Convert the ld_lifetime hours in decimal
        ld_lifetime_in_hour_decimal = int(ld_lifetime_in_hour_hex, base=16)

        ld_lifetime_in_hour_string = f"{round(ld_lifetime_in_hour_decimal)}h"

        # Get the ld_lifetime minutes hex value
        ld_lifetime_in_min_hex = ld_lifetime[6:8]
        # Convert the ld_lifetime minutes in decimal
        ld_lifetime_in_min_decimal = int(ld_lifetime_in_min_hex, base=16)

        ld_lifetime_in_min_string = f"{round(ld_lifetime_in_min_decimal)}min"

        ld_lifetime_string = " ".join([ld_lifetime_in_hour_string, ld_lifetime_in_min_string])

        # Return the string line
    return ld_lifetime_string


def convert_pd_value(pd_value):
    """
    :param pd_value:
    :return: pd_value_string
    """
    # Parameter to calculate the pd_value
    # u_ref = 2.06  # [V] Reference voltage
    # dac_max = 65535  # [-] DAC max value for 16 bits (2^16 = 65535)

    # Set the return value
    pd_value_string = "CRC Error"

    # Check if the Hex contain NUL = \x00
    if "\x00" in pd_value:
        # Set the return value to wrong Hex value
        pd_value_string = "Wrong Hex value"

    else:
        if len(pd_value) > 6:

            # Get the pd_value hex value
            pd_value_hex = pd_value[2:6]
            # Convert the pd_value in decimal
            # print(pd_value_hex)

            pd_value_decimal = int(pd_value_hex, base=16)
            # Calculate the adc LD_TEMP2 in mV
            # pd_value_dac = u_ref * (pd_value_decimal / dac_max)
            # print(pd_value_decimal)

            # [mV]
            pd_value_string = str(round(pd_value_decimal, 2))
            # print(pd_value_string)

            # Return the string line

    return pd_value_string


def convert_module_total_ontime(ontime):
    """
    :param ontime:
    :return: ontime_string
    """

    ontime_string = "CRC Error"

    if len(ontime) > 6:

        # Get the ontime hours hex value
        ontime_in_hour_hex = ontime[2:6]
        # Convert the ontime hours in decimal
        ontime_in_hour_decimal = int(ontime_in_hour_hex, base=16)

        ontime_in_hour_string = f"{round(ontime_in_hour_decimal)}h"

        # Get the ontime minutes hex value
        ontime_in_min_hex = ontime[6:8]
        # Convert the ontime minutes in decimal
        ontime_in_min_decimal = int(ontime_in_min_hex, base=16)

        ontime_in_min_string = f"{round(ontime_in_min_decimal)}min"

        ontime_string = " ".join([ontime_in_hour_string, ontime_in_min_string])

        # Return the string line
    return ontime_string


def convert_cal_laser(cal_laser):
    """
    cal laser
    :param cal_laser:
    calibrated output power [1/100 mW] and wavelength [nm]
    :return: power_out_abs_as_string
    """

    cal_laser_string = "CRC Error"

    if "\x00" in cal_laser:
        # Set the return value to wrong Hex value
        pd_value_string = "Wrong Hex value"
    else:

        if len(cal_laser) > 6:

            # Get the nominal_power hex value
            nominal_power_hex = cal_laser[2:6]
            # Convert the nominal_power in decimal
            nominal_power_decimal = int(nominal_power_hex, base=16) / 100

            nominal_power_string = f"{round(nominal_power_decimal)} mw"

            # Get the diode_wavelength hex value
            diode_wavelength_hex = cal_laser[6:10]
            # Convert the diode_wavelength in decimal
            diode_wavelength_decimal = int(diode_wavelength_hex, base=16)

            diode_wavelength_string = f"{round(diode_wavelength_decimal)} nm"

            cal_laser_string = " | ".join([nominal_power_string, diode_wavelength_string])

            # Return the string line
    return cal_laser_string


def convert_comp_ref(comp_ref):
    """
    Convert the Temperature of the GET_COMP_REF from hex in deg
    :param comp_ref: voltage hex code
    :return: comp_ref in mV
    """

    # Parameter comp REF voltage set by the SMCU current in mV in GET_COMP_REF
    u_ref = 2.06  # [V] Reference voltage
    dac_max = 65535  # [-] DAC max value for 16 bits (2^16 = 65535)

    if len(comp_ref) > 6:

        # Get the comp REF voltage hex value
        comp_ref_hex = comp_ref[2:6]
        # Convert the comp REF voltage in decimal
        comp_ref_decimal = int(comp_ref_hex, base=16) / 100
        # Calculate the comp REF voltage in mV
        comp_ref_value = u_ref * (comp_ref_decimal / dac_max) * 1000
        # make the string line for the list with interpretation
        comp_ref_string = f"{round(comp_ref_value, 2)} mV"

        # Return the string line
        return comp_ref_string
    else:
        return "CRC Error"


def convert_current_adc(current_adc):
    """
    Convert the Temperature of the GET_CURRENT_DAC_ADC from hex in deg
    :param current_adc: current hex code
    :return: NONE
    """

    # Parameter to calculate the ADC LD_TEMP
    u_ref = 2.06  # [V] Reference voltage
    adc_max = 65535  # [-] adc max value for 16 bits (2^16 = 65535)
    r_shunt = 4.8  # [Ohm] Shunt resistor (2,4  + 2,4)

    # adc_temp_as_list = []

    # Set the return value
    current_adc_as_string = "CRC Error"

    # Check if the Hex contain NUL = \x00
    if "\x00" in current_adc:
        # Set the return value to wrong Hex value
        current_dac_adc_as_string = "Wrong Hex value"

    else:
        if len(current_adc) > 6:

            # Get the adc temp hex value
            adc_temp_hex = current_adc[6:10]
            # Convert the adc temp in decimal
            adc_temp_decimal = int(adc_temp_hex, base=16)
            # Calculate the adc LD_TEMP2 in mV
            adc_temp2 = (u_ref * (adc_temp_decimal / adc_max) / r_shunt) * 1000
            # make the string line for the list with interpretation [mA]
            current_adc_as_string = str(round(adc_temp2, 2))

    # Return the string line
    return current_adc_as_string


def zx_interpret_results(hex_results_file_path):
    """
    Convert some columns of the test results from hex in clear text
    :param hex_results_file_path: path of the file with results in Hex
    :return: NONE
    """

    # Open the file with Hex results in read mode
    hex_results_file = open(hex_results_file_path, "r")

    # Create the name of the file that will contain additional columns with results in clear text
    interpreted_results_file_path = hex_results_file_path[:-4] + "_converter.csv"

    # Open the file that will contain additional columns with results in clear text in write mode
    interpreted_results_file = open(interpreted_results_file_path, "w")

    # Initialization indexes of column
    get_power_out_abs_index = 0
    get_power_val_in_perc_index = 0
    get_ld_lifetime_index = 0
    get_pd_value_index = 0
    get_module_total_ontime_index = 0
    get_cal_laser_index = 0
    get_comp_ref_index = 0
    get_fw_version_index = 0
    get_temp_adc_index = 0

    # Navigate through lines of the file with the results in Hex
    for counter, hex_results_line in enumerate(hex_results_file.readlines()):

        # check if first line
        if counter == 0:

            # Get the indexes of the columns
            header_hex_results_line_as_list = hex_results_line.strip().split(",")

            # Indexes of column
            get_power_out_abs_index = header_hex_results_line_as_list.index("GET_POWER_OUT_ABS")
            get_power_val_in_perc_index = header_hex_results_line_as_list.index("GET_POWER_VAL_IN_PERC")
            get_ld_lifetime_index = header_hex_results_line_as_list.index("GET_LD_LIFETIME")
            get_pd_value_index = header_hex_results_line_as_list.index("GET_PD_VALUE")
            get_module_total_ontime_index = header_hex_results_line_as_list.index("GET_MODULE_TOTAL_ONTIME")
            get_cal_laser_index = header_hex_results_line_as_list.index("GET_CAL_LASER")
            get_comp_ref_index = header_hex_results_line_as_list.index("GET_COMP_REF")
            get_fw_version_index = header_hex_results_line_as_list.index("GET_FW_VERSION")
            get_temp_adc_index = header_hex_results_line_as_list.index("GET_TEMP_ADC")

            # rewrite the header in the file with the titles of the new columns
            # and the new line character
            interpreted_results_file.write(hex_results_line.strip() + ",LD_TEMP_IN_DEG,STATUS_ERRORS_WARNING,"
                                                                      "LASER_ON_OR_OFF,SMCU_STATUS,TEMP_ADC,CURRENT,"
                                                                      "STATUS_BYTE,MODE,CONFIG_MODE,"
                                                                      "GET_CURRENT_DAC_ADC,GET_POWER_OUT_ABS,"
                                                                      "POWER_VAL_IN_PERC,LD_LIFETIME,GET_PD_VALUE,"
                                                                      "GET_MODULE_TOTAL_ONTIME,GET_CAL_LASER,"
                                                                      "GET_COMP_REF,GET_FW_VERSION,"
                                                                      "GET_CURRENT_ADC\n")

        else:  # Other lines
            # View the read line
            # print(hex_results_line)

            # Remove the new line ("\n") at the end of the line
            hex_results_line_strip = hex_results_line.strip()

            # Split at the comma to get each column element in the list
            hex_results_line_split = hex_results_line_strip.split(",")
            # View the split line
            # print(hex_results_line_split)
            # print(len(hex_results_line_split))

            """ Interpretation of GET_LD_TEMP """
            # Get the ld temp hex code
            ld_tem_hex = hex_results_line_split[7]
            # Convert the ntc temp value in deg
            temp_ntc_deg_value = convert_ld_temp_in_deg(ld_tem_hex)

            """ Interpretation of GET_STATUS """
            # Get the Status hex code
            status_hex = hex_results_line_split[14]
            # Convert the status
            status_hex_converted = get_errors_and_warnings_from_status_response(status_hex)

            """ Interpretation of GET_LASER_ON_OFF """
            # Get the laser on off hex code
            laser_on_off_hex = hex_results_line_split[8]
            # Convert the laser status
            laser_on_or_off = get_laser_on_or_off(laser_on_off_hex)

            """ Interpretation of GET_SMCU_STATUS """
            # Get the smcu status hex code
            smcu_status_hex = hex_results_line_split[15]
            # Interpret the smcu status
            smcu_status_hex_interpreted = interpret_get_smcu_status(smcu_status_hex)

            """ Interpretation of GET_TEMP_ADC """
            # Get the temp adc hex code
            tem_adc_hex = hex_results_line_split[get_temp_adc_index]
            # Convert the ntc temp value in deg
            temp_adc_deg_value = convert_temp_adc_in_deg(tem_adc_hex)

            """ Interpretation of GET_CURRENT """
            # Get the current hex code
            current_hex = hex_results_line_split[2]
            # Convert the current value in deg
            current_value = convert_current(current_hex)

            """ Interpretation byte of GET_STATUS """
            # Get the Status byte hex code
            status_byte_hex = hex_results_line_split[14]
            # Convert the status byte
            status_byte_converted = convert_status_byte(status_byte_hex)

            """ Interpretation byte of GET_MODE """
            # Get the mode hex code
            mode_hex = hex_results_line_split[3]
            # Convert the mode
            mode_converted = interpret_get_mode(mode_hex)

            """ Interpretation byte of GET_CONFIG_MODE """
            # Get the config_mode hex code
            config_mode_hex = hex_results_line_split[4]
            # Convert the config_mode
            config_mode_converted = interpret_get_config_mode(config_mode_hex)

            """ Interpretation of GET_CURRENT_DAC_ADC """
            # Get the current hex code
            current_dac_adc_hex = hex_results_line_split[30]
            # Convert the current value in mA
            current_dac_adc_value = convert_current_dac_adc(current_dac_adc_hex)

            """ Interpretation of GET_POWER_OUT_ABS """
            # Get the power_out hex code
            power_out_abs_hex = hex_results_line_split[get_power_out_abs_index]
            # Convert the power_out value in mw
            power_out_abs_value = convert_power_out_abs(power_out_abs_hex)

            """ Interpretation of GET_POWER_VAL_IN_PERC """
            # Get the power_val hex code
            power_val_in_perc_hex = hex_results_line_split[get_power_val_in_perc_index]
            # Convert the power_val value in percent
            power_val_in_perc_value = convert_power_val_in_perc(power_val_in_perc_hex)

            """ Interpretation of GET_LD_LIFETIME """
            # Get the ld_lifetime hex code
            ld_lifetime_hex = hex_results_line_split[get_ld_lifetime_index]
            # Convert the ld_lifetime value in hour and minutes
            ld_lifetime_value = convert_ld_lifetime(ld_lifetime_hex)

            """ Interpretation of GET_PD_VALUE """
            # Get the pd_value hex code
            pd_value_hex = hex_results_line_split[get_pd_value_index]
            # Convert the pd_value value in mA
            pd_value_value = convert_pd_value(pd_value_hex)

            """ Interpretation of GET_MODULE_TOTAL_ONTIME """
            # Get the ontime hex code
            ontime_hex = hex_results_line_split[get_module_total_ontime_index]
            # Convert the ontime value in hour and minutes
            ontime_value = convert_module_total_ontime(ontime_hex)

            """ Interpretation of GET_CAL_LASER """
            # Get the cal_laser hex code
            cal_laser_hex = hex_results_line_split[get_cal_laser_index]
            # Convert the output power in mW and wavelength value in nm
            cal_laser_value = convert_cal_laser(cal_laser_hex)

            """ Interpretation of GET_COMP_REF """
            # Get the comp_ref hex code
            comp_ref_hex = hex_results_line_split[get_comp_ref_index]
            # Convert the comp REF voltage set by the SMCU current in mV
            comp_ref_value = convert_comp_ref(comp_ref_hex)

            """ Interpretation of GET_FW_VERSION """
            # Get the hex code
            fw_version_hex = hex_results_line_split[get_fw_version_index]
            # Convert the MMCU and SMCU Firmware Version
            fw_version_value = interpret_get_fw_version(fw_version_hex)

            """ Interpretation of GET_CURRENT_ADC """
            # Get the current hex code
            current_adc_hex = hex_results_line_split[30]
            # Convert the current value in mA
            current_adc_value = convert_current_adc(current_adc_hex)

            """ Update the line with additional column's elements"""
            # Build the line with the additional columns at the end to be written in the file
            results_line = hex_results_line_strip + "," + temp_ntc_deg_value + "," + status_hex_converted + "," \
                           + laser_on_or_off + "," + smcu_status_hex_interpreted + "," + temp_adc_deg_value + ","\
                           + current_value + "," + status_byte_converted + "," + mode_converted + "," \
                           + config_mode_converted + "," + current_dac_adc_value + "," + power_out_abs_value \
                           + "," + power_val_in_perc_value + "," + ld_lifetime_value + "," + pd_value_value + "," \
                           + ontime_value + "," + cal_laser_value + "," + comp_ref_value + "," \
                           + fw_version_value + "," + current_adc_value + "\n"

            # Write the built line to the file with the deg lines
            interpreted_results_file.write(results_line)

    # Close the file with Hex code
    hex_results_file.close()
    # Close the file with additional interpreted columns
    interpreted_results_file.close()


if __name__ == "__main__":

    """ Call of the functions """

    """ Test of interpret_get_smcu_status """
    # print(interpret_get_smcu_status("0030141f601213407f"))

    """ Test of convert_status_byte """
    # print(convert_status_byte("ff0100000000000000000a1a"))

    """ Test of convert_pd_value(pd_value) """
    # print(convert_pd_value(""))

    """ Test of zx_interpret_results """
    zx_interpret_results("2300003506_TempZyklen_230727.csv")
