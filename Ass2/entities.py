"""
    Entity classes used in the second assignment for CSSE1001/7030.

    Athlete: Details of an athlete participating at the games.
    Event: Details of an individual event at the games.
    Country: Details of a country and its delegation at the games.
    Result: An athlete's result in an event.
"""

__author__ = "Minjae Lee"
__email__ = "m.j.lee@uqconnect.edu.au"

import csv

class Athlete(object) :
    """Details of an athlete who is competing at the games."""
    
    def __init__(self, identifier, first_name, surname, country) :
        """
        Parameters:
            identifier (str): Athlete's identification number
            first_name (str): Athlete's first name.
            surname (str): Athlete's surname.
            country (Country): Object representing this athlete's country.
        """
        self._identifier = identifier
        self._first_name = first_name
        self._surname = surname
        self._country = country
        self._results = {}
        self._events = []

    def get_result(self, event) :
        """Return the result the athlete obtained in 'event'.

        Parameters:
            event (Event): Event for which the athlete's result is wanted.
            
        Return:
            Result: Athlete's result in 'event'.
        """
        return self._results[event]

    def add_result(self, event, result) :
        """Sets athlete's 'result' in 'event', overwriting if previously set.

        Parameters:
            event (Event): Event in which this athlete competed.
            result (Result): Final result obtained in event.
        """
        self._results[event] = result
        
    def add_event(self, event) :
        """Adds event to those in which this athlete will compete.

        Parameters:
            event (Event): Event in which this athlete will compete.
        """
        self._events.append(event)
        
    def add_events(self, events) :
        """Adds all events to those in which this athlete will compete.

        Parameters:
            events (list[Event]): List of events in which this athlete will compete.
        """
        return self._events.extend(list(events))
        
    def get_events(self) :
        """(list[Event]) All events in which this athlete is competing."""
        return list(self._events)

    def get_id(self) :
        """(str) Athlete's identification number."""
        return self._identifier
    
    def get_full_name(self) :
        """(str) Athlete's full name (first + surname)."""
        return (self._first_name + " " + self._surname)

    def get_country(self) :
        """(Country) Country delegation to which this Athlete belongs."""
        return self._country

    def __str__(self) :
        return ""



class Result(object) :
    """An athlete's result in an event."""

    def __init__(self, result_value) :
        """
        Parameters:
            result_value (float): Time or score athlete achieved in event.
        """
        self._result_value = result_value
        self._place = int()
        self._medal = str()
        
    def get_place(self) :
        """(str) Place athlete obtained in the final event.

        Raise:
            RuntimeError: if places not yet determined.
        """
        if Result.places_determined(self):
            return str(self._place)
        else:
            raise RuntimeError('Places not yet determined')

    def set_place(self, place) :
        """Sets the place that the athlete achieved in the final event.

        Parameters:
            place (int): Place that athlete achieved in the event.
        """
        self._place = place

    def places_determined(self) :
        """(bool) Has places been determined yet or not."""
        return self._place > 0
    
    def get_result(self) :
        """(str) Time or score athlete achieved in the final event."""
        return str(self._result_value)

    def get_medal(self) :
       
        """(str) Medal athlete achieved or empty string if no medal.

        Raise:
            RuntimeError: if places not yet determined.
        """
        if Result.places_determined(self):          # If a place is determined
            if Result.get_place(self) == "3":
                self._medal = "Bronze"
            elif Result.get_place(self) == "2":
                self._medal = "Silver"
            elif Result.get_place(self) == "1":
                self._medal = "Gold"
            else:
                self._medal = ""
        else:
            raise RuntimeError('Place not yet determined')
        
        return str(self._medal)
        
        
    def __str__(self) :
        return ""


class Event(object) :
    """An event in which athletes compete."""
    
    def __init__(self, event_name, timed, athletes) :
        """
        Parameters:
            event_name (str): Official name of this event.
            timed (bool): Indicates if this is a timed event (else scored).
            athletes (list[Athlete]): Athletes who will compete in this event.
        """
        self._event_name = event_name
        self._timed = timed
        self._athletes = []
        
    def is_timed(self) :
        """(bool) True if event is timed, False if event is scored."""
        return self._timed
        
    def get_name(self) :
        """(str) Official name of this event."""
        return self._event_name
        
    def get_athletes(self) :
        """(list[Athlete]) All athletes currently registered to compete
                           in this event.
        """
        return list(self._athletes)
        
    def add_athlete(self, athlete) :
        """Adds athlete to those who will compete in this event.

        Parameters:
            athlete (Athlete): An athlete who will compete in this event.
        """
        self._athletes.append(athlete)
        
    def add_athletes(self, athletes) :
        """Adds all athletes to those who will compete in this event.

        Parameters:
            athletes (list[Athlete]): List of athletes who will compete
                                      in this event.
        """
        return self._athletes.extend(list(athlete))

    def __str__(self) :
        return ""



