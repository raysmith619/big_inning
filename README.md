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
 Big Inning for PHI of 2 runs in 20180930 ATL @ PHI visitor: 001000000 home: 20001000x
 Big Inning for LAN of 7 runs in 20180930 LAN @ SFN visitor: 207320001 home: 000000000
 Big Inning for BAL of 4 runs in 20180930 HOU @ BAL visitor: 000000000 home: 00040000x
 Big Inning for BOS of 4 runs in 20180930 NYA @ BOS visitor: 000200000 home: 43030000x
 Big Inning for SEA of 2 runs in 20180930 TEX @ SEA visitor: 000001000 home: 02001000x
 Big Inning for MIL of 2 runs in 20181001 MIL @ CHN visitor: 001000020 home: 000010000
 Games processed: 197236  skipped: 20931
 First skipped: 18720525 MID @ WS4 visitor:  home: 
 Last skipped: 19790712 DET @ CHA visitor:  home: 
 First processed: 18710504 CL1 @ FW1 visitor: 000000000 home: 010010000
 Last processed: 20181001 COL @ LAN visitor: 000000002 home: 00022100x
 Big inning games: 92199 (46.75%)
 Saving properties file C:\Users\raysm\workspace\python\baseball\big_inning.properties
 Closing log file C:\Users\raysm\workspace\python\baseball\log\big_inning_20190118_101400.sllog

The number of 47% was a surprise to me.  I've not investigated the high number of skipped games (20931) those
which have no inning data.  This may be a bug or missing data, but the 197236 processed files provide
a sizeable number.


Setup:
  1. Create base / project directory, e.g. big_inning
  2. Place all source (.py) files in big_inning/src
  3. Place data files (sample GL1871.TXT, GL2018.TXT) in big_inning/data
  
 Run:
   1. cd big_inning
   2. python src/big_inning.py
   
Ray Smith


