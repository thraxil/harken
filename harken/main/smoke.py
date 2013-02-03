from smoketest import SmokeTest


class DemoTest(SmokeTest):
    def setUp(self):
        print "ran setUp"

    def tearDown(self):
        print "ran teardown"

    def test_nothing(self):
        print "ran test_nothing"
        self.assertTrue(True)

    def test_always_fail(self):
        self.assertTrue(False)
