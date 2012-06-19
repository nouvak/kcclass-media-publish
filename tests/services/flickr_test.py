import unittest

from kcclassmediapublish.services.flickr import FlickrService
from kcclassmediapublish.metadata.publish_metadata import PublishMetadata, Access

class FlickrServiceTest(unittest.TestCase):

    def setUp(self):
        self.flickr = FlickrService("nouvak.kcclass@gmail.com", "KCClassTest")

    def tearDown(self):
        pass

    def test_publish_and_unpublish(self):
        # publish a sample video.
        publish_metadata = PublishMetadata(title="Marko KCClass test.",
                                           description="Marko's test image for the KC Class project.",
                                           tags=["Marko", "kcclass"],
                                           category="KCClass",
                                           access=Access.PUBLIC)
        image_id = self.flickr.publish("../../sample-data/test-image1.jpg", publish_metadata)
        self.assertTrue(image_id is not None, "Image publishing failed!")
        # unpublish the video that was just published.
        self.flickr.unpublish(image_id)


if __name__ == '__main__':
    unittest.main()