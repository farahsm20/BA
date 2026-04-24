When PostgreSQL executes a join it has choices, it can use a hash join, a nested loop join, or a merge join. When it scans a table it can 
do a full sequential scan or use an index. Physical operator selection is the step where you decide which of these to use for each join 
and each table scan in the query.

Two operating modes:
### Mode 1: with join order
A join ordering stage ran before this. The operator selection receives the final join order as input and assigns physical operators to 
each join and scan in that order.
### Mode 2: without join order
No join ordering stage is present. The operator selection assigns physical operators to any intermediate in the query, restricting
the search space of the native optimizer, which still decides the join order itself.
