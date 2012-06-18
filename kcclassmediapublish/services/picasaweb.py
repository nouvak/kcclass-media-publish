import logging
import os.path
import gdata.photos.service

from kcclassmediapublish.metadata.publish_metadata import PublishMetadata,\
    Access

log = logging.getLogger( __name__ )

class PicassawebService:
    
    def __init__(self):
        self.picassaweb_service = gdata.photos.service.PhotosService()
        # Turn on HTTPS/SSL access.
        # Note: SSL is not available at this time for uploads.
        self.picassaweb_service.ssl = False
        #self.picassaweb_service.developer_key = 'AI39si6-qCVmA8KI53Eg3NF5VjnsvKYzsmzD4njj0VFnQDWgh-Iv0X3h_ABBCAwMWDe_G3VzEHGcTrd6eAy9QBPKBb3CDDDXJw'
        #self.picassaweb_service.client_id = 'kcclass-media-publish'
        self.picassaweb_service.source = 'kcclass-media-publish'
        
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
        for album_entry in albums.entry:
            if album_entry.name.text == category_name:
                return album_entry.gphoto_id.text
        return None
    
    def publish(self, username, password, filepath, pub_metadata):
        """
        Publish the image to the PicasaWeb cloud.
        """
        assert isinstance(filepath, basestring), "filepath is not string: " + str(filepath)
        assert isinstance(pub_metadata, PublishMetadata), "pub_metadata is not PublishMetadata" + str(pub_metadata)
        log.debug("Publishing Picassaweb image: %s, %s" % (filepath, str(pub_metadata)))
        # authenticate the user.
        self.picassaweb_service.email = username
        self.picassaweb_service.password = password
        self.picassaweb_service.ProgrammaticLogin()
        # publish image.
        albums = self.picassaweb_service.GetUserFeed()
        category_id = self.__get_category_id(albums, pub_metadata.category)
        if category_id is None:
            raise Exception("Category doesn't exist: %s" % pub_metadata.category)
        album_url = '/data/feed/api/user/%s/albumid/%s' % ('default', category_id)
        image_id = self.picassaweb_service.InsertPhotoSimple(album_url, pub_metadata.title, 
            pub_metadata.description, filepath, 
            content_type=self.__get_content_type(filepath))

        # prepare a media group object to hold our video's meta-data
#        if pub_metadata.access == Access.PRIVATE:
#            is_private = gdata.media.Private()
#        else:
#            is_private = None
        log.debug("Publishing succeeded.")
        return image_id

    
    def unpublish(self, image_id):
        """
        Unpublish the image from the PicassaWeb cloud.
        """
        log.debug("Unpublishing Picassaweb image: %s" % str(image_id))
        self.picassaweb_service.Delete(image_id)
        log.debug("Unpublishing succeeded.")
