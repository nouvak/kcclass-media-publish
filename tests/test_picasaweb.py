import unittest
import gdata.media
import gdata.photos.service

class YoutubeTest(unittest.TestCase):

    def setUp(self):
        self.username = 'nouvak.kcclass@gmail.com'
        self.password = 'KCClassTest'
        self.lh2_service = gdata.photos.service.PhotosService()
        # Turn on HTTPS/SSL access.
        # Note: SSL is not available at this time for uploads.
        self.lh2_service.ssl = False
        # Authenticate using your Google email address and password.
        #self.lh2_service.ClientLogin(self.username, self.password)
        #self.lh2_service.developer_key = 'AI39si6-qCVmA8KI53Eg3NF5VjnsvKYzsmzD4njj0VFnQDWgh-Iv0X3h_ABBCAwMWDe_G3VzEHGcTrd6eAy9QBPKBb3CDDDXJw'
        #self.lh2_service.client_id = 'kcclass-media-publish'
        self.lh2_service.email = self.username
        self.lh2_service.password = self.password
        self.lh2_service.source = 'kcclass-media-publish'
        self.lh2_service.ProgrammaticLogin()

    def tearDown(self):
        pass
    
    def test_get_albums_list(self):
        albums = self.lh2_service.GetUserFeed()
        for album in albums.entry:
            print 'title: %s, number of photos: %s, id: %s' % (album.title.text,
                                                               album.numphotos.text, 
                                                               album.gphoto_id.text)
    def test_get_photos(self):
        albums = self.lh2_service.GetUserFeed()
        for album in albums.entry:
            photos = self.lh2_service.GetFeed('/data/feed/api/user/%s/albumid/%s?kind=photo' % (
                'default', album.gphoto_id.text))
            for photo in photos.entry:
                print 'Photo title:', photo.title.text

    def test_upload_and_delete(self):
        albums = self.lh2_service.GetUserFeed()
        album_url = '/data/feed/api/user/%s/albumid/%s' % ('default', albums.entry[0].gphoto_id.text)
        image_file_location = '../sample-data/test-image1.jpg'
        photo = self.lh2_service.InsertPhotoSimple(album_url, 'Marko KCClass test', 
            "Marko's test movie for the KC Class project.", image_file_location, 
            content_type='image/jpeg')
        # list the uploaded videos.
        #photos = self.lh2_service.GetFeed('/data/feed/api/user/%s/albumid/%s?kind=photo' % (
        #    'default', albums.entry[0].gphoto_id.text))
        #for photos_item in photos.entry:
        #    print 'Photo title:', photos_item.title.text
        photos = self.lh2_service.GetUserFeed(kind='photo')
        for photos_item in photos.entry:
            print 'Recently added photo title:', photos_item.title.text
        # delete the photo.
        self.lh2_service.Delete(photo)

if __name__ == '__main__':
    unittest.main()