class Country(object) :
    """Representation of a country's delegation."""

    def __init__(self, country_name, country_code) :
        """
        Parameters:
            country_name (str): Official name of this country.
            country_code (str): 3 letter code used to represent this country.
        """
        self._country_name = country_name
        self._country_code = country_code
        self._athletes = []
        
    def get_athletes(self) :
        """(list[Athlete]) All athletes competing for this country."""
        return list(self._athletes)
                            
        
    def add_athlete(self, athlete) :
        """Adds athlete as a member of this country's delegation.

        Parameters:
            athlete (Athlete): An athlete who will compete for this country.
        """
        self._athletes.append(athlete)
        
    def add_athletes(self, athletes) :
        """Adds all athletes as members of this country's delegation.

        Parameters:
            athletes (list[Athlete]): List of athletes who will compete
                                      for this country.
        """
        self._athletes.extend(list(athletes))

    def get_name(self) :
        """(str) Country's official name."""
        return self._country_name

    def get_country_code(self) :
        """(str) Country's 3 letter representation code."""
        return self._country_code

    def __str__(self) :
        return ""



class ManagedDictionary(object) :
    """A generic collection as a managed dictionary."""

    def __init__(self) :
        self._items = {}

    def add_item(self, key, item) :
        """Adds an item to this collection.
           Overwriting previous item if key was mapped to an item already.

        Parameters:
            key (immutable): Unique key for the item.
            item (value): The item to be added to this collection.
        """
        self._items[key] = item
        
    def get_items(self) :
        """(list) All items in this collection."""
        return list(self._items.values())

    def find_item(self, key) :
        """Return the item which corresponds to this key.

        Parameters:
            key (immutable): Unique key for an item.

        Return:
            (value): Item that corresponds to this key.

        Raises:
            (KeyError): If 'key' does not correspond to an item.
        """
        return self._items[key]


"""
    Globally defined collections of all key entity objects.
    These are to be used to store all of each type of entity objects that
    are created by your program.
"""
all_athletes = ManagedDictionary()
all_countries = ManagedDictionary()
all_events = ManagedDictionary()

def load_athletes(athletes):    
    """ Load the data from files into all_athletes.

        Parameters:
            athletes (str) : Name of file containing athlete data.
            
    """
    athlete_file = csv.reader(open("athletes.csv"))                                     # Load data from the data file
    for row in athlete_file:        
        athlete_country = all_countries.find_item(row[3])                               # Load country names from row 4
        athlete_sub = Athlete(str(row[0]), row[1], row[2], athlete_country)             # 
        athlete_country.add_athlete(athlete_sub)
        all_countries.add_item(athlete_country.get_country_code(), athlete_country)
        all_athletes.add_item(row[0], athlete_sub)

def load_countries(countries):
    """ Load the data from files into all_countries.

        Parameters:
            countries (str): Name of file containing country data.
            
    """
    country_file = csv.reader(open("countries.csv"))
    for row in country_file:
        country_sub = Country(row[1], row[0])
        all_countries.add_item(country_sub.get_country_code(), country_sub)
         
         
def load_events(events):
    """ Load the data from files into all_events.

        Parameters:
            events (str)   : Name of file containing events data.
            
    """
    event_file = csv.reader(open("events.csv"))
    for row in event_file:
        timed = True
        if(row[1] == "SCORED"):
            timed == False
        event_sub = Event(row[0], timed, [])
        all_events.add_item(row[0], event_sub)
         

def load_scored_events(scored_event_results):
    """ Load the data from files into all_athletes and all_events.

        Parameters:
            scored_event_results (str): Name of file containing results for scored
                                     events.
    """
    scored_event_file = csv.reader(open("scored_event_results.csv"))
    for row in scored_event_file:
        event_obj = all_events.find_item(row[1])
        athlete_obj = all_athletes.find_item(row[0])
        result_obj = Result(row[2])
        event_obj.add_athlete(athlete_obj)
        all_events.add_item(event_obj.get_name(), event_obj)
        athlete_obj.add_event(event_obj)
        athlete_obj.add_result(event_obj, result_obj)
        all_athletes.add_item(athlete_obj.get_id(), athlete_obj)


def load_timed_events(timed_event_results):
    """ Load the data from files into all_athletes and all_events.

        Parameters:
            timed_event_results (str) : Name of file containing results for timed
                                     events.
    """
    timed_event_file = csv.reader(open("timed_event_results.csv"))
    for row in timed_event_file:
        event_obj = all_events.find_item(row[1])
        athlete_obj = all_athletes.find_item(row[0])
        result_obj = Result(row[2])
        event_obj.add_athlete(athlete_obj)
        all_events.add_item(event_obj.get_name(), event_obj)
        athlete_obj.add_event(event_obj)
        athlete_obj.add_result(event_obj, result_obj)
        all_athletes.add_item(athlete_obj.get_id(), athlete_obj)

def load_data(athletes, countries, events,
              timed_event_results, scored_event_results) :
    """Loads the data from the named data files.

    Data is loaded into the all_athletes, all_countries and all_events
    collections. Results are accessible through the objects in these collections.

    Parameters:
        athletes (str) : Name of file containing athlete data.
        countries (str): Name of file containing country data.
        events (str)   : Name of file containing events data.
        timed_event_results (str) : Name of file containing results for timed
                                     events.
        scored_event_results (str): Name of file containing results for scored
                                     events.
    """

    load_countries(countries)                   # Call functions
    load_athletes(athletes)
    load_events(events)
    load_scored_events(scored_event_results)
    load_timed_events(timed_event_results)


if __name__ == "__main__" :
    print("This module provides the entities for the Olympic games results",
          "processing application and is not meant to be executed on its own.")
