class Access:
    PRIVATE=0
    PUBLIC=1

class PublishMetadata:
    """
    This class holds the metadata that is passed to the service when the
    media is uploaded. Not all the data attributes have to be set.
    """
    def __init__(self, title=None, description=None, tags=None, 
                 category=None, access=Access.PUBLIC):
        assert title is None or isinstance(title, basestring), "title is not string: " + str(title)
        assert description is None or isinstance(description, basestring), "description is not string: " + str(description)
        assert tags is None or isinstance(tags, list), "tags is not list: " + str(tags)
        assert category is None or isinstance(category, basestring), "category is not string: " + str(category)
        self.title = title
        self.description = description
        self.tags = tags
        self.category = category
        self.access = access
        
    def __str__(self):
        return "PublishMetadata: title=%s, description=%s, tags=%s, category=%s, access=%s" % \
            (self.title, self.description, str(self.tags), self.category, str(self.access))