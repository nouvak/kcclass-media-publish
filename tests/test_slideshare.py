# this code uses the "pyslideshare" library.
# you have to add the "kcclass-media-publish/libs" directory to PYTHONPATH first.

import unittest
from pyslideshare import pyslideshare

class SlideshareTest(unittest.TestCase):

    def setUp(self):
        self.username = 'KCClass'
        self.password = 'KCClassTest'
        self.api_key = '3U3jT35d'
        self.secret_key = 'OJLBwzkk'
    
    def tearDown(self):
        pass

    def test_upload_and_delete(self):
        # Use proxy if available
        params = {
            'username': self.username,
            'password': self.password, 
            'api_key': self.api_key,
            'secret_key': self.secret_key
        }    
        obj = pyslideshare.pyslideshare(params, verbose=False)
        json = obj.upload_slideshow(username=self.username, password=self.password, 
                                    slideshow_srcfile='../sample-data/test-slide2.ppt',
                                    slideshow_title='pyslideshare works!')
        assert json is not None
        slide_id = json.SlideShowUploaded.SlideShowID
        # delete the slide.
        obj.delete_slideshow(username=self.username, password=self.password, slideshow_id=slide_id)

if __name__ == '__main__':
    unittest.main()