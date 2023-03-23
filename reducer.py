#! /usr/bin/env python3

import sys

def main():
    reducing = Reducing()
    reducing.input_reduce(sys.stdin)

class Help_reduce():
    """
    Class that contains some helping functions and the values that are going to be calculated from
    the reducing function.
    """
    def __init__(self, day):
        self.day = day
        self.wind_speed_values = []
        self.humidity_values = []
        self.dew_point_values = []
        self.dry_bulb_temp_values=[]
        self.wind_speed_daily_max = None
        self.wind_speed_daily_min = None
        self.humidity_daily_min = None
        self.dew_point_values_sum = 0
        self.dew_point_values_squared_sum = 0
        self.dew_point_values_n = 0

    def add_value(self, wind_speed_value, humidity_value, dew_point_value,dry_bulb_temp_value) -> None:
        """
        Add a value to the value collection.
        
        Parameters
        ----------
        wind_speed_value, humidity_value, dew_point_value,dry_bulb_temp_value : str
            The output from the mapper.
        """
        # add the value to the collection
        self.wind_speed_values.append(wind_speed_value)
        self.humidity_values.append(humidity_value)
        self.dew_point_values.append(dew_point_value)
        self.dry_bulb_temp_values.append(dry_bulb_temp_value)
        # update the maximum and minimum values
        if self.wind_speed_daily_max is None:
            # initializing maximum and minimum values
            self.wind_speed_daily_max = wind_speed_value
            self.wind_speed_daily_min = wind_speed_value
        else:
            if wind_speed_value > self.wind_speed_daily_max: self.wind_speed_daily_max = wind_speed_value
            if wind_speed_value < self.wind_speed_daily_min: self.wind_speed_daily_min = wind_speed_value
        
        # update maximums and minimums
        if self.humidity_daily_min is None:
            # initializing maximum and mininimum values
            self.humidity_daily_min = humidity_value
        else:
            if humidity_value < self.humidity_daily_min: self.humidity_daily_min = humidity_value
        # update "running" values
        self.dew_point_values_n += 1
        self.dew_point_values_sum += dew_point_value
        self.dew_point_values_squared_sum += dew_point_value * dew_point_value
        
    def variance_function(self) -> float:
        """
        Function for calculating and returning the variance.

        """
        mean = self.dew_point_values_sum / float(self.dew_point_values_n)

        return  (1.0 / self.dew_point_values_n) * (self.dew_point_values_squared_sum - self.dew_point_values_n * mean*mean)
        
    def combinations(self):
        """
        Calculate the correlation of the values.
        """
        correlations=[]
        for i in [self.wind_speed_values,self.humidity_values,self.dry_bulb_temp_values]:
            for j in [self.wind_speed_values,self.humidity_values,self.dry_bulb_temp_values]:
                mi = sum(i)/len(i)
                mj = sum(j)/len(j)
                cov = sum((a - mi) * (b - mj) for (a,b) in zip(i,j)) / len(i)
                stdevi = (sum((a - mi)**2 for a in i)/len(i))**0.5
                stdevj = (sum((b - mj)**2 for b in j)/len(j))**0.5
                result = round(cov/(stdevi*stdevj),3)
                #print(result)
                correlations.append(result)
        return correlations
    
    def create_matrix(self,correlation):
        """
        Creates a matrix with the correlations.
        
        Parameters
        ----------
        correlation : str
            correlation between values.
        """
        sqrt = int(len(correlation) ** 0.5)
        matrix = []
        while correlation != []:
            matrix.append(correlation[:sqrt])
            correlation = correlation[sqrt:]
        return matrix

        
    
    def output(self) -> None:
        """
        Print the day values to stdout.
       
        """
        # calculate the mean
        wind_speed_daily_difference = self.wind_speed_daily_max - self.wind_speed_daily_min
        dew_point_values_mean = self.dew_point_values_sum / float(self.dew_point_values_n)
        # print the output
        print('%s, %d, %d, %.1f, %.6f' % (
            self.day,
            wind_speed_daily_difference,
            self.humidity_daily_min,
            dew_point_values_mean,
            self.variance_function()
            ))

class Reducing():
    """
    Class for summarizing the observations for each day.
    """
    def input_reduce(self, input_data):
        """
        Function that reduces the output of the mapper 
        to calculate the maximum, minimum, mean, variance, correlation and matrix.

        Parameter
        ----------
        input_data : iterable
            The input data that is going to be processed.
        """
        current_day = Help_reduce(None)
        for element in input_data:
            if element:
                # get the day and values
                day_value, dry_bulb_temp_value,dew_point_value, humidity_value, wind_speed_value = element.split(',')       
                day_value = str(day_value)
                wind_speed_value = int(wind_speed_value)
                humidity_value = int(humidity_value)
                dew_point_value = int(dew_point_value)
                dry_bulb_temp_value = int(dry_bulb_temp_value)
                
                if current_day.day == day_value:
                    current_day.add_value(wind_speed_value, humidity_value, dew_point_value,dry_bulb_temp_value)
                else:
                    # show the output if the current day exists
                    if current_day.day:
                        current_day.output()

                    # create the new day
                    current_day = Help_reduce(day_value)
                    current_day.add_value(wind_speed_value, humidity_value, dew_point_value, dry_bulb_temp_value)

        # print the last processed day
        if current_day.day == day_value:
            current_day.output()   
        print (current_day.create_matrix(current_day.combinations()))

if __name__=="__main__":
    main()