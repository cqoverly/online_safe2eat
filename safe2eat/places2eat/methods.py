import urllib
import urllib2
import httplib
from bs4 import BeautifulSoup
try:
    import json
except ImportError:
    import simplejson as json

API_KEY = 'AIzaSyCFNabJBDvXBcMzetmQU715yByGRExw1Mw'
TEXT_URL = 'https://maps.googleapis.com/maps/api/place/textsearch/json?'
NEARBY_URL = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?'
BASE_URL = 'http://info.kingcounty.gov/health/ehs/foodsafety/inspections/XmlRest.aspx?'

#==================== MANAGEMENT ====================================

def patch_http_response_read(func):
    """
    This function is purely a patch to get around an error created on the inspection site server.
    The error created in the get_report() method was an httplib.IncompleteRead exception. Solution was
    found through stackoverflow which referenced the following link where the path is shown:

        http://bobrochel.blogspot.com/2010/11/bad-servers-chunked-encoding-and.html

    Patch was written by the creator of the blog.  Thanks! Saved my day.
    """

    def inner(*args):
        try:
            return func(*args)
        except httplib.IncompleteRead, e:
            return e.partial

    return inner

httplib.HTTPResponse.read = patch_http_response_read(httplib.HTTPResponse.read)
#================ SEARCH FOR RESTAURANTS IN THE AREA ===================

def get_start_loc(address):
    # Takes an address and converts it to a tuple containg latitude and longitude of address.
    params = urllib.urlencode({'query': address, 'sensor': 'false', 'key': API_KEY})
    url = TEXT_URL+params
    res = urllib2.urlopen(url)
    info = json.loads(res.read())
    lat, lng = (info['results'][0]['geometry']['location']['lat'], info['results'][0]['geometry']['location']['lng'])
    return '%s,%s' % (lat, lng)


def get_list(coords, miles):
    """
    Calls Google Places API to generate list (limited to 20 by google without extra code)
    of restaurants within the miles passed in the args. Coordinates were created by the get_start_loc(addresss)
    method.
    """

    radius = miles * 1609  # converts miles to meters, as needed by google API.
    params = urllib.urlencode({'location': coords, 'radius': radius, 'types': 'restaurant', 'sensor': 'false', 'key': API_KEY})

    search_url = NEARBY_URL + params
    # print search_url

    res = urllib2.urlopen(search_url)
    search_list = res.read()
    return json.loads(search_list)  #  return pythonized results.


def process_list(search_list):
    """
    Takes pythonized json list of restaurants and their info and places it into a list
    of dicts, each dict holding the information for one listing. This dict will be added to
    with inspection information.
    """
    rest_info = []  #  List to hold dicts of attributes for each restauraing in list.
    for rest in search_list['results']:  # Generate dict for each listing.
        restaurant = dict()
        restaurant['Name'] = rest['name']
        try:
            restaurant['Rating'] = rest['rating']    #  See if listing has attribute.
        except KeyError:
            pass                                     #  Keep going without adding attribute.
        try:
            restaurant['Price Level'] = rest['price_level']  #  Same as above
        except KeyError:
            pass
        restaurant['Address'] = rest['vicinity']

        rest_info.append(restaurant)  # Add dict to list of restaurants.
    return rest_info


#=============  GET INSPECTION REPORT ========================

def get_report(restaurant_name, address):
    """
    Use King County Health site REST interaface, returns results in xml.
    Parse results with BeautifulSoup
    King County server is a flawed HTTP implementations, so patch is used to help get past
    the IncompleteRead error that kept the urllib2.urlopen(Url).read() from completing.
    """

    # httplib.HTTPResponse.read = patch_http_response_read(httplib.HTTPResponse.read)
    name = restaurant_name
    addr = address
    split_addr = addr.split()
    search_addr = split_addr[0]  # + ' ' + split_addr[1]
    # print 'SEARCH ADDRES: ', search_addr
    # params = urllib.urlencode({'Business_Name': name})
    params = urllib.urlencode({'Business_Name': name, 'Business_Address': search_addr})
    url = BASE_URL + params
    # print url


    res = urllib2.urlopen(url)

    try:
        res = urllib2.urlopen(url)
        soup = BeautifulSoup(res)
        return soup
    except httplib.IncompleteRead, m:
        return m

def process_report(info, name, addr):
    """
    Takes the parsed report for the restaurant passed to get_report() and parses the values
    for each inspection item to be used in final output for restaurant listing. The info argument
    is a BeautifulSoup object holding the xml code.
    """

    listing = info.find('business')
    if not listing:
        return "No inspection information found."

    inspections = info.find_all('inspection') # Get list of all inspections.
    for i in inspections:
        if i.find('inspection_result').text.strip() != 'Complete':  # 'Complete' only used for
            last_inspect = i                                        #  training visits. Not real
            break                                                   #  inspections.
                                                                    #  Moves code to the first
                                                                    #  real inspection.

    inspect_date = last_inspect.find('inspection_date').text              #  First non 'Complete'
    inspect_result = last_inspect.find('inspection_result').text.strip()  #  inspection is what we want.

    if inspect_result == 'Unsatisfactory':
        score = last_inspect.find('inspection_score').text.strip()
        violations = last_inspect.find_all('violation')
        v_list = []
        for v in violations:
            desc =  v.find('violation_descr').text.strip() + ": " + str(v.find('violation_points').text) + "pts"
            v_list.append(desc)
        return (inspect_date, inspect_result, score, v_list)
