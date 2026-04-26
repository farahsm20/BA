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

## Physical Operator Selection Summary
I implemented and ran the first PostBOUND optimization . This is the step where you tell PostgreSQL which operators to use for each table scan and join, bypassing its native optimizer.

### What we built
A basic operator selection that assigns:

SequentialScan to every table
HashJoin to every join

PostBOUND takes these decisions and injects them as pg_hint_plan hints into the SQL query.

Benchmark: [Join Order Benchmark](https://github.com/gregrahn/join-order-benchmark) (ig the original link changed ?)


### Result

```
/*+
 SeqScan(t)
 SeqScan(mi)
 SeqScan(ci)
 HashJoin(t mi)
 HashJoin(t ci)
 HashJoin(mi ci)
 HashJoin(t mi ci)
 */
SELECT * FROM title AS t 
JOIN movie_info AS mi ON t.id = mi.movie_id 
JOIN cast_info AS ci ON t.id = ci.movie_id;
```


PostgreSQL will now execute this query exactly as specified

### tbd
- Modify the operator selection to use different operators based on table size
- Implement join ordering
- Run actual benchmarks and measure execution time differences (too early ?)
