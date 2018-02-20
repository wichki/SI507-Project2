from proj2_nps import *
import unittest

class TestStateSearch(unittest.TestCase):

    def site_is_in_state_list(self, site_name, site_type, site_list):
        for s in site_list:
            if site_name == s.name and site_type == s.type:
                return True
        return False

    def get_site_from_list(self, site_name, site_list):
        for s in site_list:
            if site_name == s.name:
                return s
        return None

    def test_state_search(self):
        mi_site_list = get_sites_for_state('mi')
        self.assertEqual(len(mi_site_list), 7)
        az_site_list = get_sites_for_state('az')
        self.assertEqual(len(az_site_list), 24)

        self.assertTrue(self.site_is_in_state_list('Isle Royale',
            'National Park', mi_site_list))
        self.assertFalse(self.site_is_in_state_list('Isle Royale',
            'National Park', az_site_list))

        self.assertTrue(self.site_is_in_state_list('Lake Mead',
            'National Recreation Area', az_site_list))
        self.assertFalse(self.site_is_in_state_list('Lake Mead',
            'National Recreation Area', mi_site_list))

        isle_royale = self.get_site_from_list('Isle Royale', mi_site_list)
        lake_mead = self.get_site_from_list('Lake Mead', az_site_list)

        self.assertEqual(isle_royale.address_street, '800 East Lakeshore Drive')
        self.assertEqual(isle_royale.address_city, 'Houghton')
        self.assertEqual(isle_royale.address_zip, '49931')

        self.assertEqual(lake_mead.address_street, '601 Nevada Way')
        self.assertEqual(lake_mead.address_city, 'Boulder City')
        self.assertEqual(lake_mead.address_zip, '89005')


class TestNearbySearch(unittest.TestCase):

    def place_is_in_places_list(self, place_name, places_list):
        for p in places_list:
            if place_name == p.name:
                return True
        return False

    def test_nearby_search(self):
        site1 = NationalSite('National Monument',
            'Sunset Crater Volcano', 'A volcano in a crater.')
        site2 = NationalSite('National Park',
            'Yellowstone', 'There is a big geyser there.')

        nearby_places1 = get_nearby_places_for_site(site1)
        nearby_places2 = get_nearby_places_for_site(site2)

        self.assertTrue(self.place_is_in_places_list('Cinder Lake Landfill', nearby_places1))
        self.assertTrue(self.place_is_in_places_list('Yellowstone General Store', nearby_places2))

if __name__ == '__main__':
    unittest.main()
