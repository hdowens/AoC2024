# Notes from today

## Part 1:
The issue of not reading the question! I was not as attentive in reading today as I should have been. I looked at all the example cheats for part 1 and thought that they all followed a pattern, namely:
```
#    #         .
#    #         .
#    #       ##S#.
#    #         #
#    #         #
#    #The shape of  S#., where S is any position currently at in the path, with wall
#    #then a path component, is my first guess of a shortcut. I dont observe any other
#    #formations in the test case so will use that and see what happens

```

So I wrote code to test for this in orthogonal directions. It starts with putting the grid into a dict to use the `.get` method to circumvent all bounds checking, and then walking the path. Since the path is predefined, we can walk the path and have it in order and we can work out all shortcuts from that (didn't realise we didn't need the grid again until part2...). So, from each position in the path, check the 4 directions, if we have a `S#.` pattern in that direction, we have found a shortcut. Find the index of our shortcut `.` in the pattern, and the index of the `S` in the pattern and work out the difference. Since this difference did not take into account the 2 seconds required to do the shortcut, minus 2 from the index difference and we have our time saved. 

## Part 2:
Had to read this a few times, the problem description was confusing. I made a few assumptions, shortcuts always had to be minimal from any position, we couldn't have longer shortcuts that still saved a lot of time. Also, shortcuts could just be moving further along the path, and clipping through walls. It was then it dawned on me that for part 1 it is just 2 second shortcuts as opposed to 20, and then I re-read the problem and saw I was told that anyway lol.

So, with our new framing of the problem it becomes quite easy given that we have the path taken already. At each position, find the difference between it and all other positions in the path taken. If the manhattan/taxicab difference between the two is less than or equal to 20, then we have our shortcut. Work out the difference between their indices, and instead of minus-ing two like we did in part1, we minus the length as that is how long it would take to do the shortcut. 

It isn't hugely fast but works in under 2s. It was at this point I thought, wait can I not just do part 1 like this but have the cheat seconds changed from 20 to 2. So, I wrote a function that included the `cheat_seconds` and `interested_seconds` in the function signature to represent the seconds allowed to cheat for and the seconds we are interested in finding respectively. and... it worked. Now I have a general solution to this problem given any grid with a path and any amount of cheat seconds and interested seconds!

However, it was a bit slower than the part 1 I had written already but marginally. Maybe I'll work on optimisations, such as pre-computing distances or caching results, not entirely sure. I know for sure the amount of calculations I do are superfluous and there are definitely ways of optimising further, but got too much on atm.