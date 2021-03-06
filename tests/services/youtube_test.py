import unittest

from kcclassmediapublish.services.youtube import YoutubeService
from kcclassmediapublish.metadata.publish_metadata import PublishMetadata, Access

class YoutubeServiceTest(unittest.TestCase):

    def setUp(self):
        self.youtube = YoutubeService("nouvak.kcclass@gmail.com", "KCClassTest")

    def tearDown(self):
        pass

    def test_publish_and_unpublish(self):
        # publish a sample video.
        publish_metadata = PublishMetadata(title="Marko KCClass test.",
                                           description="Marko's test movie for the KC Class project.",
                                           tags=["Marko", "kcclass"],
                                           category="Education",
                                           access=Access.PUBLIC)
        video_id = self.youtube.publish("../../sample-data/test-video1.flv", publish_metadata)
        self.assertTrue(video_id is not None, "Video publishing failed!")
        # list the uploaded videos.
        videos = self.youtube.list()
        self.assertTrue(len(videos) > 0, "Number of published videos should be greater than 0.")
        # unpublish the video that was just published.
        self.youtube.unpublish(video_id)


if __name__ == '__main__':
    unittest.main()