## Parameters of a rectangle 

By the name the right angle is the basic element of a rectangle. Starting with central coordinates of postholes represented by a point you might expect the use of trigonometric functions to check for third points forming a right angle. Due to calculation expense this is not the case for postAAR.

Insted of calculating angles we compare the opponend sides and the diagonals. Imagine the three basic geometric forms: rectangle, trapeze and diamond.

1. rectangle: the opposing sides have equal length and the diagonals eequal lenght as well.
2. trapezoid: two opposing sides have a different length while the other sides and the diagonals have equal length.
3. diamond: the opposing sides have equal length while the diagonals differ.

There are more relatet geometric forms, e.g. rhomboid, but for our search of rectangles they represent other variants of the **two basic rools we use to find rectangles**.

Within 4 points forming a square:
1. the opposite sides have a similar length and
2. the diagonals have a similar length.

We use percent of lenght within corresponding distances to avoid scaling effects.

 ## Setting the parameters
 
 ### Sides
 The minimum and the maximum length of the sides is given in map units and defines the possible dimensions of the rectangles or quadrates incrising adjacend sides indepenently. With the difference between opposide sides the amount of irregularity increases towards trapezoids, kites, rhomboids, irregular squares.
 
 ### Diagonals
 The minimal and maximal length of the diagonals can be set in percent and will be multiplied with the corresponding value for the sides:
 
 ```
 max_diagonal_dist = maximal_length_of_side * maximal_length_of_diagonal
 min_diagonal_dist = minimal_length_of_side * minimal_length_of_diagonal
 ```
 
 Assuming a quadrate the diagonal (d) in percent of side length can be calculated by:
 
 ```
 d = sqrt(100² + 100²) ≈ 142
 ```
 
 