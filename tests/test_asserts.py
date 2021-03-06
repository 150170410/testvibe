
import nose

import testvibe


class BasicTestSuite(testvibe.Testsuite):

    def test_equal(self, v1, v2):
        self.assert_equal(v1, v2)

    def test_equal_alias_1(self, v1, v2):
        self.assert_eq(v1, v2)  # just a link to assert_equal

    def test_equal_alias_2(self, v1, v2):
        self.a_eq(v1, v2)  # just link to assert_equal

    def test_not_equal(self, v1, v2):
        self.assert_not_equal(v1, v2)

    def test_not_equal_alias_1(self, v1, v2):
        self.assert_neq(v1, v2)  # just a link to assert_equal

    def test_not_equal_alias_2(self, v1, v2):
        self.a_neq(v1, v2)  # just link to assert_equal

    def test_null(self, v):
        self.assert_null(v)

    def test_null_alias_1(self, v):
        self.a_null(v)

    def test_not_null(self, v):
        self.assert_not_null(v)

    def test_not_null_alias_1(self, v):
        self.a_not_null(v)

    def test_true(self, v):
        self.assert_true(v)

    def test_true_alias_1(self, v):
        self.a_true(v)

    def test_false(self, v):
        self.assert_false(v)

    def test_false_alias_1(self, v):
        self.a_false(v)

    def test_in(self, v, l):
        self.assert_in(v, l)

    def test_in_alias_1(self, v, l):
        self.a_in(v, l)

    def test_not_in(self, v, l):
        self.assert_not_in(v, l)

    def test_not_in_alias_1(self, v, l):
        self.a_not_in(v, l)

    def test_greater_than(self, v1, v2):
        self.assert_greater_than(v1, v2)

    def test_greater_than_alias_1(self, v1, v2):
        self.assert_gt(v1, v2)

    def test_greater_than_alias_2(self, v1, v2):
        self.a_gt(v1, v2)

    def test_greater_than_or_equal(self, v1, v2):
        self.assert_greater_than_or_equal(v1, v2)

    def test_greater_than_or_equal_alias_1(self, v1, v2):
        self.assert_gte(v1, v2)

    def test_greater_than_or_equal_alias_2(self, v1, v2):
        self.a_gte(v1, v2)

    def test_lesser_than(self, v1, v2):
        self.assert_lesser_than(v1, v2)

    def test_lesser_than_alias_1(self, v1, v2):
        self.assert_lt(v1, v2)

    def test_lesser_than_alias_2(self, v1, v2):
        self.a_lt(v1, v2)

    def test_lesser_than_or_equal(self, v1, v2):
        self.assert_lesser_than_or_equal(v1, v2)

    def test_lesser_than_or_equal_alias_1(self, v1, v2):
        self.assert_lte(v1, v2)

    def test_lesser_than_or_equal_alias_2(self, v1, v2):
        self.a_lte(v1, v2)

    def test_is_a_number(self, v):
        self.assert_is_a_number(v)

    def test_is_a_number_alias1(self, v):
        self.assert_is_n(v)

    def test_is_a_number_alias2(self, v):
        self.a_is_n(v)


