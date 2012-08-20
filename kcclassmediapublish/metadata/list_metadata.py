from atom import Id

class ListMetadata:
    """
    This class holds the metadata about the published media.
    """
    def __init__(self, id, title=None, description=None, tags=None, 
                 category=None):
        assert id is None or isinstance(id, Id), "id is not string: " + str(id)
        assert title is None or isinstance(title, basestring), "title is not string: " + str(title)
        assert description is None or isinstance(description, basestring), "description is not string: " + str(description)
        assert tags is None or isinstance(tags, list), "tags is not list: " + str(tags)
        assert category is None or isinstance(category, basestring), "category is not string: " + str(category)
        self.id = id
        self.title = title
        self.description = description
        self.tags = tags
        self.category = category
        
    def __str__(self):
        return "PublishMetadata: id=%s, title=%s, description=%s, tags=%s, category=%s" % \
            (self.id, self.title, self.description, str(self.tags), self.category, str(self.access))