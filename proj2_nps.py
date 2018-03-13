## proj_nps.py
## Skeleton for Project 2, Winter 2018
## ~~~ modify this file, but don't rename it ~~~
import requests
import json
from bs4 import BeautifulSoup
import re
from secrets import *
import plotly.plotly as py

cache_fname = "proj2_cache.json"
try:
    cache_file = open(cache_fname, "r")
    cache_contents = cache_file.read()
    cache_diction = json.loads(cache_contents)
    cache_file.close()
except:
    cache_diction = {}

## you can, and should add to and modify this class any way you see fit
## you can add attributes and modify the __init__ parameters,
##   as long as tests still pass
##
## the starter code is here just to make the tests run (and fail)
class NationalSite():
    def __init__(self, parkType, name, desc, street=None, city=None, state=None, zipcode=None, url=None):
        self.type = parkType
        self.name = name
        self.description = desc
        self.url = url

        # needs to be changed, obvi.
        self.address_street = street
        self.address_city = city
        self.address_state = state
        self.address_zip = zipcode

        self.list_number = None
        self.latitude = None
        self.longitude = None

    def __str__(self):
        return "{} ({}): {}, {}, {} {}".format(self.name, self.type, self.address_street, self.address_city, self.address_state, self.address_zip)

## you can, and should add to and modify this class any way you see fit
## you can add attributes and modify the __init__ parameters,
##   as long as tests still pass
##
## the starter code is here just to make the tests run (and fail)
class NearbyPlace():
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return "{}".format(self.name)
## Must return the list of NationalSites for the specified state
## param: the 2-letter state abbreviation, lowercase
##        (OK to make it work for uppercase too)
## returns: all of the NationalSites
##        (e.g., National Parks, National Heritage Sites, etc.) that are listed
##        for the state at nps.gov
def check_cache(unique_id):
    # baseURL = "https://www.nps.gov"
    if unique_id in cache_diction:
        # print("Getting cached data...")
        return cache_diction[unique_id]
    else:
        print("Making a request for new data...")
        response = requests.get(unique_id).text
        cache_diction[unique_id] = response
        dumped_json_cache = json.dumps(cache_diction)
        f = open(cache_fname,"w")
        f.write(dumped_json_cache)
        f.close()
        return cache_diction[unique_id]

def get_sites_for_state(state_abbr):
    baseURL = "https://www.nps.gov"
    unique_id = baseURL + "/state/" + state_abbr

    cache_nps_homepage = check_cache("https://www.nps.gov/index.htm")
    npsHTML = BeautifulSoup(cache_nps_homepage, "html.parser")
    statesList = npsHTML.find(class_="dropdown-menu SearchBar-keywordSearch")
    findOneStateLink = statesList.find("a", href=re.compile(state_abbr))

    stateURL = baseURL + findOneStateLink["href"]
    data = check_cache(stateURL)
    stateHTML = BeautifulSoup(data, "html.parser")
    # print(stateHTML)
    parkList = stateHTML.find("div", id="parkListResults")
    # print(parkList)

    state_park_object_list = []
    for i in parkList.find_all("li", class_="clearfix"):
        try:
            parkName = i.find("h3").find("a").text
            # print(parkName)
        except:
            # parkName = "NAME ERROR"
            # print(parkName)
            pass

        try:
            parkType = i.find("h2").text
                # if parkType == "":
                #     parkType = "No park type!"
            # if parkType == "":
            #     parkType = "NO TYPE"
            # print(parkType)
        except:
            # parkType = "TYPE ERROR"
            # print(parkType)
            pass

        try:
            parkRelURL = i.find("h3").find("a")["href"]
            parkURL = "https://www.nps.gov" + parkRelURL
        except:
            # parkURL = "URL ERROR"
            pass

        try:
            parkDescription = i.find("p").text.strip()
        except:
            # parkDescription = "No description"
            pass

        # print(parkName, parkType, parkURL, parkDescription)
        # print(i.text)

        #get basic info for one park
        # print(parkURL)
        # print(parkSection)
        # print(oneParkHTML)

        oneParkBasicInfo = check_cache(parkURL)
        oneParkHTML = BeautifulSoup(oneParkBasicInfo, "html.parser")
        parkSection = oneParkHTML.find("div", class_="ParkFooter-contact")

        # print(parkSection)

        try:
            streetAddress = parkSection.find("span", class_="street-address").text.strip()
            city = parkSection.find(itemprop="addressLocality").text.strip()
            state = parkSection.find(itemprop="addressRegion").text.strip()
            zipcode = parkSection.find(itemprop="postalCode").text.strip()
        except:
            streetAddress = "No street address!"
            city = "No city!"
            state = "No state!"
            zipcode = "No zipcode!"

        state_park_object_list.append(NationalSite(parkType, parkName, parkDescription, streetAddress, city, state, zipcode))
        # print(parkName, parkType, streetAddress, city, state, zipcode)
    #
    # for i in state_park_object_list:
    #     print(i.__str__())

    return state_park_object_list

#################

    # name = parkList.find("a")
    # print(name.text)
    # print(oneState)
    # print(states)
    # print(npsHTML)
    # return []

# get_sites_for_state("mi")