class TestAsserts(object):

    t = None

    def setUp(self):
        self.t = BasicTestSuite()

    def tearDown(self):
        self.t = None

    def test_equal(self):
        self.t.test_equal(9, 9)
        self.t.test_equal_alias_1(9, 9)
        self.t.test_equal_alias_2(9, 9)

    @nose.tools.raises(testvibe.asserts.AssertionExceptionEqual)
    def test_neg_equal(self):
        self.t.test_equal(1, 3)

    # NOTE(niklas9):
    # * need a second test case for the alias since after the raise
    #   in the first line of test_neg_assert_equal any other statement
    #   won't be executed
    @nose.tools.raises(testvibe.asserts.AssertionExceptionEqual)
    def test_neg_equal_alias_1(self):
        self.t.test_equal_alias_1(1, 3)

    @nose.tools.raises(testvibe.asserts.AssertionExceptionEqual)
    def test_neg_equal_alias_2(self):
        self.t.test_equal_alias_2(6, 7)

    def test_not_equal(self):
        self.t.test_not_equal(9, 10)
        self.t.test_not_equal_alias_1(77, 777)
        self.t.test_not_equal_alias_2(1023, 10.23)

    @nose.tools.raises(testvibe.asserts.AssertionExceptionNotEqual)
    def test_neg_not_equal(self):
        self.t.test_not_equal(3, 3)

    @nose.tools.raises(testvibe.asserts.AssertionExceptionNotEqual)
    def test_neg_not_equal_alias_1(self):
        self.t.test_not_equal_alias_1(55, 55.0)

    @nose.tools.raises(testvibe.asserts.AssertionExceptionNotEqual)
    def test_neg_not_equal_alias_2(self):
        self.t.test_not_equal_alias_2(99999, 99999)

    def test_null(self):
        self.t.test_null(None)
        self.t.test_null_alias_1(None)

    def test_true(self):
        self.t.test_true(True)
        self.t.test_true_alias_1(True)

    @nose.tools.raises(testvibe.asserts.AssertionExceptionIsNotTrue)
    def test_neg_true(self):
        self.t.test_true(False)

    @nose.tools.raises(testvibe.asserts.AssertionExceptionIsNotTrue)
    def test_neg_true_alias_1(self):
        self.t.test_true_alias_1(False)

    def test_false(self):
        self.t.test_false(False)
        self.t.test_false_alias_1(False)

    @nose.tools.raises(testvibe.asserts.AssertionExceptionIsNotFalse)
    def test_neg_false(self):
        self.t.test_false(True)

    @nose.tools.raises(testvibe.asserts.AssertionExceptionIsNotFalse)
    def test_neg_false_alias_1(self):
        self.t.test_false_alias_1(True)

    @nose.tools.raises(testvibe.asserts.AssertionExceptionIsNull)
    def test_neg_null(self):
        self.t.test_null('None')

    @nose.tools.raises(testvibe.asserts.AssertionExceptionIsNull)
    def test_neg_null_alias_1(self):
        self.t.test_null_alias_1('None')

    def test_not_null(self):
        self.t.test_not_null('None')
        self.t.test_not_null_alias_1('None')

    @nose.tools.raises(testvibe.asserts.AssertionExceptionIsNotNull)
    def test_neg_not_null(self):
        self.t.test_not_null(None)

    @nose.tools.raises(testvibe.asserts.AssertionExceptionIsNotNull)
    def test_neg_not_null_alias_1(self):
        self.t.test_not_null_alias_1(None)

    def test_in(self):
        self.t.test_in('a', ['c', 'b', 'a'])

    @nose.tools.raises(testvibe.asserts.AssertionExceptionIn)
    def test_neg_in(self):
        self.t.test_in('None', ('f', 'c', 'enoN'))

    @nose.tools.raises(testvibe.asserts.AssertionExceptionIn)
    def test_neg_in_alias_1(self):
        self.t.test_in_alias_1('None', ('f', 'c', 'enoN'))

    def test_not_in(self):
        self.t.test_not_in('a', ['c', 'b', '0'])

    @nose.tools.raises(testvibe.asserts.AssertionExceptionNotIn)
    def test_neg_not_in(self):
        self.t.test_not_in('None', ('f', 'None', 'enoN'))

    @nose.tools.raises(testvibe.asserts.AssertionExceptionNotIn)
    def test_neg_not_in_alias_1(self):
        self.t.test_not_in_alias_1('None', ('f', 'None', 'enoN'))

    def test_greater_than(self):
        self.t.test_greater_than(9, 8)
        self.t.test_greater_than_alias_1(0.2, 0.1)
        self.t.test_greater_than_alias_2(87, 12)

    @nose.tools.raises(testvibe.asserts.AssertionExceptionGreaterThan)
    def test_neg_greater_than(self):
        self.t.test_greater_than(22, 23)

    @nose.tools.raises(testvibe.asserts.AssertionExceptionGreaterThan)
    def test_neg_greater_than_alias_1(self):
        self.t.test_greater_than_alias_1(0.1, 0.2)

    @nose.tools.raises(testvibe.asserts.AssertionExceptionGreaterThan)
    def test_neg_greater_than_alias_2(self):
        self.t.test_greater_than_alias_2(23, 100)

    def test_greater_than_or_equal(self):
        self.t.test_greater_than_or_equal(2, 1)
        self.t.test_greater_than_or_equal(2, 2)
        self.t.test_greater_than_or_equal(1001, 997)

    @nose.tools.raises(testvibe.asserts.AssertionExceptionGreaterThanOrEqual)
    def test_neg_greater_than_or_equal(self):
        self.t.test_greater_than_or_equal(1, 2)

    @nose.tools.raises(testvibe.asserts.AssertionExceptionGreaterThanOrEqual)
    def test_neg_greater_than_or_equal_alias_1(self):
        self.t.test_greater_than_or_equal_alias_1(432, 432.01)

    @nose.tools.raises(testvibe.asserts.AssertionExceptionGreaterThanOrEqual)
    def test_neg_greater_than_or_equal_alias_2(self):
        self.t.test_greater_than_or_equal_alias_2(231, 1000)

    def test_lesser_than(self):
        self.t.test_lesser_than(8, 9)
        self.t.test_lesser_than_alias_1(0.1, 0.2)
        self.t.test_lesser_than_alias_2(11, 88)

    @nose.tools.raises(testvibe.asserts.AssertionExceptionLesserThan)
    def test_neg_lesser_than(self):
        self.t.test_lesser_than(23, 22)

    @nose.tools.raises(testvibe.asserts.AssertionExceptionLesserThan)
    def test_neg_lesser_than_alias_1(self):
        self.t.test_lesser_than_alias_1(0.2, 0.1)

    @nose.tools.raises(testvibe.asserts.AssertionExceptionLesserThan)
    def test_neg_lesser_than_alias_2(self):
        self.t.test_lesser_than_alias_2(100, 23)

    def test_lesser_than_or_equal(self):
        self.t.test_lesser_than_or_equal(1, 2)
        self.t.test_lesser_than_or_equal(2, 2)
        self.t.test_lesser_than_or_equal(996, 1001)

    @nose.tools.raises(testvibe.asserts.AssertionExceptionLesserThanOrEqual)
    def test_neg_lesser_than_or_equal(self):
        self.t.test_lesser_than_or_equal(2, 1)

    @nose.tools.raises(testvibe.asserts.AssertionExceptionLesserThanOrEqual)
    def test_neg_lesser_than_or_equal_alias_1(self):
        self.t.test_lesser_than_or_equal_alias_1(432.01, 432)

    @nose.tools.raises(testvibe.asserts.AssertionExceptionLesserThanOrEqual)
    def test_neg_lesser_than_or_equal_alias_2(self):
        self.t.test_lesser_than_or_equal_alias_2(1000, 231)

    def test_assert_counters(self):
        assert self.t.get_assert_counters() == (0, 0)
        self.t.test_equal('A', 'A')
        assert self.t.get_assert_counters() == (1, 1)
        self.t.test_null(None)
        self.t.test_lesser_than_or_equal(7, 9)
        assert self.t.get_assert_counters() == (3, 3)
        try:
            self.t.test_in(3, [1, 2, 4])
        except testvibe.asserts.AssertionExceptionIn as e:
            pass
        assert self.t.get_assert_counters() == (3, 4)

    def test_assert_counters_reset(self):
        assert self.t.get_assert_counters() == (0, 0)
        self.t.test_equal('A', 'A')
        self.t.reset_assert_counter()
        assert self.t.get_assert_counters() == (0, 0)

    def test_is_a_number(self):
        self.t.test_is_a_number(9)
        self.t.test_is_a_number(9.9)
        self.t.test_is_a_number_alias1(9.5)
        self.t.test_is_a_number_alias2(10)

    @nose.tools.raises(testvibe.asserts.AssertionExceptionIsANumber)
    def test_neg_is_a_number(self):
        self.t.test_is_a_number('234')

