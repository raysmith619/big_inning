# big_inning.py

import re
import os
import csv 

from select_trace import SlTrace
from game_stats import GameStats

"""
Data origin followed by file format is in game_stats.py
"""

data_dir = "../data"
game_file_pat = r'^GL\d+\.TXT$'

SlTrace.setupLogging()
SlTrace.setProps()
SlTrace.lg("big_inning")
###SlTrace.setFlags("list_file_name,list_file_rows,list_raw_interest")
SlTrace.setFlags("list_big_innings")

dir_set = ()
if os.path.isabs(data_dir):
    data_dir_path = data_dir
else:
    data_dir_path = os.path.abspath(data_dir)
print("data_dir: %s" % data_dir_path)
data_files = os.listdir(data_dir)
n_big_inning_games = 0

n_files = 2
n_files = None
n_rows = 10
n_rows = None

file_no = 0
for file_name in data_files:
    ###print("file_name: %s" % file_name)
    if not re.match(game_file_pat, file_name):
        continue
    file_no += 1
    if n_files is not None and file_no > n_files:
        break
    file_path = os.path.join(data_dir_path, file_name)
    SlTrace.lg("file: %s" % file_path, "list_file_name")
    csv_r = csv.reader(open(file_path, newline=''))
    row_no = 0
    for row in csv_r:
        row_no += 1
        if n_rows is not None and row_no > n_rows:
            break
        SlTrace.lg(",".join(row), "list_file_rows")
        game_stats = GameStats(row)
        if not game_stats.is_ok():
            SlTrace.lg("Skipping game " + game_stats.raw_interest(), "list_games_skipped")
            continue
        
        SlTrace.lg(game_stats.raw_interest(), "list_raw_interest")
        win_t, loose_t = game_stats.team_infos()
        win_max_inn = max(win_t.inning_scores)
        loose_score = loose_t.game_score
        if win_max_inn > loose_score:
            n_big_inning_games += 1
            win_team = win_t.team
            SlTrace.lg("Big Inning for %s of %d runs in %s"
                        % (win_team, win_max_inn, game_stats.summary()), "list_big_innings")
SlTrace.lg("Games processed: %d  skipped: %d" % (GameStats.n_processed, GameStats.n_skipped))
big_percent = n_big_inning_games / GameStats.n_processed * 100. 
SlTrace.lg("Big inning games: %d (%.2f%%)" % (n_big_inning_games, big_percent))
        
"""
Recipients of Retrosheet data are free to make any desired use of
the information, including (but not limited to) selling it,
giving it away, or producing a commercial product based upon the
data.  Retrosheet has one requirement for any such transfer of
data or product development, which is that the following
statement must appear prominently:

     The information used here was obtained free of
     charge from and is copyrighted by Retrosheet.  Interested
     parties may contact Retrosheet at "www.retrosheet.org".

Retrosheet makes no guarantees of accuracy for the information 
that is supplied. Much effort is expended to make our website 
as correct as possible, but Retrosheet shall not be held 
responsible for any consequences arising from the use the 
material presented here. All information is subject to corrections 
as additional data are received. We are grateful to anyone who
discovers discrepancies and we appreciate learning of the details.
"""
