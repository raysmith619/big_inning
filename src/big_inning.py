# big_inning.py

import sys
import argparse
import re
import os
import csv 

from select_trace import SlTrace
from game_stats import GameStats

"""
Data origin followed by file format is in game_stats.py
"""



def str2bool(v):
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')


data_dir = "../data"
game_file_pat = r'^GL(\d+)\.TXT$'
nfiles = None       # Limit number of files to this number
nrows = None        # Limit column display to this number
nbiginn = 4         # Check for big inning(s)
start_year = None   # Start looking at this year, if present
strict = False      # True only look at completely acquired games stats
team_pat = None     # team name regex pattern, if present, restricts games to contain
trace = "list_big_innings"
parser = argparse.ArgumentParser()

parser.add_argument('--data_dir=', dest='data_dir', default=data_dir)
parser.add_argument('--game_file_pat=', dest='game_file_pat', default=game_file_pat)
parser.add_argument('--nfiles=', type=int, dest='nfiles', default=nfiles)
parser.add_argument('--nrows=', type=int, dest='nrows', default=nrows)
parser.add_argument('--nbiginn=', type=int, dest='nbiginn', default=nbiginn)
parser.add_argument('--start_year=', type=int, dest='start_year', default=start_year)
parser.add_argument('--strict', type=str2bool, dest='strict', default=strict)
parser.add_argument('--team_pat=', dest='team_pat', default=team_pat)
parser.add_argument('--trace=', dest='trace', default=trace)
args = parser.parse_args()             # or die "Illegal options"

data_dir = args.data_dir
game_file_pat = args.game_file_pat
nfiles = args.nfiles 
ncols = args.nrows
nbiginn = args.nbiginn
start_year = args.start_year
strict = args.strict
team_pat = args.team_pat
trace = args.trace

SlTrace.lg("%s %s\n" % (os.path.basename(sys.argv[0]), " ".join(sys.argv[1:])))
SlTrace.lg("args: %s\n" % args)


SlTrace.setupLogging()
SlTrace.setProps()
SlTrace.lg("big_inning")
###SlTrace.setFlags("list_file_name,list_file_rows,list_raw_interest")
SlTrace.setFlags(trace)

dir_set = ()
if os.path.isabs(data_dir):
    data_dir_path = data_dir
else:
    data_dir_path = os.path.abspath(data_dir)
print("data_dir: %s" % data_dir_path)
data_files = os.listdir(data_dir)
n_big_inning_games = 0
n_bigtie_inning_games = 0      # Tie or better
first_skipped_game = None
last_skipped_game = None
first_processed_game = None
last_processed_game = None
n_games_considered = 0
n_home_team_wins = 0
n_home_team_big_inning_games = 0
n_visitor_team_wins = 0
n_visitor_team_big_inning_games = 0

n_team_pat_home_team_wins = 0       # selected team
n_team_pat_home_team_big_inning_games = 0
n_team_pat_visitor_team_wins = 0
n_team_pat_visitor_team_big_inning_games = 0
n_team_pat_home_games = 0
n_team_pat_visitor_games = 0
n_team_pat_big_inning_games = 0

file_no = 0
for file_name in data_files:
    ###print("file_name: %s" % file_name)
    fmat = re.match(game_file_pat, file_name)
    if not fmat:
        continue
    if start_year is not None:
        file_year = int(fmat.group(1))
        if start_year > file_year:
            continue
    file_no += 1
    if nfiles is not None and file_no > nfiles:
        break
    file_path = os.path.join(data_dir_path, file_name)
    SlTrace.lg("file: %s" % file_path, "list_file_name")
    csv_r = csv.reader(open(file_path, newline=''))
    row_no = 0
    for row in csv_r:
        row_no += 1
        if nrows is not None and row_no > nrows:
            break
        SlTrace.lg(",".join(row), "list_file_rows")
        game_stats = GameStats(row)
        if not game_stats.is_ok():
            SlTrace.lg("Skipping game " + game_stats.raw_interest(), "list_games_skipped")
            last_skipped_game = game_stats
            if first_skipped_game is None:
                first_skipped_game = game_stats
            continue
        
        if team_pat is not None:
            if (not re.match(team_pat, game_stats.h_team())
                and not re.match(team_pat, game_stats.v_team())):
                continue        # Not our team(s)
            
            if re.match(team_pat, game_stats.h_team()):
                n_team_pat_home_games += 1
            else:
                n_team_pat_visitor_games += 1    # One or the other
                
        n_games_considered += 1

        last_processed_game = game_stats
        if first_processed_game is None:
            first_processed_game = game_stats

        SlTrace.lg(game_stats.raw_interest(), "list_raw_interest")
        win_t, loose_t = game_stats.team_infos()
        win_max_inn = max(win_t.inning_scores)
        loose_score = loose_t.game_score
        has_big_inning = False      # Set True iff got it
        if win_max_inn > loose_score:
            n_big_inning_games += 1
            win_team = win_t.team
            has_big_inning = True
            SlTrace.lg("Big Inning: %s got %d in inning %d on %s"
                        % (win_team, win_max_inn,
                            win_t.fiwirun(win_max_inn), game_stats.summary()),
                         "list_big_innings")
            if team_pat is not None:
                if re.match(team_pat, win_team):
                    n_team_pat_big_inning_games += 1
        if win_max_inn >= loose_score:
            n_bigtie_inning_games += 1
            SlTrace.lg("Big Tie Inning: %s got %d in inning %d on %s"
                        % (win_team, win_max_inn,
                            win_t.fiwirun(win_max_inn), game_stats.summary()),
                         "list_bigtie_innings")
        if win_t.team_type == "h":
            n_home_team_wins += 1
            if has_big_inning:
                n_home_team_big_inning_games += 1
            if team_pat is not None:
                if re.match(team_pat, win_t.team):
                    n_team_pat_home_team_wins += 1
                    if has_big_inning:
                        n_team_pat_home_team_big_inning_games += 1
                
        if win_t.team_type == "v":
            n_visitor_team_wins += 1
            if has_big_inning:
                n_visitor_team_big_inning_games += 1
            if team_pat is not None:
                if re.match(team_pat, win_t.team):
                    n_team_pat_visitor_team_wins += 1
                    if has_big_inning:
                        n_team_pat_visitor_team_big_inning_games += 1


