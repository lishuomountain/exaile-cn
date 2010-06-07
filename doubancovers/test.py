from tests.base import BaseTestCase
from tests.cover import CoverBaseTestCase
import doubancovers

class DoubanCoverTestCase(CoverBaseTestCase):
    def setUp(self):
        CoverBaseTestCase.setUp(self)
        self.cm.add_search_method(doubancovers.DoubanCoverSearch())

    def testDoubanCovers(self):
        track = self.collection.search('Now the day is over')[0]
        self.cm.set_preferred_order(['douban'])

        covers = self.cm.find_covers(track, limit=2)

        assert len(covers) == 2, "Douban cover search failed"
