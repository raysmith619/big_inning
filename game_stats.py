# game_stats.py

import re

from select_error import SelectError

fn_date = 1
fn_game_no = 2
fn_day_of_week = 3
fn_v_team = 4
fn_v_league = 5
fn_v_game_no = 6
fn_h_team = 7
fn_h_league = 8
fn_h_game_no = 9
fn_v_game_score = 10
fn_h_game_score = 11
fn_game_len_outs = 12
fn_day_night = 13
fn_game_complete = 14
fn_forfeit = 15
fn_protest = 16
fn_park_id = 17
fn_attendance = 18
fn_time_of_game = 19
fn_v_line_score = 20
fn_h_line_score = 21
"""  Complete field mapping and access functinos """


class TeamInfo:
    
    def __init__(self, gs, team='h'):
        """ Team information
        :team: w - winning team, if one
               l - loosing team, if one
               h - home team
               v = visitor
               
        if winloose = 'w':
            self.date = gs.date()
            self.game_no = gs.game_no()
            self.day_of_week = gs.day_of_week()
            self.team = gs.
        """
        self.date = 0
        self.year = 0
        self.mth_no = 0
        self.mth_day_no = 0
        self.game_no = 0
        self.day_of_week = 0
        self.team = ""
        self.league = ""
        self.game_score = ""
        self.game_len_outs = 0
        self.day_night = 0
        self.game_complete = 0
        self.forfeit = ""
        self.protest = ""
        self.park_id = 0
        self.attendance = 0
        self.time_of_game = 0
        self.line_score =    0
        self.tie_game = False
        self.win_loss = "?"
        self.inning_scores = []
             
        if team == 'w':
            if gs.h_game_score() > gs.v_game_score():
                team = 'h'
                self.win = True
            elif gs.h_game_score() < gs.v_game_score():
                team = 'v'
                self.win = True
            else:
                team = 'h'
                self.tie_game = True
        elif team == 'l':
            if gs.h_game_score() < gs.v_game_score():
                team = 'h'
                self.win = True
            elif gs.h_game_score() > gs.v_game_score():
                team = 'v'
                self.win = True
            else:
                team = 'h'
                self.tie_game = True
        
        team_type = team
        self.team_type = team_type
        self.date = gs.date()
        self.day_of_week = gs.day_of_week()
        self.year = gs.year()
        self.mth_no = gs.mth_no()
        self.mth_day_no = gs.mth_day_no()
        self.game_len_outs = gs.game_len_outs()
        self.forfeit = gs.forfeit()
        self.park_id = gs.park_id()
        self.attendance = gs.attendance()
        self.time_of_game = gs.time_of_game()
        self.game_complete = gs.game_complete()
        self.day_night = gs.day_night()
        self.game_complete = gs.game_complete()
        
        if team_type == 'h':
            self.game_no = gs.h_game_no()
            self.team = gs.h_team()
            self.league = gs.h_league()
            self.game_score = gs.h_game_score()
            self.line_score = gs.h_line_score()
            self.inning_scores = gs.h_inning_scores()
            if self.game_score > gs.v_game_score():
                self.win = True
            elif self.game_score < gs.v_game_score():
                self.win = False
            else:
                self.tie_game = True    
        elif team_type == 'v':
            self.game_no = gs.v_game_no()
            self.team = gs.v_team()
            self.league = gs.v_league()
            self.game_score = gs.v_game_score()
            self.line_score = gs.v_line_score()
            self.inning_scores = gs.v_inning_scores()
            if self.game_score > gs.h_game_score():
                self.win = True
            elif self.game_score < gs.h_game_score():
                self.win = False
            else:
                self.tie_game = True
        else:
            raise SelectError("Unrecognized team info team '%s' in %s" % (team, gs.row))

                    
