# Notes
--- Day 11: Plutonian Pebbles ---

## Part 1:
Not much to say, just brute forced it with storing everything in a a list. 25 iterations didn't seem too bad. It computed < 1s so I wasn't fussed.

## Part 2:
75 Iterations. Brute forcing will sadly not work here anymore, but it offers a chance to implement some optimisations. My first thought was the memoise the stone "transmutation" as I called it, so the process of taking a stone and turning it to a new stone / new stones. This offered some speed-up with brute force but by iteration ~45 it wasn't budging. Time to re-think the approach.

The key insight here is that order does not matter. Therefore, there is no point storing them in an implicitly ordered data structure. We can just keep track of the count of each stone in each iteration. This speeds things up and solves the problem in 0.062s. I've used the Counter from collections, not particularly sure why, I just used it for project euler back in t'day and now carrying it forth. 


### defaultdict vs Counter
from: https://stackoverflow.com/questions/19883015/python-collections-counter-vs-defaultdictint

-    Counter supports most of the operations you can do on a multiset. So, if you want to use those operation then go for Counter.

 -   Counter won't add new keys to the dict when you query for missing keys. So, if your queries include keys that may not be present in the dict then better use Counter.

This supports what I've seen in previous days' solutions but not made a note of it even though I should have. I saw sometehing cool for the grid problems, parse the grid and store them in dict/Counter and then to stop worrying about bounds checks make a call to the Counter, which will return None if they dont exist so it solves all those issues. I will do this for the next grid problem. (from the future, it happens tomorrow!)


### Other people's approaches
Memoisation is the theme of breaking the back of non-brute forceable AOC problems, so its no surprise a lot of people focused on that. The focus there was to memoise the entire function and all itself recursively each time the list was update, kind of like the day previous. Interesting approach, one of which I would turn to last due to recursion introducing so many headaches for debugging. I'm 99% sure that it then becomes a dynamic programming issue, like the coin problem in project euler.

- - - 

### Is there a number cycle?
My thinking here is wondering what numbers will end up as


- - -
### A bitta fun
```
func:'count_stones' args:[(['1750884', '193', '866395', '7', '1158', '31', '35216', '0'], 25), {}] took: 0.0020 sec
Part 1 with 25 iterations: 231278

func:'count_stones' args:[(['1750884', '193', '866395', '7', '1158', '31', '35216', '0'], 75), {}] took: 0.0626 sec      
Part 2 with 75 iterations: 274229228071551

func:'count_stones' args:[(['1750884', '193', '866395', '7', '1158', '31', '35216', '0'], 5000), {}] took: 11.4473 sec   
Part 3 with 5000 iterations (for science): 320575548096635838334577812204234190306405803662306041157618479427301318682906346125036928197146353644062044328556918452658074276341055364946235794513970168062370624878173150137211076071262635913687305286665059894219621582945512596654428968322798321629440440347952972593533434429115569547781929973284735563536381499229495489899910169226584678330810257246818307913026615742123118167152326666661817531394194802265547718727431297884732387983541305737401168877974195383449291354308206804694075612658176868795757685194695855650836760797087503324054730673485734959641077160652696816970718434849028783560928763361735105090053111216608079831424663924920657007266584216247824230634439184070316857516725481072030481186719349954251000603460835049359602296960058385100968876286215529216458103982559380693213516643593605379119589071150363524474584692031659864690177747212557118050233159439953419901291155347665180988062397
```