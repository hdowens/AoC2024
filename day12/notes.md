# Notes from today

Today was definitely the hardest thus far. After enough thought it's not too hard to conceptualise what to do but actually implementing it is another thing entirely.

## Part 1

1. Do a BFS on each square. If that square is not visited already (global set) set a new region. The BFS would only add positions to the deque if the char at the position it is looking forward to is of the same char as the char at the new region. This BFS returned is the set of point involved in each region. So, iterating over the grid ($$O(N^m)$$, sure you could flatten the grid to make it $$O(N)$$ with a stride...) for each point try and compute a region. 
 >Probs is a way to optimise this, for example turn the grid into a set and when you return a region remove all the points involved with each step but the grids are not too big.

 Now that we have all the regions, for each region we need to compute the area and perimeter. Area is just the length of the region as each square is one unit. The perimeter is a little more tricky, the approach is that for each member in the set, look at its four neighbours (no diagonals) and for each one not in the region, increase the perimeter count. Multiply that by the area, sum them and we have the answer.

### Other approaches
Have seen people using flood fill algos which I think is functionally similar to what I did. The most interesting approach for me is to split the grid by character, so for all 'A's in the grid have all the positions. Then, you can figure out all the regions just from looking at all neighbours. Then, rinse and repeat with area and perimeter


## Part 2
This part was a tricky and I went down a rabbit hole of drawing out each grid to try and count the sides then, after looking for hints on reddit, counting the corners was the trick. I thought this wouldn't be difficult but it turned out to be harder than I anticipated.
 
For each point in the region, we need to see how many neighbours it has as that will tell us how many corners it should have. No or 1 neighbours is simple enough, but 2 3 and 4 could have neighbours in various configurations and you need to consider the diagonals here to see if there is what I called a 'middle' corner.

For example, consider the two regions below
```
+-+-+
|C C| 
|C C| 
+-+-+


+-+
|C|
+ +-+
|C C|
+-+-+
```
The first grid has no 'middle' corner as the _diagonal_ is also in the region, so we need to see in the bottom case if the top right is _also_ in the region. If it is, then there is no corner. This has various edge cases for 2 and 3 based on the orientation of the garden.
```
  +-+         +-+
  |C|         |C|
+-+ +-+   &   + +-+
|C C C|       |C C|
+-+-+-+       + +-+
              |C|
              +-+

```
In the above two example we will need to check the two diagonals based on if the three in the row are horizontally or vertically aligned.
With 4 cases, you need to check if a plus sign shape has all 4 diagonals.

This turned out to be pretty messy code but it is what it is... Some people solved with some observations and maths tricks which I wish I had the foresight for but once I was nearly at the solution I could see the end so I just barreled on with this solution.


