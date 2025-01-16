## Notes from day 16

### Part 1
So this is now a weighted path search so we cannot just use BFS as BFS assumes the cost of traversing in any way to be equivalent. So, we need to use a new algorithm.

The algorithm is a called Dijsktra's algorithm, classic graph theory uni CS algo. Here, each edge in the graph has a cost associated with traversing that. It uses a priority queue, implemented in python from the `heapq` module which implements it as a heap.  A priority queue, when you pop it, will always pop the value with the smallest value attached to it. So, you pop each position to mov eto with the associated cost and traverse the network that way.

An interesting difference between it and BFS is that when BFS sees a node, it adds it to the visited set and then, algorithmically, that node is dealt with. This is not the case for Dijsktra. The first path to that node may not have the optimal cost associated to it, so whilst we can assign a cost to it with the direction it arrived from, we may need to revisit it with a more optimal cost. It is only considered complete when we have seen it with all directions you can arrive it at from.

### Part 2
Here my idea was just to get the path of every optimal path and then find the set intersection between them all. To do this, the implemented dijkstra would need to be modified a bit because for the optimal cost implementation the program was not tracking the path throughout the traversal, treating the cost finding effectively as a dynamic programming problem. The current path was added as part of the priority queue key.