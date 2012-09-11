import logging
import os.path
import gdata.photos.service

from kcclassmediapublish.metadata.publish_metadata import PublishMetadata
from kcclassmediapublish.metadata.list_metadata import ListMetadata

log = logging.getLogger( __name__ )

class PicassawebService:
    
    def __init__(self, username, password):
        self.picasaweb_service = gdata.photos.service.PhotosService()
        # Turn on HTTPS/SSL access.
        # Note: SSL is not available at this time for uploads.
        self.picasaweb_service.ssl = False
        #self.picasaweb_service.developer_key = 'AI39si6-qCVmA8KI53Eg3NF5VjnsvKYzsmzD4njj0VFnQDWgh-Iv0X3h_ABBCAwMWDe_G3VzEHGcTrd6eAy9QBPKBb3CDDDXJw'
        #self.picasaweb_service.client_id = 'kcclass-media-publish'
        self.picasaweb_service.source = 'kcclass-media-publish'
        # authenticate the user.
        self.picasaweb_service.email = username
        self.picasaweb_service.password = password
        self.picasaweb_service.ProgrammaticLogin()
        
    def __get_content_type(self, filepath):
        """
        Get the MIME content type from the file extension.
        """
        file_name, file_extension = os.path.splitext(filepath)
        # trim the leading . of the extension.
        if file_extension.lower() == ".jpg" or file_extension.lower() == ".jpeg":
            return "image/jpeg"
        else:
            raise Exception("Unknown extension: %s" % file_extension)
        
    def __get_category_id(self, albums, category_name):
        """
        Get a reference to a category whose name is equal to category_name.
        """
        for album_entry in albums.entry:
            if album_entry.name.text == category_name:
                return album_entry.gphoto_id.text
        return None
    
    def publish(self, filepath, pub_metadata):
        """
        Publish the image to the PicasaWeb cloud.
        """
        assert isinstance(filepath, basestring), "filepath is not string: " + str(filepath)
        assert isinstance(pub_metadata, PublishMetadata), "pub_metadata is not PublishMetadata" + str(pub_metadata)
        log.debug("Publishing Picassaweb image: %s, %s" % (filepath, str(pub_metadata)))
        # publish image.
        albums = self.picasaweb_service.GetUserFeed()
        category_id = self.__get_category_id(albums, pub_metadata.category)
        if category_id is None:
            raise Exception("Category doesn't exist: %s" % pub_metadata.category)
        album_url = '/data/feed/api/user/%s/albumid/%s' % ('default', category_id)
        tags = ','.join(pub_metadata.tags)
        image_id = self.picasaweb_service.InsertPhotoSimple(album_url, pub_metadata.title, 
            pub_metadata.description, filepath, 
            content_type=self.__get_content_type(filepath),
            keywords=tags)
        # prepare a media group object to hold our video's meta-data
#        if pub_metadata.access == Access.PRIVATE:
#            is_private = gdata.media.Private()
#        else:
#            is_private = None
        log.debug("Publishing succeeded.")
        return image_id.id.text

    
    def unpublish(self, image_id):
        """
        Unpublish the image from the PicassaWeb cloud.
        """
        log.debug("Unpublishing Picassaweb image: %s" % str(image_id))
        image = self.picasaweb_service.GetEntry(image_id)
        self.picasaweb_service.Delete(image)
        log.debug("Unpublishing succeeded.")
        
    def list(self):
        """
        Return a list of published images in PicasaWeb cloud for the given user.
        """
        log.debug("Listing the uploaded Picasa Web photos.")
        feed = self.picasaweb_service.GetUserFeed(kind='photo')
        photos = []
        for entry in feed.entry:
            video_id = entry.id.text
            title = entry.title.text
            description = entry.media.description.text
            if len(entry.media.category) > 0:
                category = entry.media.category[0].text
            else:
                category = None
            if entry.media.keywords.text is None:
                tags = []
            else:
                tags = entry.media.keywords.text.split(",")
            photo_metadata = ListMetadata(id=video_id, title=title, 
                                          description=description,
                                          tags=tags, category=category)
            photos.append(photo_metadata)
        return photos

