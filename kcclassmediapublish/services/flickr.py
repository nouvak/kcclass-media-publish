import logging
import flickrapi

from kcclassmediapublish.metadata.publish_metadata import PublishMetadata,\
    Access
from kcclassmediapublish.metadata.list_metadata import ListMetadata

log = logging.getLogger( __name__ )

class FlickrService:
    
    def __init__(self, username, password):
        self.username = username
        self.password = password
        api_key = 'cbc982c7bc51e3572083335231bb0a31'
        api_secret = '38231b4ff8f9edc0'
        self.flickr_service = flickrapi.FlickrAPI(api_key, api_secret)
        (token, frob) = self.flickr_service.get_token_part_one(perms='delete')
        if not token:
            raw_input("Press ENTER after you authorized this program")
        self.flickr_service.get_token_part_two((token, frob))
        
    def __get_category_id(self, category_name):
        """
        Get a reference to a category whose name is equal to category_name.
        """
        photosets = self.flickr_service.photosets_getList()
        for photosets_entry in photosets.find('photosets'):
            if photosets_entry.find('title').text == category_name:
                return photosets_entry.attrib['id']
        return None
    
    def __get_privacy_flags(self, access):
        """
        Get Flickr privacy flags based on access level.
        """
        privacy_flags = {}
        if access == Access.PUBLIC:
            privacy_flags['is_public'] = u'1'
            privacy_flags['is_family'] = u'1'
            privacy_flags['is_friend'] = u'1'
        else:
            privacy_flags['is_public'] = u'0'
            privacy_flags['is_family'] = u'0'
            privacy_flags['is_friend'] = u'0'
        return privacy_flags
    
    @staticmethod
    def __add_quotes(str):
        return '"' + str + '"'
        
    def publish(self, filepath, pub_metadata):
        """
        Publish the slide to the Slideshare cloud.
        """
        assert isinstance(filepath, basestring), "filepath is not string: " + str(filepath)
        assert isinstance(pub_metadata, PublishMetadata), "pub_metadata is not PublishMetadata" + str(pub_metadata)
        log.debug("Publishing Flickr image: %s, %s" % (filepath, str(pub_metadata)))
        category_id = self.__get_category_id(pub_metadata.category)
        if category_id is None:
            raise Exception("Category doesn't exist: %s" % pub_metadata.category)
        # upload image
        quotes_enclosed_tags = [FlickrService.__add_quotes(tag) for tag in pub_metadata.tags]
        str_tags = " ".join(quotes_enclosed_tags)
        privacy_flags = self.__get_privacy_flags(pub_metadata.access)
        result = self.flickr_service.upload(filename=filepath, 
                                            title=pub_metadata.title, 
                                            description=pub_metadata.description,
                                            tags=str_tags,
                                            is_public=privacy_flags['is_public'], 
                                            is_family=privacy_flags['is_family'], 
                                            is_friend=privacy_flags['is_friend'])
        image_id = result.find('photoid').text
        self.flickr_service.photosets_addPhoto(photoset_id=category_id, photo_id=image_id)
        log.debug("Publishing succeeded.")
        return image_id

    
    def unpublish(self, image_id):
        """
        Unpublish the image from the PicassaWeb cloud.
        """
        log.debug("Unpublishing Flickr image: %s" % str(image_id))
        result = self.flickr_service.photos_delete(photo_id=image_id)
        if result.attrib['stat'] != 'ok':
            raise Exception("Unpublishing failed.")
        log.debug("Unpublishing succeeded.")

    def list(self, category=None):
        """
        Return a list of published slideshows in Flickr cloud for the given user.
        """
        log.debug("Listing the uploaded Flickr photos.")
        photos = []
        if category is None:
            user_id = self.flickr_service.people_findByEmail(find_email=self.username).find('user').get('nsid')
            entries = self.flickr_service.people_getPhotos(user_id=user_id).find('photos').findall('photo')
        else:
            category_id = self.__get_category_id(category)
            entries = self.flickr_service.walk_set(category_id)

        for entry in entries:
            photo_id = entry.get('id')
            photo_info = self.flickr_service.photos_getInfo(photo_id=photo_id)
            title = entry.get('title')
            description = photo_info.find('photo').find('description').text
            category = None
            tags = []
            for tag in photo_info.find('photo').find('tags').findall('tag'):
                tags.append(tag.text)
            photo_metadata = ListMetadata(id=photo_id, title=title, 
                                          description=description,
                                          tags=tags, category=category)
            photos.append(photo_metadata)

        return photos