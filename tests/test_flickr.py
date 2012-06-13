# this code uses the "flickrapi" library.
# you have to install that first:
#   pip install flickrapi

import flickrapi
import os
import sys
import unittest

class FlickrTest(unittest.TestCase):

    def setUp(self):
        api_key = 'cbc982c7bc51e3572083335231bb0a31'
        api_secret = '38231b4ff8f9edc0'
        self.flickr = flickrapi.FlickrAPI(api_key, api_secret)
        (token, frob) = self.flickr.get_token_part_one(perms='delete')
        if not token:
            raw_input("Press ENTER after you authorized this program")
        self.flickr.get_token_part_two((token, frob))

    def tearDown(self):
        pass
    
    def test_list_photosets(self):
        photosets = self.flickr.photosets_getList()
        assert photosets.attrib['stat'] == 'ok'
        assert len(photosets.find('photosets')) > 0

    def test_upload_and_delete(self):
        photosets = self.flickr.photosets_getList()
        photoset_id = photosets.find('photosets')[0].attrib['id']
        self.update_photosets(photoset_id, ['../sample-data/test-image1.jpg', '../sample-data/test-image2.gif'])
        
    def update_photosets(self, photoset_id, to_upload):
        """
        set max_uploads to 1 while debugging to upload only one photo per run
        """
        photos = []
        for photo in to_upload:
            result = self.flickr.upload(filename=photo, title='KC Class test', description='KC Class testing images.', is_public=u'1', is_family=u'1', is_friend=u'1')
            photo_id = result.find('photoid').text
            photos.append(photo_id)
            self.flickr.photosets_addPhoto(photoset_id=photoset_id, photo_id=photo_id)
        # delete the images.
        for photo_id in photos:
            result = self.flickr.photos_delete(photo_id=photo_id)
            assert result.attrib['stat'] == 'ok'
    
if __name__ == '__main__':
    unittest.main()