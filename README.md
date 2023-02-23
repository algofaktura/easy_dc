# easy dc solver
An algorithm for solving the Hamiltonian cycle problem deterministically and in linear time on all instances of discocube graphs which are:
3-dimensional grid graphs derived from: a polycube of an octahedron | a Hauy construction of an octahedron using cubes as identical building blocks | the accretion of cubes around a central cube forming an octahedron at the limit...

![Planar embedding of Cube and Discocubes](imgs/planar_emb.png?raw=true "Planar embedding of Cube and Discocubes")
*Planar embedding of a cube and a discocube. from the set of all graphs G, where the order of G is of the ***Uncentered octahedral numbers*** [A130809](https://oeis.org/A130809), only the first two instances shown above; n[0] and n[1] are planarly embeddable i.e., it can be represented on a two-dimensional surface without any of its edges crossing.*

![First 11 discocubes and their order (number of nodes)](imgs/rect5857.png?raw=true "Discocubes orders")
*The first eleven discocubes and their respective orders (number of nodes)*

Finding the solution to the problem reminded me of macramé, of tying knots, weaving and how repeating certain movements resulted in certain patterns. I followed the thought further and asked myself if there was a 'weave' I could use to expose underlying unit structure and repeat this throughout to get an initial solution which could later be mutated to produce a more polished solution. 

The focus of this work is to apply all that I know about this graph, not as a discrete mathematician, but as an artists with an eye towards visual aesthetics. Inspiration was the driving force behind the work (a bit of obsession I confess). 

From expressing the desire to sculpt a 3-dimensional contour drawing of an object to reformulating this desire mathematically as searching for a Hamiltonian cycle in specific yet unidentified graph, sketches are indistinguishable from mini algorithms.  An artist uses language and forms that language to communicate their vision to others, taking part in a process of translation from one medium to another, from vision to object, from words to movement, just as a programmer might transform ideas into an orchestra of processing with the perfect score.

This is a tiny result of that artistic investigative process and I hope it will be useful. I've grown so obsessed with the discocube object, really not unlike an obsessive artist's muse to the point of being a stalker. 

The goal wasn't to write a fast algorithm that finds always turning hamiltonian cycles in discocube graphs, and other stuff...  it was a constant moving of goalposts, of never being satisfied, of not knowing what, but of wanting more... until I could claim the discocube was my own (in my mind), as a painter would claim a portrait their own after having spent months realizing a vision.

Art studies forms, the curvature of the neck as it disappears into the back, the color in the foreground, so luminous, relegating all things beyond to irrelevance. So in this project, I studied the discocube as a body, where each turn was conceptualized not as a discrete math object but as movement of the body, resulting in more doodles and sketches than pages of equations.

I hope to tell the story of the discocube, introduce an undefined graph class *Cubic Accretion Graphs*, some of its properties, and the share insights I've gained by solving this problem having taken an approach similar to that of sculpting the human body...After thousands of studies, drawings, a little math: this is a tiny glimpse into how moving towards a specific aethetic goal yields results. When a graph becomes an artist's muse, how does the artist go about rendering their vision as a painter paints a portrait?

![Discocubes](imgs/dcviews.png?raw=true "Discocubes")
*Discocubes 8 - 1760*

What started as a hack-your-own version of a depth-first-search-with-shortcuts for the discocube graph (solving up to 960 vertices), metastasized into pages of overgrown mixin classes mysteriously coupled to each another like overgrown vines pushing me deeper and deeper into the underbelly of its mutant tentacles. Although it was able to solve instances of over a million vertices, it had the clarity of primordial soup. So, as a sadistic gardener I painstakingly pruned my own unescapable web (all those letters you haven't opened yet?) of thorny vines into presentable tiny bonsai trees. So what is a bonsai if not a tree in intimate scope?

To paraphrase Hauy: 

*When solving problems that involve analyzing how nature progresses, we are led by very rapid methods to results that are not immediately obvious. These results may appear paradoxical and surprising. However, if we take the time to carefully examine the steps we took to reach these results, we will begin to understand the underlying principles that led to these outcomes. By going back over the process step by step, we can better understand the logic behind the final results.*

The result of this creative process is a family of algorithms developed specifically to solve various graph problems on the disoocube graph, 3d grid graph and hexprism honeycomb diamond graphs. 
The algorithm presented in this repository is the least complex, also making it the fastest. It does the job, solving the hamiltonian cycle problem for over millions of vertices in reasonable time (seconds vs. years), while others take longer but also have other objectives, like forming an always turning cycle with even edge distribution across all axes. But that's giving too much away... 

Eventually this repository will include other linear time algorithms for solving the hamiltonian cycle problem in 3d grid graphs and also in solid grid graphs, addressing some open issues raised in the graph theory research literature.
Execution time of each order (in millions):

![Hexprism Honeycomb Diamond](imgs/hexhoneydiamond.png?raw=true "Hexprism Honeycomb Diamond")
*Hexprism Honeycomb Diamond*


## Running times
As the order of the graph increases the number of function calls for each nodes goes down to less than 1.5 function calls when profiled using a deterministic profiler. At around 2 million vertices the function call for each node goes down to almost one.

New running times cut down by the introduction of the colored yarns:

***before***
![Runtimes of each order](imgs/8-2million.png?raw=true "Runtimes of each order")

***after***
![Runtimes of each order](imgs/8-2million2.png?raw=true "Runtimes of each order")

***after after: 2x faster***
![Runtimes of each order](imgs/8-2million2x2.png?raw=true "Runtimes of each order 2x faster")

### solve profile 2,997,280 vertices:
![Profile of solve_np](imgs/profile_2997280.png?raw=true "Profile of solve_np")
***I've managed to speed it up even more: Twice the speed!***
![Profile of solve_np](imgs/profile_2997280faster.png?raw=true "Profile of solve_np")
### solve profile 5,061,680 vertices:
![Profile of solve_np](imgs/profile_solve_np5.png?raw=true "Profile of solve_np")
### solve profile 10,039,120 vertices:
![Profile of solve_np](imgs/profile_10.png?raw=true "Profile of solve_np")


### digital discocubes
As each solution is as unique as a fingerprint, or a diamond it allows one to have their own digital version of a discocube, which is also an instruction for building your own.

![Discocube 3640 view](imgs/icy_cube.png?raw=true "icy cube") 
![Discocube 3640 view](imgs/icy_cube5.png?raw=true "icy cube")
![Discocube 3640 view](imgs/icy_cube4.png?raw=true "icy cube")
![Discocube 3640 view](imgs/icy_cube3.png?raw=true "icy cube another view")
![Discocube 3640 view](imgs/icy_cube2.png?raw=true "icy cube another view")
![Always Turning Discocube 9120 view](imgs/always_turning_9120.png?raw=true "Always Turning Discocube 9120 view")
*Discocubes as glb, using different mirrored texture yields personalized results and unique reflections meaning each discocube has its own reflection/shadow fingerprint! With millions of combinations available (glass texture/image/color, mirror texture/image/color, edge texture/image/color), the possibilities are endless!*


### coming soon...
![Discocube 3640 view](imgs/comingsoom.png?raw=true "Drawing of the algorithmic process") 
*I'm currently in the process of illustrating the process of the algorithm. But that's its own process.*

### ps...
Please note: the hamiltonian cycle produced by this algorithm is the base form, without a high mutation rate. The polished versions available have no nonturns and all their edges are distributed evenly across the three axes.
The other algorithms I spoke of earlier accomplish this task.

## Installation
You can install the package by running: 
```
pip install easy_dc
```

## Usage
You can use the package by running the following command in the command line:
```
solve(order)
```

## Command line usage
To use the package via the command line, navigate to the root directory of the project in your terminal and run the following command:
```
python -m easy_dc solve [ORDER]
```
Where [ORDER] is the order of the graph you want to solve. This command will create the graph if it does not already exist, solve the problem, print the time it took to solve the problem, and plot the solution as a 3D line drawing.

You can also pass multiple orders to solve at once by separating them with a space:
```
python -m easy_dc solve 32 80 160 280
```
You can also use the '--help' flag to see a list of available orders:
```
python -m easy_dc solve --help
```
This will show a list of available orders, which can be used as input when running the solve command.

Note that the first 25 instances, from order 32 to 26208, are already included in the package. If you want to solve higher instances, you will need to create the corresponding graphs first using the make_graphs command (see below).

## Creating graphs
To create new graphs, you can use the 'make_graphs' command:
```
python -m easy_dc make_graphs [ORDER] 
```
Where [ORDER] is the order of the graphs you want to create. The graphs will be saved in the graphs folder within the project directory.
Upon installation, the package will create 25 problem instances from order 32 to 26208 in the graphs folder. You can solve higher instances but the graphs will have to be produced first.

You can also pass multiple orders to create at once by separating them with a space:
```
python -m easy_dc make_graphs 32 80 280 960
```
This command will create 3 graphs of order 32, 80, 280 and 960.

Where order is an integer from the following list of available orders:

```
[32, 80, 160, 280, 448, 672, 960, 1320, 1760, 2288, 2912, 3640, 4480, 5440, 6528, 7752, 9120, 10640, 12320, 14168, 16192, 18400, 20800, 23400, 26208, 29232, 32480, 35960, 39680, 43648, 47872, 52360, 57120, 62160, 67488, 73112, 79040, 85280, 91840, 98728, 105952, 113520, 121440, 129720, 138368, 147392, 156800, 166600, 176800, 187408, 198432, 209880, 221760, 234080, 246848, 260072, 273760, 287920, 302560, 317688, 333312, 349440, 366080, 383240, 400928, 419152, 437920, 457240, 477120, 497568, 518592, 540200, 562400, 585200, 608608, 632632, 657280, 682560, 708480, 735048, 762272, 790160, 818720, 847960, 877888, 908512, 939840, 971880, 1004640, 1038128, 1072352, 1107320, 1143040, 1179520, 1216768, 1254792, 1293600, 1333200, 1373600, 1414808, 1456832, 1499680, 1543360, 1587880, 1633248, 1679472, 1726560, 1774520, 1823360, 1873088, 1923712, 1975240, 2027680, 2081040, 2135328, 2190552, 2246720, 2303840, 2361920, 2420968, 2480992, 2542000, 2604000, 2667000, 2731008, 2796032, 2862080, 2929160, 2997280]
```

The program will then solve the problem instance, display the time it took and plot the solution as a 3D line drawing.

## Additional Options

You can also use the '--output' flag to specify a custom directory to save the output graphs. For example:
```
python -m easy_dc make_graphs 1373600 --output /path/to/custom/directory
```
___
![A Discocube with 960 vertices](imgs/dc960.JPG?raw=true "A Discocube with 960 vertices")

## Licensing:

This package is licensed under the MIT license.




Happy reading!