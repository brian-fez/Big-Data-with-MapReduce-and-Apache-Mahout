#! /usr/bin/env python3

import sys

def main():
    mapping = Mapping()
    mapping.input_map(sys.stdin)


class Mapping():
    """
    Class for implementing the mapping process.
    """
    def input_map(self, data_input):
        """
        Function that maps each input to the output.
        Parameter
        ----------
        input_data : iterable
            Data to be processed.
        """
        data_output = []

        for element in data_input:
            mapped_element = self.map_function(element)
            if mapped_element:
                print(mapped_element)

        return data_output

    def map_function(self, element):
        """
        Function for mapping the input to the day the observations the dry bulb temperature, dew point temperature, 
            humidity, wind speed values.

        Parameters
        ----------
        item : str
            The data to be mapped.

        Returns
        -------
        output : str
            String that contains the date format YYYYMMDD and dry bulb temperature, dew point temperature , 
            humidity and wind speed.
        """
        # code for ignoring the headers of the file
        if element.startswith('Wban Number'):
            return None

        # code for ignoring empty lines
        if element == '\n':
            return None

        # input tokenization
        token = element.split(',')

        # extract the day value
        day = token[1].strip()

        # code for extracting the dry bulb temperature, dew point, humidity, wind speed
        dry_bulb_temp_value = token[8].strip()
        dew_point_value = token[9].strip()
        humidity_value = token[11].strip()
        wind_speed_value = token[12].strip()
        # will not process empty or wrong values
        for i in (dry_bulb_temp_value, dew_point_value, humidity_value, wind_speed_value):
            if i in  ['-','','/0','//','`0']:
                return None
            else:
                i = int(i)

        # return the key and values
        return '%s,%s,%s,%s,%s' % (day, dry_bulb_temp_value, dew_point_value, humidity_value, wind_speed_value)
        
if __name__=="__main__":
    main()