class GameStats:
    n_skipped = 0
    n_processed = 0
    
    def __init__(self, row):
        """ Input from parsed csv file
        """

        self.row = row
        """ Do some sanity checking score == total line
        """
        if not self.is_ok():
            GameStats.n_skipped += 1
            return
        
        GameStats.n_processed += 1
        
        v_score = self.v_game_score()
        v_inning_scores = self.v_inning_scores()
        v_isum = sum(v_inning_scores)
        if v_score != v_isum:
            raise SelectError("visitor score(%d) != sum of innings(%d) date: %s %s @ %s"
                              % (v_score, v_isum, self.date(),
                                 self.v_team(), self.h_team()))
        
        h_score = self.h_game_score()
        h_inning_scores = self.h_inning_scores()
        h_isum = sum(h_inning_scores)
        if h_score != h_isum:
            raise SelectError("home score(%d) != sum of innings(%d) date: %s %s @ %s"
                              % (h_score, h_isum, self.date(),
                                 self.h_team(), self.h_team()))
        
    def is_ok(self):
        """ Sanity check
        We will ignore if not
        """
        if (len(self.v_inning_scores()) == 0
             or len(self.h_inning_scores()) == 0):
            return False
    
        return True
    
    
     
    def date(self):
        return self.row[fn_date-1]
    
    def game_no(self):
        return self.row[fn_game_no-1]
        
    def day_of_week(self):
        return self.row[fn_day_of_week-1]
    
    def v_team(self):
        return self.row[fn_v_team-1]
    
    def v_league(self):
        return self.row[fn_v_league-1]
    
    def v_game_no(self):
        return self.row[fn_v_game_no-1]
    
    def h_team(self):
        return self.row[fn_h_team-1]
    
    def h_league(self):
        return self.row[fn_h_league-1]
    
    def h_game_no(self):
        return self.row[fn_h_game_no-1]
    
    def v_game_score(self):
        return int(self.row[fn_v_game_score-1])
    
    def h_game_score(self):
        return int(self.row[fn_h_game_score-1])
    
    def game_len_outs(self):
        return self.row[fn_game_len_outs-1]
    
    def day_night(self):
        return self.row[fn_day_night-1]

    def game_complete(self):
        return self.row[fn_game_complete-1]

    def forfeit(self):
        return self.row[fn_forfeit-1]

    def protest(self):
        return self.row[fn_protest-1]

    def park_id(self):
        return self.row[fn_park_id-1]

    def attendance(self):
        return self.row[fn_attendance-1]

    def time_of_game(self):
        return self.row[fn_time_of_game-1]

    def v_line_score(self):
        return self.row[fn_v_line_score-1]

    def h_line_score(self):
        return self.row[fn_h_line_score-1]

    def year(self):
        return int(self.date()[0:3])

    def mth_no(self):
        return int(self.date()[4:5])

    def mth_day_no(self):
        return int(self.date()[6:7])

    def v_inning_scores(self):
        """ Inning scores
        """
        return self.line2innings(self.v_line_score())

    def h_inning_scores(self):
        """ Inning scores
        """
        return self.line2innings(self.h_line_score())

    def team_infos(self, teams=None):
        """ Get teams info based on win/loss
        :teams: (w-win, l-loose, h-home, v-visitor
        :returns: list of team infos
        """
        if teams is None:
            teams = 'wl'
        infos = []
        for tm in teams:
            infos.append(TeamInfo(self, tm))
        return infos
        
    def array_to_str(self, array):
        ret = ""
        for member in array:
            if ret == "":
                ret = "["
            else:
                ret += ","
            ret += str(member)
        ret += "]"
        return ret
    
            
    def line2innings(self, line_score, show_x=False):
        """ Convert line score to list of innings
        :line_score: string of digits with possible "x" at end
        :show_x:  show x(non played inning)
                default: set nonplayed as 0
        :returns:" list of integers (-1 for x)
        """
        inn_iter = re.finditer(r'\d|\(\d+\)|x', line_score)
        innings = []
        for inning_match in inn_iter:
            inning = inning_match.group(0)
            mat = re.fullmatch(r'\((\d+)\)', inning)
            if mat is not None:
                inning = mat.group(1)
            elif inning == 'x':
                if show_x:
                    pass
                else:
                    inning= "0"
            elif re.fullmatch(r'\d+', inning):
                pass
            try:
                inn_score = int(inning)
            except:
                raise SelectError(
                    "Unrecognized line_score:%s with %s"
                                     % (line_score, inning))
            innings.append(inn_score)
        return innings
            

    def raw_interest(self):
        """ string of raw interesting stats
        """
        str_str = (self.date()
               + " " + self.v_team()
               + " @ " + self.h_team()
               + " visitor line: " + self.v_line_score()
               + " = " + self.array_to_str(self.v_inning_scores())
               + " home line: " + self.h_line_score()
               + " = " + self.array_to_str(self.h_inning_scores())
               )
        return str_str
            

    def summary(self):
        """ string of summary stats
        """
        str_str = (self.date()
               + " " + self.v_team()
               + " @ " + self.h_team()
               + " visitor: " + self.v_line_score()
               + " home: " + self.h_line_score()
               )
        return str_str