## Must return the list of NearbyPlaces for the specifite NationalSite
## param: a NationalSite object
## returns: a list of NearbyPlaces within 10km of the given site
##          if the site is not found by a Google Places search, this should
##          return an empty list
def get_nearby_places_for_site(national_site):
    # first get GPS coordinates
    textBaseURL = "https://maps.googleapis.com/maps/api/place/textsearch/json?query="
    # params = {"key":google_places_key}
    parkName = national_site.name
    parkType = national_site.type
    textPlaceURL = textBaseURL + parkName + parkType + "&key=" + google_places_key
    # gpsResponse = requests.get(baseURL + parkName + parkType, params).text
    gpsResponse = json.loads(check_cache(textPlaceURL))
    # print(gpsResponse)
    longitude = gpsResponse["results"][0]["geometry"]["location"]["lng"]
    latitude = gpsResponse["results"][0]["geometry"]["location"]["lat"]
    print(latitude, longitude)

    placesBaseURL = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?"
    radius = "20"
    placesSearchURL = placesBaseURL + "location=" + str(latitude) + "," + str(longitude) + "&radius=" + radius + "&key=" + google_places_key
    print(placesSearchURL)
    nearbyPlacesResponse = json.loads(check_cache(placesSearchURL))
    # print(nearbyPlacesResponse)
    # print(type(placesResponse))

    nearby_results_list = []
    for i in nearbyPlacesResponse["results"]:
        name = i["name"]
        # print(name)
        nearby_results_list.append(NearbyPlace(name))

    return nearby_results_list

# d = get_nearby_places_for_site(get_sites_for_state("az")[18])
site_list_objects = get_sites_for_state("ca")
# for i in site_list_objects:
#     print(i)
sunset = site_list_objects[9]
# print(sunset.name, sunset.type)
nearby_sunset = get_nearby_places_for_site(sunset)
# print(nearby_sunset.__str__())
# for i in nearby_sunset:
#     print(i)

# print(d)

# for i in z:
#     print(i)


## Must plot all of the NationalSites listed for the state on nps.gov
## Note that some NationalSites might actually be located outside the state.
## If any NationalSites are not found by the Google Places API they should
##  be ignored.
## param: the 2-letter state abbreviation
## returns: nothing
## side effects: launches a plotly page in the web browser
def plot_sites_for_state(state_abbr):
    state_sites = get_sites_for_state(state_abbr)
    # # print(state_sites)
    park_names = []
    lat_vals = []
    lng_vals = []

    for i in state_sites:
        textBaseURL = "https://maps.googleapis.com/maps/api/place/textsearch/json?query="
        parkName = i.name
        parkType = i.type
        textPlaceURL = textBaseURL + parkName + parkType + "&key=" + google_places_key
        gpsResponse = json.loads(check_cache(textPlaceURL))

        for j in gpsResponse["results"]:
            # print(i["geometry"]["location"])
            latitude = j["geometry"]["location"]["lat"]
            longitude = j["geometry"]["location"]["lng"]
            # adds latitude and longitude to NationalSite instance variable
            i.latitude = latitude
            i.longitude = longitude
            # print(parkName, latitude, longitude)

    for i in state_sites:
        if i.latitude == None and i.longitude == None:
            pass
        else:
            #now we have a list of NationalSits with GPS coordinates
            park_names.append(i.name)
            lat_vals.append(i.latitude)
            lng_vals.append(i.longitude)

    data = [dict(
    type = "scattergeo",
    locationmode = "USA-states",
    lon = lng_vals,
    lat = lat_vals,
    text = park_names,
    mode = "markers",
    marker = dict(
        size = 8,
        opacity = 0.8,
        reversescale = True,
        autocolorscale = False,
        symbol = "star")
    )]

    layout = dict(
    title = 'National Parks',
    geo = dict(
        scope='usa',
        projection=dict( type='albers usa' ),
    showland = True,
    landcolor = "rgb(250, 250, 250)",
    subunitcolor = "rgb(100, 217, 217)",
    countrycolor = "rgb(217, 100, 217)",
    # lataxis = {'range': lat_axis},
    # lonaxis = {'range': lon_axis},
    countrywidth = 3,
    subunitwidth = 3
        ),
    )

    fig = dict(data=data, layout=layout)
    py.plot(fig, validate=False)

    # trace1 =
    # print(park_names)
    # print(lat_vals)
    # print(lng_vals)

# plot_sites_for_state("ca")

## Must plot up to 20 of the NearbyPlaces found using the Google Places API
## param: the NationalSite around which to search
## returns: nothing
## side effects: launches a plotly page in the web browser
one_site = get_sites_for_state("ca")[1]
# print(one_site.latitude)

def plot_nearby_for_site(site_object):
    nearbyPlacesForOneSite = get_nearby_places_for_site(site_object)
    # print(oneSite)
    # for i in oneSite:
    #     print(i)

    textBaseURL = "https://maps.googleapis.com/maps/api/place/textsearch/json?query="
    parkName = site_object.name
    parkType = site_object.type
    # print(parkName, parkType)
    textPlaceURL = textBaseURL + parkName + parkType + "&key=" + google_places_key
    gpsResponse = json.loads(check_cache(textPlaceURL))
    # print(gpsResponse)
    latitude = gpsResponse["results"][0]["geometry"]["location"]["lat"]
    longitude = gpsResponse["results"][0]["geometry"]["location"]["lng"]
    print(latitude, longitude)

# plot_nearby_for_site(one_site)

# plot_nearby_for_site()
