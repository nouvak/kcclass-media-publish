import unittest

from kcclassmediapublish.services.picasaweb import PicassawebService
from kcclassmediapublish.metadata.publish_metadata import PublishMetadata, Access

class PicassawebServiceTest(unittest.TestCase):

    def setUp(self):
        self.picassaweb = PicassawebService()

    def tearDown(self):
        pass

    def test_publish_and_unpublish(self):
        # publish a sample video.
        publish_metadata = PublishMetadata(title="Marko KCClass test.",
                                           description="Marko's test image for the KC Class project.",
                                           tags=["Marko", "kcclass"],
                                           category="Education",
                                           access=Access.PUBLIC)
        image_id = self.picassaweb.publish("nouvak.kcclass@gmail.com", "KCClassTest", 
                             "../../sample-data/test-image1.jpg", publish_metadata)
        self.assertTrue(image_id is not None, "Image publishing failed!")
        # unpublish the video that was just published.
        self.picassaweb.unpublish(image_id)


if __name__ == '__main__':
    unittest.main()