# big_inning
A simple analysis of baseball statistics using Python
This exercise came about via an old baseball bet my late dad used:
"I bet that the wining team will score more runs in one inning than
the losing team will score in the whole game."
It was not intended to be a sure thing but as a bet that was a lot
better than it seamed and to add interest to almost any game.

My son pointed me to some readable data: 
  https://www.retrosheet.org/gamelogs/glfields.txt

My thanks go to the retrosheet organization for there hard work.

My intent was, rather than the simplest or shortest code, but
to produce code that might be able to be reused to investigate
or answer interesting question about baseball statistics.

The data resides in a number of CSV files which I downloaded into a sister
directory "data".

The base source files are in "src" directory, except for a few helper files:
  src/big_inning.py - scanns the game log files in "data" and tests game
  src/game_stats.py - analyzes a game stats, facilitates access, e.g. winner's innings
  select_trace.py which facilitates tracing and loging.
  select_error.py which provides domain based error processing

A couple of data files are present GL1871.TXT, GL2018.TXT.  The complete list were
downloaded to the "data" sister directory from www.retrosheet.org/gamelogs

At the risk of spoiling the surprise, the run listing end was:
```
 Big Inning: NYN got 1 in inning 13 on 20180929 MIA @ NYN visitor: 0000000000000 home: 0000000000001
 Big Inning: PHI got 3 in inning 7 on 20180929 ATL @ PHI visitor: 000000000 home: 00000030x
 Big Inning: MIN got 6 in inning 2 on 20180929 CHA @ MIN visitor: 100000002 home: 26000000x
 Big Inning: SEA got 3 in inning 7 on 20180929 TEX @ SEA visitor: 100000000 home: 00001030x
 Big Inning: COL got 3 in inning 5 on 20180930 WAS @ COL visitor: 000000000 home: 20203023x
 Big Inning: MIL got 6 in inning 7 on 20180930 DET @ MIL visitor: 000000000 home: 20010161x
 Big Inning: NYN got 1 in inning 4 on 20180930 MIA @ NYN visitor: 000000000 home: 00010000x
 Big Inning: PHI got 2 in inning 1 on 20180930 ATL @ PHI visitor: 001000000 home: 20001000x
 Big Inning: LAN got 7 in inning 3 on 20180930 LAN @ SFN visitor: 207320001 home: 000000000
 Big Inning: BAL got 4 in inning 4 on 20180930 HOU @ BAL visitor: 000000000 home: 00040000x
 Big Inning: BOS got 4 in inning 1 on 20180930 NYA @ BOS visitor: 000200000 home: 43030000x
 Big Inning: SEA got 2 in inning 2 on 20180930 TEX @ SEA visitor: 000001000 home: 02001000x
 Big Inning: MIL got 2 in inning 8 on 20181001 MIL @ CHN visitor: 001000020 home: 000010000
 Games processed: 197231  skipped: 20936
 First skipped: 18720525 MID @ WS4 visitor:  home: 
 Last skipped: 19790712 DET @ CHA visitor:  home: 
 First processed: 18710504 CL1 @ FW1 visitor: 000000000 home: 010010000
 Last processed: 20181001 COL @ LAN visitor: 000000002 home: 00022100x
 Big inning games: 92196 (46.75%)
 BigorTie inning games: 133743 (67.81%)
 Saving properties file C:\Users\raysm\workspace\python\baseball\big_inning.properties
 Closing log file C:\Users\raysm\workspace\python\baseball\log\big_inning_20190118_191651.sllog

```
The number of 47% was a surprise to me.  I've not investigated the high number of skipped games (20931) - those
which have no inning data.  This may be a bug or missing data, but the 197236 processed games provide
a sizeable number.

Some more selection has been added to select start_year an team_pat:
```
Big Inning: BAL got 4 in inning 9 on 20180926 BAL @ BOS visitor: 200010304 home: 100110000
 Big Inning: BOS got 4 in inning 1 on 20180930 NYA @ BOS visitor: 000200000 home: 43030000x
 Start with year: 2018
 Select games with team pattern: BOS
 Games processed: 2431  skipped: 0
 First processed: 20180329 BOS @ TBA visitor: 030000100 home: 00000006x
 Last processed: 20180930 NYA @ BOS visitor: 000200000 home: 43030000x
 Games considered: 162
 BOS Statistics
 BOS Total games: 162
 BOS Total winning games: 108 (66.67%)
 BOS home games: 81
 BOS Home    winning games: 57 (70.37%)
 BOS away games: 81
 BOS Away    winning games: 51 (62.96%)
 BOS Big inning games: 57 (35.19%)
 BOS Home    Win Big inning games: 32 (56.14%)
 BOS away    Win Big inning games: 25 (49.02%)
 
Overall Statisitcs
 Visitor Win Big inning games: 32 (42.67%)
 Home    winning games: 87 (53.70%)
 Visitor winning games: 75 (46.30%)
 Big inning games: 81 (50.00%)
 BigorTie inning games: 112 (69.14%)
 Home    Win Big inning games: 49 (56.32%)
 Visitor Win Big inning games: 32 (42.67%)
```


Setup:
  1. Create base / project directory, e.g. big_inning
  2. Place all source (.py) files in big_inning/src
  3. Place data files (sample GL1871.TXT, GL2018.TXT) in big_inning/data
  
 Run:
   1. cd big_inning
   2. python src/big_inning.py
   
Ray Smith


