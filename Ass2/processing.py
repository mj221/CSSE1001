"""
    Logical processing classes used in the second assignment for CSSE1001/7030.

    ProcessResults: Abstract class that defines the logical processing interface.
    AthleteResults: Provides details of one athlete’s results for all of the
                    events in which they competed.
    CountryResults: Provides a summary of the results of all athletes who
                    competed for one country.
    EventResults  : Provides details of the results of all athlete's who
                    competed in one event.
    DeterminePlaces: Determines the place ranking of all athletes who competed
                     in one event.
"""

__author__ = "Minjae Lee"
__email__ = "m.j.lee@uqconnect.edu.au"



from entities import Athlete, Result, Event, Country, ManagedDictionary
from entities import all_athletes, all_countries, all_events, load_data



class ProcessResults(object) :      # Super class
    """Superclass for the logical processing commands."""

    _processing_counter = 0  # Number of times any process command has executed.
    
    def process(self) :
        """Abstract method representing collecting and processing results data.
        """
        ProcessResults._processing_counter += 1
    
    def get_results(self) :
        """Abstract method representing obtaining the processed results.

        Return:
            list: Subclasses will determine the contents of the resulting list.
        """
        raise NotImplementedError()



class AthleteResults(ProcessResults) :
    """Determines the resuls achieved by one athlete."""

    _athlete_results_counter = 0  # Number of times this command has executed.

    def __init__(self, athlete) :
        """
        Parameters:
            athlete (Athlete): Athlete for whom we wish to determine their results.
        """
        self._athlete = athlete     # athlete object
        self._results = []          # results list [array]
        self._processed = False     # Boolean. Keeps track of whether data was processed.

    def process(self) :
        """Obtain all the results for this athlete and
           order them from best to worst placing.
           If two or more results have the same place they should be ordered
           by event name in ascending alphabetical order.
        """
        super().process()                               # Call super class (ProcessResults) method.
        AthleteResults._athlete_results_counter += 1    # Add a count to _athlete_results_counter.
        events = self._athlete.get_events()
        
        place_sub = []  # A temporary list containing for each event in _athlete, the event object and name, and athlete place.

        for event in events:    # To store necessary data into place_sub
            event_obj = event
            event_name = event.get_name()
            place = self._athlete.get_result(event).get_place()

            place_sub.append([event_obj, event_name, place])

        place_sub.sort(key = lambda x: [float(x[2]), x[1]]) # Sort by athlete's place: Learned from web tutorial
        for data in place_sub:
            event_obj = data[0]
            result_obj = self._athlete.get_result(event_obj)
            self._results.append(result_obj)

        self._processed = True          # Data was processed
            
    def get_results(self) :
        """Obtain the processed results for _athlete.

        Return:
            list[Result]: Ordered list of the _athlete's results.
                          Sorted from best to worst, based on place in event.
                          Results with the same place are ordered by event name
                          in ascending alphabetical order.

        Raises:
            ValueError: If process has not yet been executed.
        """
        if self._processed:   # Checking whether process has been executed.
            return list(self._results)
        else:
            raise ValueError('The process has not yet been executed')       # Raise ValueError when process was not executed.

    def get_usage_ratio() :
        """Ratio of usage of the AthleteResults command against all commands.

        Return:
            float: ratio of _athlete_results_counter by _processing_counter.
        """
        return float(AthleteResults._athlete_results_counter                # Ratio of how often AthleteResults subclass was called/used 
                / AthleteResults._processing_counter)                                   
    
    def _sort_results(self, result):            # Sorting list of tuples.
        """How the result should be sorted. 

        Parameters:
            list[Result]: List of results of the athlete we wish to determine of.

        Return:
            list[Result], tuple<int, int> order of second item then by first
        """
        v1, v2 = result
        return v2, v1   #   Change tuple sorting.
         
    def __str__(self) :
        """(str) Return a formatted string of the results for this athlete."""
        """Implementation of this is optional but useful for observing your
           programs behaviour.
        """
        return ""

