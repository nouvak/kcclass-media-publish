import unittest

from kcclassmediapublish.services.slideshare import SlideshareService
from kcclassmediapublish.metadata.publish_metadata import PublishMetadata, Access

class SlideshareServiceTest(unittest.TestCase):

    def setUp(self):
        self.slideshare = SlideshareService("KCClass", "KCClassTest")

    def tearDown(self):
        pass

    def test_publish_and_unpublish(self):
        # publish a sample video.
        publish_metadata = PublishMetadata(title="Marko KCClass test.",
                                           description="Marko's test image for the KC Class project.",
                                           tags=["Marko", "kcclass"],
                                           category="KCClass",
                                           access=Access.PUBLIC)
        slide_id = self.slideshare.publish("../../sample-data/test-slide2.ppt", 
                                           publish_metadata)
        self.assertTrue(slide_id is not None, "Image publishing failed!")
        # unpublish the video that was just published.
        self.slideshare.unpublish(slide_id)


if __name__ == '__main__':
    unittest.main()