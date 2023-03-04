## easy_dc

### algorithmic process:


What is the input? 
- List of edges?
- Adjacency list?
- List of vertices?

What does it need?
- A: An adjacency mapping using nodes (vs. vertices) from edges
- VI: A mapping of each vertex to its index in the list of vertices.
- EA: A mapping of edge and adjacent edges (edges parallel to key edge).
- W: A mapping of node to its accretion level (manhattan distance to origin (0, 0, 0)), this is only needed for the z-level -1. ie vertices whose z-value == -1.
- ZA: The adjacency list reduced where vertices with the z-value -1 are partitioned into its own adjacency list and for the rest of the floor the number of vertices in that level are saved: So {-1: {int: Set[int]}, -3: 24, -5: 12: -7: 4}   

form / scheme / design


### cut():
    
write a function that takes in a subset and a list and cuts the list using the subset.
subset is a subset of the list.
It does this by:
Getting the indices of all the subset nodes in the list.  
sort indices from min-max
split the tour accordingly.
make sure that subset node is in the left position to prepare for joining. 


the roaring twenties had the disco ball. 
I want to make a text in latex that is a4 and can be framed as a kind of explanation.

The discocube is techno's answer to the discoball.

an artist chooses an object as his muse,
starts to find ways to describe the object,
define a particular set of constraints which should lead specific aesthetic result. 
one of those constraints is to remove edges so that the reflections have more space to bounce around within the object. 
finds out describing the object is actually a problem people have been working on for hundreds of years.
But not on this particular instance.
The artistic vision remains the same, but the materials and techniques by which to render the object according to that vision. 
Drawing the form means programming the algorithm that solves the problem. 
But most of the algorithms that solve the problem are intractable with larger instances.
So i had to go about solving it myself using 

Steps to a discocube:

Draw the form: define the problem. write the algorithm that solves the problem.
reason for a loop is to give ample space 

discocube = discoball + graph theory + techno + 
 
Making a discocube is like connecting the dots to form a star, except you don't have to form a star, 
just connect the dots
As the number of dots to connect grows s

After 200 years: techno's upgrade to the discoball.
How does one digitize an object? by means 

I picked the form defined the problem without knowing that there was already a mathematical description of the problem and ways to solve it.. 
unfortunately not for the discocube. So the additional tasks was to acquire the knowledge and ability to write the algorithm that solves the problem, ie draws my form.


hamiltonian cycle. is a graph that visits each vertex exacltly once.


I chose the form, went about constructing the algorithm that solves the problem. 
A discocube graph is a graph constructed by the accretion of identical cubes around a central cube centered at origin

The discocube was conceived as techno's upgrade to the discoball.
Every discocube is unique as each winding form is computed by an algorithm.
Endless contour drawing of a geometric form, a mathematician would solve the problem of finding a hamiltonian cycle in a graph.

The artistic formulation of the problem is as follows, given a geometric form, describe the object using a line by drawing the contours of the object
The mathematical formulation of the problem is:

