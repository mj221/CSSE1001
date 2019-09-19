#!/usr/bin/env python3
"""
Supporting tests for the second assignment

Passing these test is NOT a guarantee your code works. It is up to you to
test and verify that your code works correctly. We will use more tests than
this to mark your assignment and verify functionality. Many test cases have
not been included.

Usage:
At the command line, and in the same directory as your assignment solution type:
   python sample_tests_a2.py
OR
   Execute sample_tests_a2.py through IDLE

Put sample_tests_a2.py and testrunner.py in the same folder as your assignment
solution files, which must be called 'entities.py' and 'processing.py'.
Ensure there is a folder called 'data_files' which contains the data files
athletes.csv, countries.csv, events.csv, scored_event_results.csv and
timed_event_results.csv

In the interest of getting this testing code to you ASAP we have skipped some
good coding practices, e.g. detailed comments, magic numbers and accessing
private variables.
Do not take this as a perfect example of code for this course.
"""

from testrunner import *

import os

import entities
import processing

__author__ = "Joshua Sutton"
__version__ = "1.0.1"

# #############################################################################
# DEFAULT OVERRIDES #
DEFAULTS["VERSION"] = "2018s1"
DEFAULTS["HIDE_TRACEBACK_PATHS"] = True
# The script to test
DEFAULTS["SCRIPT"] = "processing"
DEFAULTS["MAXDIFF"] = 20000
DEFAULTS["TEST_DATA"] = None
DEFAULTS["TEST_DATA_RAW"] = None


# END DEFAULT OVERRIDES #
# #############################################################################

def setUpTestFiles1():
    with open("countries.test", "w") as countryFile:
        countryFile.write(
            "AUS,Australia\nAUT,Austria\nCAN,Canada\nCHN,China\nFIN,Finland\nFRA,France\nGBR,Great Britian\nGER,Germany\nITA,Italy\nJPN,Japan\nKAZ,Kazakhstan\nKOR,Republic of Korea\nMEX,Mexico\nNED,Netherlands\nNOR,Norway\nUSA,United States of America\n")
    with open("athletes.test", "w") as athleteFile:
        athleteFile.write(
            "1,Rohan,Chapman-Davies,AUS\n2,Matt,Graham,AUS\n3,Brodie,Summers,AUS\n4,James,Matheson,AUS\n5,Madii,Himbury,AUS\n6,Jakara,Anthony,AUS\n7,Britteny,Cox,AUS\n8,Claudia,Gueli,AUS\n9,Alexander,Ferlazzo,AUS\n10,David,Morris,AUS\n11,Lydia,Lassila,AUS\n12,Laura,Peel,AUS\n13,Danielle,Scott,AUS\n14,Samantha,Wells,AUS\n15,Scotty,James,AUS\n16,Kent,Callister,AUS\n17,Nathan,Johnstone,AUS\n18,Emily,Arthur,AUS\n19,Holly,Crawford,AUS\n20,Russ,Henshaw,AUS\n21,Daniel,Greig,AUS\n22,Lewis,Irving,CAN\n23,Olivier,Rochon,CAN\n24,Catrine,Lavallee,CAN\n25,Marc-Antoine,Gagnon,CAN\n26,Mikael,Kingsbury,CAN\n27,Philippe,Marquis,CAN\n28,Chloe,Dufour-Lapointe,CAN\n29,Justine,Dufour-Lapointe,CAN\n30,Andi,Naude,CAN\n31,Audrey,Robichaud,CAN\n32,Sam,Edney,CAN\n33,Reid,Watts,CAN\n34,Mitchel,Malyk,CAN\n35,Alex,Gough,CAN\n36,Kimberley,McRae,CAN\n37,Brooke,Apshkrum,CAN\n38,Derek,Livingstone,CAN\n39,Elizabeth,Hocking,CAN\n40,Calynn,Irwin,CAN\n41,Mercedes,Nicoll,CAN\n42,Max,Parrot,CAN\n43,Mark,McMorris,CAN\n44,Tyler,Nicholson,CAN\n45,Sebastien,Toutant,CAN\n46,Laurie,Blouin,CAN\n47,Brooke,Voigt,CAN\n48,Spencer,O'Brien,CAN\n49,Gilmore,Junio,CAN\n50,Laruent,Dubreuil,CAN\n51,Alex,Boisvert-Lacroix,CAN\n52,Alexandre,St-Jean,CAN\n53,Vincent,De Haitre,CAN\n54,Ted-Jan,Bloemen,CAN\n55,Kim,Boutin,CAN\n56,Jamie,MacDonald,CAN\n57,Kaylin,Irvine,CAN\n58,Heather,McLean,CAN\n59,Natalie,Geisenberger,GER\n60,Sven,Kramer,NED\n61,Sverre Lunde,Pedersen,NOR\n62,Choi,Minjeong,KOR\n63,Arianna,Fontana,ITA\n64,Yara,van Kerkhof,NED\n65,Elise,Christie,GBR\n66,Redmond,Gerard,USA\n67,Shaun,White,USA\n68,Ayumu,Hirano,JPN\n69,Chloe,Kim,USA\n70,Jiayu,Liu,CHN\n71,Arielle,Gold,USA\n72,Chris,Mazdzer,USA\n73,David,Gleirscher,AUT\n74,Johannes,Ludwig,GER\n75,Dajana,Eitberger,GER\n76,Perrine,Laffont,FRA\n77,Yulia,Galysheva,KAZ\n78,Daichi,Hara,JPN\n79,Jamie,Anderson,USA\n80,Enni,Rukajarvi,FIN\n81,Jorien,Ter Mors,NED\n82,Nao,Kodaira,JPN\n83,Miho,Takagi,JPN\n84,Brittany,Bowe,USA\n")
    with open("events.test", "w") as eventFile:
        eventFile.write(
            "Men's Aerials,SCORED\nMen's Half-Pipe,SCORED\nMen's Luge,TIMED\nMen's Moguls,SCORED\nMen's Slopestyle,SCORED\nMen's Speedskating 1000m,TIMED\nMen's Speedskating 5000m,TIMED\nMen's Speedskating 500m,TIMED\nWomen's Aerials,SCORED\nWomen's Half-Pipe,SCORED\nWomen's Luge,TIMED\nWomen's Moguls,SCORED\nWomen's Slopestyle,SCORED\nWomen's Speedskating 1000m,TIMED\nWomen's Speedskating 500m,TIMED\n")
    with open("timed_event_results.test", "w") as timedFile:
        timedFile.write(
            "9,Men's Luge,219.287\n21,Men's Speedskating 500m,35.22\n21,Men's Speedskating 1000m,69.99\n32,Men's Luge,191.021\n33,Men's Luge,191.49\n34,Men's Luge,191.946\n35,Women's Luge,185.644\n36,Women's Luge,185.878\n37,Women's Luge,187.561\n49,Men's Speedskating 500m,35.158\n50,Men's Speedskating 500m,35.16\n51,Men's Speedskating 500m,34.934\n52,Men's Speedskating 1000m,69.24\n50,Men's Speedskating 1000m,70.03\n53,Men's Speedskating 1000m,69.79\n54,Men's Speedskating 5000m,371.616\n55,Women's Speedskating 500m,43.881\n56,Women's Speedskating 500m,55.65\n57,Women's Speedskating 1000m,76.9\n58,Women's Speedskating 1000m,77.25\n59,Women's Luge,185.232\n60,Men's Speedskating 5000m,369.76\n61,Men's Speedskating 5000m,371.618\n62,Women's Speedskating 500m,56.66\n63,Women's Speedskating 500m,42.569\n64,Women's Speedskating 500m,43.256\n65,Women's Speedskating 500m,83.063\n72,Men's Luge,190.728\n73,Men's Luge,190.702\n74,Men's Luge,190.932\n75,Women's Luge,185.599\n81,Women's Speedskating 1000m,73.56\n82,Women's Speedskating 1000m,73.82\n83,Women's Speedskating 1000m,73.98\n84,Women's Speedskating 1000m,74.36\n")
    with open("scored_event_results.test", "w") as scoredFile:
        scoredFile.write(
            "1,Men's Moguls,73.96\n2,Men's Moguls,82.57\n3,Men's Moguls,15.11\n4,Men's Moguls,75.98\n5,Women's Moguls,68.19\n6,Women's Moguls,75.35\n7,Women's Moguls,75.08\n8,Women's Moguls,68.68\n10,Men's Aerials,61.95\n11,Women's Aerials,44.69\n12,Women's Aerials,55.34\n13,Women's Aerials,47.01\n14,Women's Aerials,34.28\n15,Men's Half-Pipe,92\n16,Men's Half-Pipe,62\n17,Men's Half-Pipe,62.25\n18,Women's Half-Pipe,48.25\n19,Women's Half-Pipe,57.5\n20,Men's Slopestyle,1\n22,Men's Aerials,86.28\n23,Men's Aerials,98.11\n24,Women's Aerials,52.24\n25,Men's Moguls,77.02\n26,Men's Moguls,86.63\n27,Men's Moguls,12.22\n28,Women's Moguls,70.98\n29,Women's Moguls,78.56\n30,Women's Moguls,13.33\n31,Women's Moguls,74.89\n38,Men's Half-Pipe,71.25\n39,Women's Half-Pipe,36.75\n40,Women's Half-Pipe,23.25\n41,Women's Half-Pipe,50\n42,Men's Slopestyle,86\n43,Men's Slopestyle,85.2\n44,Men's Slopestyle,76.41\n45,Men's Slopestyle,61.08\n46,Women's Slopestyle,76.33\n47,Women's Slopestyle,36.61\n48,Women's Slopestyle,36.45\n66,Men's Slopestyle,87.16\n67,Men's Half-Pipe,97.75\n68,Men's Half-Pipe,95.25\n69,Women's Half-Pipe,98.25\n70,Women's Half-Pipe,89.75\n71,Women's Half-Pipe,85.75\n76,Women's Moguls,78.65\n77,Women's Moguls,77.4\n78,Men's Moguls,82.19\n79,Women's Slopestyle,83\n80,Women's Slopestyle,75.38\n")


def tearDownTestFiles():
    os.remove("countries.test")
    os.remove("athletes.test")
    os.remove("events.test")
    os.remove("scored_event_results.test")
    os.remove("timed_event_results.test")

class A2TestClass(OrderedTestCase):
    """Base class for a2 tests"""

    def assertMethodDefined(self, class_instance, method_name, parameters):
        """ Asserts that a method (class function) is correctly defined with the correct number
        of parameters
        Parameters:
            class_instance: The class instance
            method_name (string): The name of the method
            parameters (int): The number of parameters the method should take
        """

        self.assertDefined(class_instance, method_name, FunctionType)

        sig = signature(getattr(class_instance, method_name))

        if len(sig.parameters) != parameters:
            raise AssertionError(
                "'{}' does not have the correct number of parameters, expected {} found {}".format(
                    method_name, parameters, len(sig.parameters)
                )
            )

    def assertDefined(self, module, variable, var_type):
        """ Asserts that a variable is defined inside a module
        with the given type
        Raises an assertion error if it fails
        Parameters:
            module: The module or class
            variable (string): The name of the variable
            var_type (type): The type of the variable
        """

        if not hasattr(module, variable):
            raise AssertionError("'{}' is not defined correctly, check spelling".format(variable))

        var = getattr(module, variable)

        if type(var) != var_type:
            raise AssertionError("'{}' is type '{}', expected '{}'".format(variable, type(var), var_type))

    def assertIsSubclass(self, sub_class, parent_class):
        """ Asserts that a class is a subclass of the parent class
        Parameters:
            sub_class: The subclass to check
            parent_class: The parent class
        """
        self.assertTrue(issubclass(sub_class, parent_class))


class ResultTests(A2TestClass):
    """ test the Result class"""

    @classmethod
    def setUpClass(cls):
        cls.test_no = 0
        super(ResultTests, cls).setUpClass()

    def testMethodsDefined(self):
        """ test method stubs"""
        self.assertMethodDefined(entities.Result, "get_medal", 1)
        self.assertMethodDefined(entities.Result, "get_place", 1)
        self.assertMethodDefined(entities.Result, "get_result", 1)
        self.assertMethodDefined(entities.Result, "places_determined", 1)
        self.assertMethodDefined(entities.Result, "set_place", 2)

    def testGetResult(self):
        """ test get_result """
        self.assertEqual(entities.Result(1.3).get_result(), "1.3")

    def testPlacesDetermined(self):
        """ test places_determined """
        res1 = entities.Result(4.2)
        self.assertFalse(res1.places_determined())
        res1.set_place(4)
        self.assertTrue(res1.places_determined())

    def testGetPlace(self):
        """ test get_place """
        res1 = entities.Result(4.4)
        with self.assertRaises(RuntimeError):
            res1.get_place()
        res1.set_place(4)
        self.assertEqual(res1.get_place(), "4")

    def testGetMedal(self):
        """ test get_medal """
        res1 = entities.Result(542)
        with self.assertRaises(RuntimeError):
            res1.get_medal()
        res1.set_place(3)
        self.assertEqual(res1.get_medal(), "Bronze")


class CountryTests(A2TestClass):
    """ test the Country class"""

    @classmethod
    def setUpClass(cls):
        cls.test_no = 1
        super(CountryTests, cls) .setUpClass()

    def testMethodsDefined(self):
        """ test method stubs"""
        self.assertMethodDefined(entities.Country, "add_athlete", 2)
        self.assertMethodDefined(entities.Country, "add_athletes", 2)
        self.assertMethodDefined(entities.Country, "get_athletes", 1)
        self.assertMethodDefined(entities.Country, "get_country_code", 1)
        self.assertMethodDefined(entities.Country, "get_name", 1)

    def testGetName(self):
        """ test get_name"""
        self.assertEqual(entities.Country("Canada", "CAN").get_name(), "Canada")

    def testGetCountryCode(self):
        """ test get_country_code"""
        self.assertEqual(entities.Country("Australia", "AUS").get_country_code(), "AUS")

    def testAthletes(self):
        """ test add_athlete and get_athletes"""
        country1 = entities.Country("Canada", "CAN")
        ath1 = entities.Athlete("1635", "John", "Smith", country1)
        self.assertEqual(country1.get_athletes(), [])
        country1.add_athlete(ath1)
        self.assertEqual(country1.get_athletes(), [ath1])


class AthleteTests(A2TestClass):
    """ test the Athlete class"""

    @classmethod
    def setUpClass(cls):
        cls.test_no = 2
        super(AthleteTests, cls).setUpClass()

    def testMethodsDefined(self):
        """ test method stubs """
        self.assertMethodDefined(entities.Athlete, "get_result", 2)
        self.assertMethodDefined(entities.Athlete, "add_result", 3)
        self.assertMethodDefined(entities.Athlete, "add_event", 2)
        self.assertMethodDefined(entities.Athlete, "add_events", 2)
        self.assertMethodDefined(entities.Athlete, "get_events", 1)

    def testID(self):
        """ test get_id"""
        country1 = entities.Country("Canada", "CAN")
        self.assertEqual(entities.Athlete("12345", "John", "Smith", country1).get_id(), "12345")

    def testName(self):
        """ test get_full_name"""
        country1 = entities.Country("Canada", "CAN")
        self.assertEqual(entities.Athlete("12345", "John", "Smith", country1).get_full_name(),
                         "John Smith")

    def testCountry(self):
        """ test get_country"""
        country1 = entities.Country("Canada", "CAN")
        self.assertEqual(entities.Athlete("12345", "John", "Smith", country1).get_country(), country1)

    def testEvents(self):
        """ test get_events and add_event"""
        country1 = entities.Country("Canada", "CAN")
        athlete1 = entities.Athlete("12345", "John", "Smith", country1)
        self.assertEqual(athlete1.get_events(), [])
        event1 = entities.Event("Skiing", False, [])
        athlete1.add_event(event1)
        self.assertEqual(athlete1.get_events(), [event1])

    def testResults(self):
        """ test get_result and add_result"""
        country1 = entities.Country("Canada", "CAN")
        athlete1 = entities.Athlete("12345", "John", "Smith", country1)
        event1 = entities.Event("Skiing", False, [])
        athlete1.add_event(event1)
        result1 = entities.Result(15.1)
        athlete1.add_result(event1, result1)
        self.assertEqual(athlete1.get_result(event1), result1)


class EventTests(A2TestClass):
    """ test the Event class"""

    @classmethod
    def setUpClass(cls):
        cls.test_no = 3
        super(EventTests, cls).setUpClass()

    def testMethodsDefined(self):
        """ test  method stubs"""
        self.assertMethodDefined(entities.Event, "add_athlete", 2)
        self.assertMethodDefined(entities.Event, "add_athletes", 2)
        self.assertMethodDefined(entities.Event, "get_athletes", 1)
        self.assertMethodDefined(entities.Event, "get_name", 1)
        self.assertMethodDefined(entities.Event, "is_timed", 1)

    def testIsTimed(self):
        """ test is_timed"""
        self.assertTrue(entities.Event("Skiing", True, []).is_timed())

    def testGetName(self):
        """ test get_name"""
        self.assertEqual(entities.Event("Skiing", True, []).get_name(), "Skiing")

    def testAthlete(self):
        """ test add_athlete and get_athletes"""
        country1 = entities.Country("Canada", "CAN")
        athlete1 = entities.Athlete("1635", "John", "Smith", country1)
        event1 = entities.Event("Skiing", True, [])
        self.assertEqual(event1.get_athletes(), [])
        event1.add_athlete(athlete1)
        self.assertEqual(event1.get_athletes(), [athlete1])


class AthleteResultsTests(A2TestClass):
    """ Tests the AthleteResults class"""

    @classmethod
    def setUpClass(cls):
        cls.test_no = 4
        super(AthleteResultsTests, cls).setUpClass()

    def testMethodStubs(self):
        """ test method stubs"""
        self.assertIsSubclass(processing.AthleteResults, processing.ProcessResults)
        self.assertMethodDefined(processing.AthleteResults, "process", 1)
        self.assertMethodDefined(processing.AthleteResults, "get_usage_ratio", 0)
        self.assertMethodDefined(processing.AthleteResults, "get_results", 1)

    def testGetResults(self):
        """ test get_results"""
        athleteResults = processing.AthleteResults(entities.Athlete("12345", "John", "Smith",
                                                                    entities.Country("Canada", "CAN")))
        with self.assertRaises(ValueError):
            athleteResults.get_results()

    def testProcessing(self):
        """ test athlete processing """
        country1 = entities.Country("Canada", "CAN")
        athlete1 = entities.Athlete("12345", "John", "Smith", country1)
        event1 = entities.Event("Skiing 2000m", True, [athlete1])
        event2 = entities.Event("Skiing 4000m", True, [athlete1])
        event3 = entities.Event("Asking 6000m", True, [athlete1])
        athlete1.add_event(event1)
        athlete1.add_event(event2)
        athlete1.add_event(event3)
        result1 = entities.Result(28.4)
        result2 = entities.Result(60.47)
        result3 = entities.Result(174.3)
        result1.set_place(15)
        result2.set_place(7)
        result3.set_place(12)
        athlete1.add_result(event1, result1)
        athlete1.add_result(event2, result2)
        athlete1.add_result(event3, result3)
        athleteProcessing = processing.AthleteResults(athlete1)
        athleteProcessing.process()
        self.assertEqual(athleteProcessing.get_results(),
                         [result2, result3, result1])

    def testUsageRatio(self):
        """ test get_usage_ratio """
        self.assertAlmostEqual(processing.AthleteResults.get_usage_ratio(), 1)


class EventResultsTests(A2TestClass):
    """ Tests the EventResults class"""

    @classmethod
    def setUpClass(cls):
        cls.test_no = 5
        super(EventResultsTests, cls).setUpClass()

    def testMethodStubs(self):
        """ test method stubs"""
        self.assertIsSubclass(processing.EventResults, processing.ProcessResults)
        self.assertMethodDefined(processing.EventResults, "process", 1)
        self.assertMethodDefined(processing.EventResults, "get_usage_ratio", 0)
        self.assertMethodDefined(processing.EventResults, "get_results", 1)

    def testGetResults(self):
        """ test get_results"""
        eventResults = processing.EventResults(entities.Event("Skiing", False, []))
        with self.assertRaises(ValueError):
            eventResults.get_results()

    def testProcessing(self):
        """ test event processing """
        country1 = entities.Country("Canada", "CAN")
        athlete1 = entities.Athlete("12345", "John", "Smith", country1)
        athlete2 = entities.Athlete("12346", "David", "Smith", country1)
        athlete3 = entities.Athlete("12347", "Thomas", "Jones", country1)
        event1 = entities.Event("Skiing 2000m", True, [])
        result1 = entities.Result(28.4)
        result2 = entities.Result(60.47)
        result3 = entities.Result(174.3)
        result1.set_place(8)
        result2.set_place(5)
        result3.set_place(10)
        athlete1.add_event(event1)
        athlete2.add_event(event1)
        athlete3.add_event(event1)
        athlete1.add_result(event1, result1)
        athlete2.add_result(event1, result2)
        athlete3.add_result(event1, result3)
        event1.add_athlete(athlete1)
        event1.add_athlete(athlete2)
        event1.add_athlete(athlete3)
        eventProcessing = processing.EventResults(event1)
        eventProcessing.process()
        self.assertEqual(eventProcessing.get_results(),
                         [athlete2, athlete1, athlete3])

    def testUsageRatio(self):
        """ test get_usage_ratio """
        self.assertAlmostEqual(processing.EventResults.get_usage_ratio(), 0.5)


class CountryResultsTests(A2TestClass):
    """ Tests the CountryResults class"""

    @classmethod
    def setUpClass(cls):
        cls.test_no = 6
        super(CountryResultsTests, cls).setUpClass()

    def testMethodStubs(self):
        """ test method stubs """
        self.assertIsSubclass(processing.CountryResults, processing.ProcessResults)
        self.assertMethodDefined(processing.CountryResults, "process", 1)
        self.assertMethodDefined(processing.CountryResults, "get_usage_ratio", 0)
        self.assertMethodDefined(processing.CountryResults, "get_results", 1)
        self.assertMethodDefined(processing.CountryResults, "get_num_gold", 1)
        self.assertMethodDefined(processing.CountryResults, "get_num_silver", 1)
        self.assertMethodDefined(processing.CountryResults, "get_num_bronze", 1)
        self.assertMethodDefined(processing.CountryResults, "get_num_athletes", 1)

    def testGetResults(self):
        """ Test get_results fails before processing is called. """
        countryResults = processing.CountryResults(entities.Country("Canada", "CAN"))
        with self.assertRaises(ValueError):
            countryResults.get_results()

    def _processing_setup(self) :
        """ Create a country with athletes and results to test processing. """
        country1 = entities.Country("Canada", "CAN")
        athlete1 = entities.Athlete("12345", "John", "Smith", country1)
        athlete2 = entities.Athlete("12346", "David", "Smith", country1)
        athlete3 = entities.Athlete("12347", "Thomas", "Jones", country1)
        event1 = entities.Event("Skiing 2000m", True, [])
        result1 = entities.Result(28.4)
        result2 = entities.Result(60.47)
        result3 = entities.Result(174.3)
        result1.set_place(2)
        result2.set_place(3)
        result3.set_place(10)
        athlete1.add_event(event1)
        athlete2.add_event(event1)
        athlete3.add_event(event1)
        athlete1.add_result(event1, result1)
        athlete2.add_result(event1, result2)
        athlete3.add_result(event1, result3)
        country1.add_athlete(athlete1)
        country1.add_athlete(athlete2)
        country1.add_athlete(athlete3)
        event1.add_athlete(athlete1)
        event1.add_athlete(athlete2)
        event1.add_athlete(athlete3)
        return country1

    def testProcessing(self):
        """ Test country processing. """
        country1 = self._processing_setup()
        countryProcessing = processing.CountryResults(country1)
        countryProcessing.process()
        self.assertEqual(countryProcessing.get_results(), [0, 1, 1, 3])
        self.assertEqual(countryProcessing.get_num_gold(), 0)

    def testUsageRatio(self):
        """ test get_usage_ratio """
        self.assertAlmostEqual(processing.CountryResults.get_usage_ratio(), 0.3333333)


class DeterminePlacesTests(A2TestClass):
    """ Tests the DeterminPlaces class"""

    @classmethod
    def setUpClass(cls):
        cls.test_no = 7
        super(DeterminePlacesTests, cls).setUpClass()

    def testMethodStubs(self):
        """ test method stubs"""
        self.assertIsSubclass(processing.DeterminePlaces, processing.ProcessResults)
        self.assertMethodDefined(processing.DeterminePlaces, "process", 1)
        self.assertMethodDefined(processing.DeterminePlaces, "get_usage_ratio", 0)
        self.assertMethodDefined(processing.DeterminePlaces, "get_results", 1)

    def testGetResults(self):
        """ test get_results"""
        placeResults = processing.DeterminePlaces(entities.Event("Skiing 2000m", True, []))
        with self.assertRaises(ValueError):
            placeResults.get_results()

    def testProcessing(self):
        """ test place processing """
        country1 = entities.Country("Canada", "CAN")
        athlete1 = entities.Athlete("12345", "John", "Smith", country1)
        athlete2 = entities.Athlete("12346", "David", "Smith", country1)
        athlete3 = entities.Athlete("12347", "Thomas", "Jones", country1)
        event1 = entities.Event("Skiing 2000m", True, [])
        result1 = entities.Result(128.4)
        result2 = entities.Result(60.47)
        result3 = entities.Result(174.3)
        athlete1.add_event(event1)
        athlete2.add_event(event1)
        athlete3.add_event(event1)
        athlete1.add_result(event1, result1)
        athlete2.add_result(event1, result2)
        athlete3.add_result(event1, result3)
        event1.add_athlete(athlete1)
        event1.add_athlete(athlete2)
        event1.add_athlete(athlete3)
        places = processing.DeterminePlaces(event1)
        places.process()
        self.assertEqual(places.get_results(), [athlete2, athlete1, athlete3])
        self.assertEqual(result1.get_place(), "2")
        self.assertEqual(result2.get_place(), "1")

    def testUsageRatio(self):
        """ test get_usage_ratio """
        self.assertAlmostEqual(processing.DeterminePlaces.get_usage_ratio(), 0.25)


class LoadDataTests(A2TestClass):
    """ Tests the loadData function """

    @classmethod
    def setUpClass(cls):
        cls.test_no = 8
        super(LoadDataTests, cls).setUpClass()
        setUpTestFiles1()

    @classmethod
    def tearDownClass(cls):
        tearDownTestFiles()

    def testFunction(self):
        """ tests function and variables """
        self.assertDefined(entities, "load_data", FunctionType)
        self.assertDefined(entities, "all_countries", entities.ManagedDictionary)
        self.assertDefined(entities, "all_events", entities.ManagedDictionary)
        self.assertDefined(entities, "all_athletes", entities.ManagedDictionary)

    def testLoadData(self):
        """ tests load_data"""
        # entities.load_data(os.path.join("data_files", "athletes.csv"),
        #                   os.path.join("data_files", "countries.csv"),
        #                   os.path.join("data_files", "events.csv"),
        #                   os.path.join("data_files", "timed_event_results.csv"),
        #                   os.path.join("data_files", "scored_event_results.csv"))
        entities.load_data("athletes.test", "countries.test", "events.test",
                           "timed_event_results.test", "scored_event_results.test")
        self.assertEqual(len(entities.all_athletes.get_items()), 84, msg='wrong number of athletes loaded from file')
        self.assertEqual(len(entities.all_countries.get_items()), 16, msg='wrong number of countries loaded from file')
        self.assertEqual(len(entities.all_events.get_items()), 15, msg='wrong number of events loaded from file')

    def testProcessing(self):
        """ test data processing from loaded file"""
        for event in entities.all_events.get_items():
            processing.DeterminePlaces(event).process()

        countryProcessing = processing.CountryResults(entities.all_countries.find_item("GER"))
        countryProcessing.process()
        self.assertEqual(countryProcessing.get_results(), [1, 1, 1, 3])

        eventProcessing = processing.EventResults(entities.all_events.find_item("Men's Speedskating 5000m"))
        eventProcessing.process()
        self.assertEqual(eventProcessing.get_results(), [entities.all_athletes.find_item("60"),
                                                         entities.all_athletes.find_item("54"),
                                                         entities.all_athletes.find_item("61")])

        athlete50 = entities.all_athletes.find_item("50")
        athleteProcessing = processing.AthleteResults(athlete50)
        athleteProcessing.process()
        self.assertEqual(athleteProcessing.get_results(), [athlete50.get_result(entities.all_events.find_item("Men's Speedskating 500m")),
                                                           athlete50.get_result(entities.all_events.find_item("Men's Speedskating 1000m"))])


class AssignmentMaster(TestMaster):
    """ Runs the tests """

    def prepare(self):
        self._tests = [
            ResultTests,
            CountryTests,
            AthleteTests,
            EventTests,
            AthleteResultsTests,
            EventResultsTests,
            CountryResultsTests,
            DeterminePlacesTests,
            LoadDataTests
        ]

        for test_case in self._tests:
            setattr(test_case, "_module", self._module)


if __name__ == "__main__":
    print(f"Tests version: {__version__}")
    testrunner = AssignmentMaster()
    testrunner.main()