class EventResults(ProcessResults) :    ### Implented functionality, however does not work properly
    """Determines the results achieved by all athlete in one event."""

    _event_results_counter = 0  # Number of times this command has executed.

    def __init__(self, event) :
        """
        Parameters:
            event (Event): An event for which we want to determine the results of for all athletes.
        """
        self._event = event     # event object
        self._results = []      # results arrays
        self._processed = False # Boolean. Keeps track of whether data was processed.

    def process(self) :
        """Obtain all the results for this one event and
           order them from best to worst placing.
           If two or more results have the same place they should be ordered
           by the Athlete's full name in ascending alphabetical order.
        """
        super().process()   # Call super class (ProcessResults) method.
        EventResults._event_results_counter += 1        # Add a count to _event_results_counter.

        athletes = self._event.get_athletes()
        place_sub = []  # A temporary list containing for each event in _athlete, the event object and name, and athlete place.

        for athlete in athletes:    # To store necessary data into place_sub
            athlete_obj = athlete
            athlete_name = athlete.get_full_name()
            place = athlete.get_result(self._event).get_place()

            place_sub.append([athlete_obj, athlete_name, place])

        place_sub.sort(key = lambda x: [int(x[2]), x[1]]) # Sort by athlete's place: Learned from web tutorial
        for data in place_sub:
            athlete_obj = data[0]
            result_obj = athlete_obj.get_result(self._event)
            self._results.append(result_obj)

        self._processed = True          # Data was processed

    def get_results(self) :
        """Obtain the processed results for _event.

        Return:
            list[Result]: Ordered list of all results in one event
                          Sorted from best to worst, based on place in event.
                          Results with the same place are ordered by Athlete's name
                          in ascending alphabetical order.

        Raises:
            ValueError: If process has not yet been executed.
        """
        if self._processed:   # Checking whether process has been executed.
            return list(self._results)
        else:
            raise ValueError('The process has not yet been executed')   # Raise ValueError (process was not executed).
        
    def get_usage_ratio() :
        """Ratio of usage of the EventResults command against all commands.

        Return:
            float: ratio of _event_results_counter by _processing_counter.
        """
        return float(EventResults._event_results_counter    # Ratio of how often EventResults subclass was used
                / EventResults._processing_counter)                          

    def __str__(self) :
        return ""

class CountryResults(ProcessResults) :
    """ Obtains the summary of the results of one country's delegation.
        Total number of golds, silver and bronze and athletes competed in the game.

    """

    _country_results_counter = 0  # Number of times this command has executed.

    def __init__(self, country) :
        """
        Parameters:
            country (Country): A Country for which we need to find the result of.
        """
        self._country = country         # country object
        self._results = []              # Array
        self._gold_num = int()          # Assignment of gold_num variable (empty integer)
        self._silver_num = int()        # Assignment of silver_num variable (empty integer)
        self._bronze_num = int()        # Assignment of bronze_num variable (empty integer)
        self._athletes = int()       # Assignment of athlete_num (empty integer)
        self._processed = False         # Boolean. Keeps track of whether data was processed.
    
    def process(self) :
        """ Obtain total number of gold, silver and bronze medals obtained.
            Number of competing players for the Country.
        """
        super().process()       # Call super class (ProcessResults) method.
        CountryResults._country_results_counter += 1    # Add a count to _country_results_counter.

        for athlete in self._country.get_athletes():
            athlete_obj = athlete
            self._athletes += 1
            
            for event in athlete_obj.get_events():
                medal = athlete_obj.get_result(event).get_medal()
                if(medal == "Gold"):
                    self._gold_num += 1
                elif(medal == "Silver"):
                    self._silver_num +=1
                elif(medal == "Bronze"):
                    self._bronze_num +=1

                 
        self._results = [self._gold_num, self._silver_num,  # Listing results in the required format
                         self._bronze_num, self._athletes]
        self._processed = True          # Data was processed
        
    def get_results(self) :
        """Obtain the processed results for _country.

        Return:
            list[Result]: List of the medals earned + number of athletes competed.
                          Sorted from 'Gold', 'Silver', 'Bronze' to 'Number of Athletes'.

        Raises:
            ValueError: If process has not yet been executed.
        """
        if self._processed:   # Checking whether process has been executed.
            return list(self._results)     # Return results as list
        else:
            raise ValueError('The process has not yet been executed')       # Raise ValueError when executed before process

    def get_usage_ratio() :
        """Ratio of usage of the AthleteResults command against all commands.

        Return:
            float: ratio of _athlete_results_counter by _processing_counter.
        """
        return (CountryResults._country_results_counter     # Ratio of how often CountryResults subclass was used to process results 
                / CountryResults._processing_counter)

    def get_num_gold(self):
        """Obtain the number of gold medals achieved by athlets in _country
        Return:
            int: number of gold medals
        """
        return self._gold_num            # Return Gold Medal(quantity)

    def get_num_silver(self):
        """Obtain the number of silver medals achieved by athlets in _country
        Return:
            int: number of silver medals
        """
        return self._silver_num           # Return Silver Medal(quantity)
    
    def get_num_bronze(self):
        """Obtain the number of bronze medals achieved by athlets in _country
        Return:
            int: number of bronze medals
        """
        return self._bronze_num            # Return Bronze Medal(quantity)
    
    def get_num_athletes(self):
        """Number of athletes in country
        Return:
            int: Number of athletes
        """
        return self._athlete_num            # Return fourth list item: Number of athletes competed for that Country

    def __str__(self) :
        return ""
    
