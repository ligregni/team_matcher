import unittest
from app.team_matcher import get_calendar
import app.team_matcher as team_matcher

class Judge:
    def __init__(self, ut, n=0, calendar=None):
        self.ut = ut
        self.n = n
        self.calendar = calendar
        self.matches = set()

    def get_match(self, s):
        return ''.join(sorted(s))

    def verify_matchday(self, matches):
        self.ut.assertEqual(len(matches), self.n / 2,
            msg='Not enough matches on this matchday')
        teams = set()
        for match in matches:
            for team in match:
                self.ut.assertNotIn(team, teams,
                    msg='Team {} plays two matches on the same matchday!'.format(
                        team))
                teams.add(team)

    def verify_matches_against_previous_matches(self, matches):
        for m in matches:
            match = self.get_match(m)
            self.ut.assertNotIn(match, self.matches,
                msg='Same match occurs more than once in the tournament: {} {}'
                    .format(match, self.calendar))
            self.matches.add(match)

    def verify_calendar(self):
        for matchday in self.calendar:
            self.verify_matchday(matchday)
            self.verify_matches_against_previous_matches(matchday)

class JudgeTest(unittest.TestCase):
    def test_get_match(self):
        judge = Judge(self)
        self.assertEqual(judge.get_match('AB'), 'AB')
        self.assertEqual(judge.get_match('BA'), 'AB')

    def test_verify_matchday(self):
        judge = Judge(self, 6, [])
        judge.verify_matchday(['AB', 'CD', 'EF'])
        with self.assertRaisesRegexp(AssertionError,
            'Team D plays two matches on the same matchday!'):
            judge.verify_matchday(['AB', 'CD', 'DF'])

    def test_verify_matches_against_previous_matches_good(self):
        judge = Judge(self, 6, [])
        judge.verify_matches_against_previous_matches(['AB', 'CD', 'EF'])
        judge.verify_matches_against_previous_matches(['AC', 'BE', 'DF'])
        judge.verify_matches_against_previous_matches(['AD', 'BF', 'CE'])

    def test_verify_matches_against_previous_matches_same_day(self):
        judge = Judge(self, 6, [])
        with self.assertRaisesRegexp(AssertionError,
            'Same match occurs more than once in the tournament: AB'):
            judge.verify_matches_against_previous_matches(['AB', 'CD', 'BA'])

    def test_verify_matches_against_previous_matches_other_day(self):
        judge = Judge(self, 6, [])
        judge.verify_matches_against_previous_matches(['AB', 'BE', 'DF'])
        with self.assertRaisesRegexp(AssertionError,
            'Same match occurs more than once in the tournament: AB'):
            judge.verify_matches_against_previous_matches(['BA', 'CD', 'EF'])

class MatcherTest(unittest.TestCase):
    def test_get_previous(self):
        self.assertEqual(team_matcher.get_previous(1, 4), 0)
        self.assertEqual(team_matcher.get_previous(3, 4), 2)
        self.assertEqual(team_matcher.get_previous(0, 4), 3)

    def test_get_match_string(self):
        self.assertEqual(team_matcher.get_match_string(0, 3), 'AD')
        self.assertEqual(team_matcher.get_match_string(0, 1), 'AB')
        self.assertEqual(team_matcher.get_match_string(1, 5), 'BF')

    def test_get_match_from_previous(self):
        self.assertEqual(team_matcher.get_match_from_previous(
            [[2, None, 0, None], [3, None, None, 0], [1, 0, None, None]], 1, 0), 
            3)
        self.assertEqual(team_matcher.get_match_from_previous(
            [[2, 3, 0, 1], [3, None, None, 0], [1, 0, None, None]], 1, 1),
            2)

    def test_get_calendar(self):
        judge = Judge(self, 2, team_matcher.get_calendar(2))
        judge.verify_calendar()
        judge = Judge(self, 4, team_matcher.get_calendar(4))
        judge.verify_calendar()
        judge = Judge(self, 14, team_matcher.get_calendar(14))
        judge.verify_calendar()