if start_year is not None:
    SlTrace.lg("Start with year: %d" % start_year)
if team_pat is not None:
    SlTrace.lg("Select games with team pattern: %s" % team_pat)

if nfiles is not None:
    SlTrace.lg("Scan only first %d files" % nfiles)

if nrows is not None:
    SlTrace.lg("Scan only first %d games in each file" % nrows)
                        
SlTrace.lg("Games processed: %d  skipped: %d" % (GameStats.n_processed, GameStats.n_skipped))
if first_skipped_game is not None:
    SlTrace.lg("First skipped: %s" % first_skipped_game.summary())
if first_skipped_game is not None:
    SlTrace.lg("Last skipped: %s" % last_skipped_game.summary())
if first_processed_game is not None:
    SlTrace.lg("First processed: %s" % first_processed_game.summary())
if first_processed_game is not None:
    SlTrace.lg("Last processed: %s" % last_processed_game.summary())

SlTrace.lg("Games considered: %d" % n_games_considered)    
if team_pat is not None:
    SlTrace.lg("%s Statistics" % team_pat)
    tp_tot_games = n_team_pat_home_games+n_team_pat_visitor_games
    tp_tot_wins = n_team_pat_home_team_wins + n_team_pat_visitor_team_wins
    SlTrace.lg("%s Total games: %d" % (team_pat, tp_tot_games))        
    tp_tot_win_percent =  tp_tot_wins/ tp_tot_games * 100.
    SlTrace.lg("%s Total winning games: %d (%.2f%%)" % (team_pat, tp_tot_wins, tp_tot_win_percent))
    
    SlTrace.lg("%s home games: %d" % (team_pat, n_team_pat_home_games))    
    tp_hwin_percent = n_team_pat_home_team_wins / n_team_pat_home_games * 100. 
    SlTrace.lg("%s Home    winning games: %d (%.2f%%)" % (team_pat, n_team_pat_home_team_wins, tp_hwin_percent))

    SlTrace.lg("%s away games: %d" % (team_pat, n_team_pat_visitor_games))    
    tp_vwin_percent = n_team_pat_visitor_team_wins / n_team_pat_visitor_games * 100. 
    SlTrace.lg("%s Away    winning games: %d (%.2f%%)" % (team_pat, n_team_pat_visitor_team_wins, tp_vwin_percent))
    tp_big_percent = n_team_pat_big_inning_games / n_games_considered * 100. 
    SlTrace.lg("%s Big inning games: %d (%.2f%%)" % (team_pat, n_team_pat_big_inning_games, tp_big_percent))
    tp_big_percent = n_team_pat_home_team_big_inning_games / n_team_pat_home_team_wins * 100. 
    SlTrace.lg("%s Home    Win Big inning games: %d (%.2f%%)" % (team_pat, n_team_pat_home_team_big_inning_games, tp_big_percent))
    tp_v_big_percent = n_team_pat_visitor_team_big_inning_games / n_team_pat_visitor_team_wins * 100. 
    SlTrace.lg("%s away    Win Big inning games: %d (%.2f%%)" % (team_pat, n_team_pat_visitor_team_big_inning_games, tp_v_big_percent))
    SlTrace.lg("\nOverall Statisitcs")

vw_big_percent = n_visitor_team_big_inning_games / n_visitor_team_wins * 100. 
SlTrace.lg("Visitor Win Big inning games: %d (%.2f%%)" % (n_visitor_team_big_inning_games, vw_big_percent))
    
    
    
hwin_percent = n_home_team_wins / n_games_considered * 100. 
SlTrace.lg("Home    winning games: %d (%.2f%%)" % (n_home_team_wins, hwin_percent))
    
vwin_percent = n_visitor_team_wins / n_games_considered * 100. 
SlTrace.lg("Visitor winning games: %d (%.2f%%)" % (n_visitor_team_wins, vwin_percent))
    
    
big_percent = n_big_inning_games / n_games_considered * 100. 
SlTrace.lg("Big inning games: %d (%.2f%%)" % (n_big_inning_games, big_percent))
bigtie_percent = n_bigtie_inning_games / n_games_considered * 100. 
SlTrace.lg("BigorTie inning games: %d (%.2f%%)" % (n_bigtie_inning_games, bigtie_percent))

hw_big_percent = n_home_team_big_inning_games / n_home_team_wins * 100. 
SlTrace.lg("Home    Win Big inning games: %d (%.2f%%)" % (n_home_team_big_inning_games, hw_big_percent))

vw_big_percent = n_visitor_team_big_inning_games / n_visitor_team_wins * 100. 
SlTrace.lg("Visitor Win Big inning games: %d (%.2f%%)" % (n_visitor_team_big_inning_games, vw_big_percent))


        
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