"""
Field format
From:
https://www.retrosheet.org/gamelogs/glfields.txt 

Field(s)  Meaning
    1     Date in the form "yyyymmdd"
    2     Number of game:
             "0" -- a single game
             "1" -- the first game of a double (or triple) header
                    including seperate admission doubleheaders
             "2" -- the second game of a double (or triple) header
                    including seperate admission doubleheaders
             "3" -- the third game of a triple-header
             "A" -- the first game of a double-header involving 3 teams
             "B" -- the second game of a double-header involving 3 teams
    3     Day of week  ("Sun","Mon","Tue","Wed","Thu","Fri","Sat")
  4-5     Visiting team and league
    6     Visiting team game number
          For this and the home team game number, ties are counted as
          games and suspended games are counted from the starting
          rather than the ending date.
  7-8     Home team and league
    9     Home team game number
10-11     Visiting and home team score (unquoted)
   12     Length of game in outs (unquoted).  A full 9-inning game would
          have a 54 in this field.  If the home team won without batting
          in the bottom of the ninth, this field would contain a 51.
   13     Day/night indicator ("D" or "N")
   14     Completion information.  If the game was completed at a
          later date (either due to a suspension or an upheld protest)
          this field will include:
             "yyyymmdd,park,vs,hs,len" Where
          yyyymmdd -- the date the game was completed
          park -- the park ID where the game was completed
          vs -- the visitor score at the time of interruption
          hs -- the home score at the time of interruption
          len -- the length of the game in outs at time of interruption
          All the rest of the information in the record refers to the
          entire game.
   15     Forfeit information:
             "V" -- the game was forfeited to the visiting team
             "H" -- the game was forfeited to the home team
             "T" -- the game was ruled a no-decision
   16     Protest information:
             "P" -- the game was protested by an unidentified team
             "V" -- a disallowed protest was made by the visiting team
             "H" -- a disallowed protest was made by the home team
             "X" -- an upheld protest was made by the visiting team
             "Y" -- an upheld protest was made by the home team
          Note: two of these last four codes can appear in the field
          (if both teams protested the game).
   17     Park ID
   18     Attendance (unquoted)
   19     Time of game in minutes (unquoted)
20-21     Visiting and home line scores.  For example:
             "010000(10)0x"
          Would indicate a game where the home team scored a run in
          the second inning, ten in the seventh and didn't bat in the
          bottom of the ninth.
22-38     Visiting team offensive statistics (unquoted) (in order):
             at-bats
             hits
             doubles
             triples
             homeruns
             RBI
             sacrifice hits.  This may include sacrifice flies for years
                prior to 1954 when sacrifice flies were allowed.
             sacrifice flies (since 1954)
             hit-by-pitch
             walks
             intentional walks
             strikeouts
             stolen bases
             caught stealing
             grounded into double plays
             awarded first on catcher's interference
             left on base
39-43     Visiting team pitching statistics (unquoted)(in order):
             pitchers used ( 1 means it was a complete game )
             individual earned runs
             team earned runs
             wild pitches
             balks
44-49     Visiting team defensive statistics (unquoted) (in order):
             putouts.  Note: prior to 1931, this may not equal 3 times
                the number of innings pitched.  Prior to that, no
                putout was awarded when a runner was declared out for
                being hit by a batted ball.
             assists
             errors
             passed balls
             double plays
             triple plays
50-66     Home team offensive statistics
67-71     Home team pitching statistics
72-77     Home team defensive statistics
78-79     Home plate umpire ID and name
80-81     1B umpire ID and name
82-83     2B umpire ID and name
84-85     3B umpire ID and name
86-87     LF umpire ID and name
88-89     RF umpire ID and name
          If any umpire positions were not filled for a particular game
          the fields will be "","(none)".
90-91     Visiting team manager ID and name
92-93     Home team manager ID and name
94-95     Winning pitcher ID and name
96-97     Losing pitcher ID and name
98-99     Saving pitcher ID and name--"","(none)" if none awarded
100-101   Game Winning RBI batter ID and name--"","(none)" if none
          awarded
102-103   Visiting starting pitcher ID and name
104-105   Home starting pitcher ID and name
106-132   Visiting starting players ID, name and defensive position,
          listed in the order (1-9) they appeared in the batting order.
133-159   Home starting players ID, name and defensive position
          listed in the order (1-9) they appeared in the batting order.
  160     Additional information.  This is a grab-bag of informational
          items that might not warrant a field on their own.  The field 
          is alpha-numeric. Some items are represented by tokens such as:
             "HTBF" -- home team batted first.
             Note: if "HTBF" is specified it would be possible to see
             something like "01002000x" in the visitor's line score.
          Changes in umpire positions during a game will also appear in 
          this field.  These will be in the form:
             umpchange,inning,umpPosition,umpid with the latter three
             repeated for each umpire.
          These changes occur with umpire injuries, late arrival of 
          umpires or changes from completion of suspended games. Details
          of suspended games are in field 14.
  161     Acquisition information:
             "Y" -- we have the complete game
             "N" -- we don't have any portion of the game
             "D" -- the game was derived from box score and game story
             "P" -- we have some portion of the game.  We may be missing
                    innings at the beginning, middle and end of the game.
 
Missing fields will be NULL.
"""
    