class DeterminePlaces(ProcessResults) :     ### Unfinished Implementation
    """Process results to determine the athlete's final places."""

    _determine_places_counter = 0  # Number of times this command has executed.

    def __init__(self, places) :
        """
        Parameters:
            athlete (Athlete): Athlete for whom we wish to determine their results.
        """
        self._places = places      # Number of places
        self._results = []
        
        self._processed = False     # Boolean. Keeps track of whether data was processed.

    def process(self) :
        """Obtain all the results for this athlete and
           order them from best to worst placing.
           If two or more results have the same place they should be ordered
           by event name in ascending alphabetical order.
        """
        super().process()
        DeterminePlaces._determine_places_counter += 1

        if Event.is_timed == True:          # If Event is timed, then call respective method
            self._results.sort(key = self._sort_results_timed)
        else:                               # If Event is scored, then call respective method
            self._results.sort(key = self._sort_results_scored) 
        self._processed = True          # Data was processed

    def get_results(self) :
        """Obtain the processed results for _athlete.

        Return:
            list[Result]: Ordered list of the _athlete's results.
                          Sorted from best to worst, based on place in event.
                          Results with the same place are ordered by event name
                          in ascending alphabetical order.

        Raises:
            ValueError: If process has not yet been executed.
        """
        if self._processed:             # If data was processed
            return list(self._results)  # get list of result
        else:
            raise ValueError('The process has not yet been executed')   # Raise ValueError if not processed

    def get_usage_ratio() :
        """Ratio of usage of the AthleteResults command against all commands.

        Return:
            float: ratio of _athlete_results_counter by _processing_counter.
        """
        return (DeterminePlaces._determine_places_counter           # Return ratio counter
                / DeterminePlaces._processing_counter)
    
    def _sort_results_scored(self, result):     # Sort scores from highest to lowest
        """How the scored result should be sorted. 

        Parameters:
            list[Result]: List of scores we wish to list

        Return:
            list[Result], tuple<int, int> order of second item then by first
        """
        v1, v2 = result
        return v2, v1
    
    def _sort_results_timed(self, result):      # Sort time from lowest to highest
        """How the scored result should be sorted. 

        Parameters:
            list[Result]: List of scores we wish to list

        Return:
            list[Result], tuple<int, int> order of second item then by first
        """
        v1, v2 = result
        return v1, v2
    
    def __str__(self) :
        return ""
    
def demo_entities() :
    """Simple test code to demonstrate using the entity classes.
       Output is to console.
    """
    TIMED = True
    SCORED = False

    print("Demonstrate creating country objects:")
    CAN = Country("Canada", "CAN")
    AUS = Country("Australia", "AUS")
    all_countries.add_item(CAN.get_country_code(), CAN)
    all_countries.add_item(AUS.get_country_code(), AUS)
    for country in all_countries.get_items() :
        print(country)

    print("\nDemonstrate creating athlete objects, adding them to",
          "all_athletes and countries:")
    a1 = Athlete("1", "Athlete", "One", CAN)
    a2 = Athlete("2", "Athlete", "Two", CAN)
    a3 = Athlete("10", "Athlete", "Three", CAN)
    a4 = Athlete("4", "Athlete", "Four", AUS)
    a5 = Athlete("5", "Athlete", "Five", AUS)
    a6 = Athlete("20", "Athlete", "Six", AUS)
    for athlete in [a1, a2, a3, a4, a5, a6] :
        all_athletes.add_item(athlete.get_id(), athlete)
    athletes = all_athletes.get_items()
    for athlete in athletes :
        print(athlete)
    CAN.add_athletes([a1, a2, a3])
    AUS.add_athletes([a4, a5, a6])
    print("\nDemonstrate finding an athlete in all_athletes:")
    print(all_athletes.find_item("2"))

    # Create event objects and add athletes to the events.
    e1 = Event("Event1", TIMED, [a1, a2, a3, a4, a5])
    all_events.add_item(e1.get_name(), e1)
    a2.add_event(e1)
    a3.add_event(e1)
    a4.add_event(e1)
    a5.add_event(e1)
    e2 = Event("Event2", SCORED, [a1, a2, a3, a5, a6])
    all_events.add_item(e2.get_name(), e2)
    a2.add_event(e2)
    a3.add_event(e2)
    a5.add_event(e2)
    a6.add_event(e2)
    a1.add_events([e1, e2])

    # Create result objects for each athlete in the events.
    a1.add_result(e1, Result(10.5))
    a2.add_result(e1, Result(9.5))
    a3.add_result(e1, Result(11.5))
    a4.add_result(e1, Result(8.5))
    a5.add_result(e1, Result(12.5))

    a1.add_result(e2, Result(100.5))
    a2.add_result(e2, Result(99.5))
    a3.add_result(e2, Result(98.5))
    a5.add_result(e2, Result(90.5))
    a6.add_result(e2, Result(89.5))



def demo_processing() :
    """Simple test code to demonstrate using the processing classes.
       Output is to console.
    """
    print("\n\nDemonstrate processing of results:")
    for athlete in all_athletes.get_items() :
        athlete_results = AthleteResults(athlete)
        athlete_results.process()
        results = athlete_results.get_results()
        # Do something with this athlete's results.

    print("\nDemonstrate listing the results for an event:")
    event = all_events.find_item("Event1")
    results_dict = {}
    for athlete in event.get_athletes() :
        results_dict[athlete.get_result(event).get_result()] = \
            athlete.get_result(event)
    for result in sorted(results_dict) :
        print(result)

    print("\nAthleteResults was used",
          "{0:.1%}".format(AthleteResults.get_usage_ratio()),
          "of the time of all results processing commands.")



if __name__ == "__main__" :
    demo_entities()
    demo_processing()
