

import testvibe

class BasicTestSuite(testvibe.TestSuite):  pass


class TestSetupTeardown(object):

    t = None

    def setUp(self):
        self.t = BasicTestSuite()

    def tearDown(self):
        self.t = None

    def test_class_type(self):
        assert isinstance(self.t, testvibe.TestSuite)