import unittest
import time
from kcclassmediapublish.services.picasaweb import PicassawebService
from kcclassmediapublish.metadata.publish_metadata import PublishMetadata, Access

class PicassawebServiceTest(unittest.TestCase):

    def setUp(self):
        self.picasaweb = PicassawebService("nouvak.kcclass@gmail.com", "KCClassTest")

    def tearDown(self):
        pass

    def test_publish_and_unpublish(self):
        # publish a sample video.
        publish_metadata = PublishMetadata(title="Marko KCClass test.",
                                           description="Marko's test image for the KC Class project.",
                                           tags=["Marko", "kcclass"],
                                           category="KCClass",
                                           access=Access.PUBLIC)
        image_id = self.picasaweb.publish("../../sample-data/test-image1.jpg", publish_metadata)
        self.assertTrue(image_id is not None, "Image publishing failed!")
        # list the uploaded videos.
        photos = self.picasaweb.list()
        self.assertTrue(len(photos) > 0, "Number of published videos should be greater than 0.")
        # unpublish the video that was just published.
        self.picasaweb.unpublish(image_id)


if __name__ == '__main__':
    unittest.main()