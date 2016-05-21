import logging

logger = logging.getLogger()
logging.level = logging.DEBUG

def initialize_first_team(teams):
    n = len(teams[0])
    opponent = n/2
    for m in xrange(n-1):
        teams[m][0] = opponent
        teams[m][opponent] = 0
        opponent = (opponent + 1) % n
        if opponent == 0:
            opponent += 1

def get_previous(x, n):
    return (x + n - 1) % n

def get_match_from_previous(teams, team, matchday):
    m = get_previous(matchday, len(teams))
    while True:
        if teams[m][team-1] != team:
            return teams[m][team-1]
        m = get_previous(m, len(teams))
    # We should never reach this point
    assert False

def solve(n):
    assert n >= 2
    tournament = []
    teams = [ [None] * n for _ in range(n-1) ]
    initialize_first_team(teams)
    for t in xrange(1, n):
        left = n - t - 1
        matchday = 0
        while left > 0:
            if teams[matchday][t] is None:
                opponent = get_match_from_previous(teams, t, matchday)
                teams[matchday][t] = opponent
                teams[matchday][opponent] = t
                left -= 1
            matchday += 1
    return teams

def get_match_string(a, b):
    return ''.join([ chr(x+ord('A')) for x in [a,b] ])

def generate_calendar(teams):
    calendar = []
    for m in teams:
        matchday = []
        for i,x in enumerate(m):
            if i < x:
                matchday.append(get_match_string(i,x))
        calendar.append(matchday)
    return calendar

def get_calendar(n):
    teams = solve(n)
    return generate_calendar(teams)
