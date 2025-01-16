## Notes from day 18

## Part 1
Another grid problem, finally getting the hang of them. This is one where we dont need to weight any movements like in day 16, but instead we have a lot of possible moves throughout the grid. Therefore, in order to solve this the program will need to be modified to use a better version of BFS. 

Instead of using a double ended queue, we can borrow the priority queue taken from day 16. We will need a 'score' or, as its known in maths jargon, a 'heurstic' when adding each position to the priority queue which it will use to pick from. (Implementation note, lists in python are lexicographically compared so the score will need to be first, and this is how the priority queue will pick.) For this, the program implements a common heuristic known as the manhattan/taxicab difference. It is the absolute difference between the difference the y values of two co-ordinates plus the absolute difference between the x values. We then add and iterate over the queue without much other logic, and exit when the position we are looking at is the end.

## Part 2
I had anticipated having to simulate more scenarios of RAM but this turned out nicer than expected. Loop through the simulation sizes, and find where no path could return. Mine is slightly slow, producing the answer in under one minute just. There are many ways to speed this up. 


## Cool implementation
> https://www.reddit.com/r/adventofcode/comments/1hhiawu/2024_day_18_part_2_visualization_of_my_algorithm/

This is a seriously cool implementation. The OP doesn't explain how it works but my visual guess after 30 seconds of looking at it, is that it works out what co-ord causes a contiguous area of error memory to be on two horizontal (or vertical) limits. This is similar to the definition of a SPANGRAM in the NYT daily puzzle 'Strands'.