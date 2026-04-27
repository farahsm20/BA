# [How good are query optimizers, really?](https://www.vldb.org/pvldb/vol9/p204-leis.pdf)

## Summary



## Key Takeaways 
- **Cardinality estimation is weak:**
  - Databases often guess row counts very inaccurately
  - Errors grow with more joins (factors of 1000 or more)
  - Estimation errors may occasionally offset, giving acceptable plans despite inaccuracies
  - Correlations between tables are a major cause of these errors

- **Cost model is less critical:**
  - Even simple cost models perform well
  - The real problem is inaccurate cardinality estimates

- **Join order matters:**
  - Different join orders → large performance differences
  - Finding a good join order is essential

- **Exhaustive search helps:**
  - Trying all bushy tree plans is better than shortcuts or heuristics (like "Greedy Operator Ordering")


## Experimental Setup (Reference Template
> "2.5 Experimental Setup
The cardinalities of the commercial systems were obtained using
a laptop running Windows 7. All performance experiments were
performed on a server with two Intel Xeon X5570 CPUs (2.9 GHz)
and a total of 8 cores running PostgreSQL 9.4 on Linux. PostgreSQL does not parallelize queries, so that only a single core was
used during query processing. The system has 64 GB of RAM,
which means that the entire IMDB database is fully cached in RAM.
Intermediate query processing results (e.g., hash tables) also easily
fit into RAM, unless a very bad plan with extremely large intermediate results is chosen.
We set the memory limit per operator (work mem) to
2 GB, which results in much better performance due to the
more frequent use of in-memory hash joins instead of external memory sort-merge joins. Additionally, we set the
buffer pool size (shared buffers) to 4 GB and the size
of the operating system’s buffer cache used by PostgreSQL
(effective cache size) to 32 GB. For PostgreSQL it is generally recommended to use OS buffering in addition to its own
buffer pool and keep most of the memory on the OS side. The defaults for these three settings are very low (MBs, not GBs), which
is why increasing them is generally recommended. Finally, by increasing the geqo threshold parameter to 18 we forced PostgreSQL to always use dynamic programming instead of falling
back to a heuristic for queries with more than 12 joins."

## Quotes
>"In reality, cardinality estimates are usually computed based on simplifying assumptions like uniformity and independence. In realworld data sets, these assumptions are frequently wrong, which may lead to sub-optimal and sometimes disastrous plans.

> "Even exhaustive join order enumeration and a perfectly accurate cost model are worthless unless the cardinality estimates are (roughly) correct
                                                                           "
> "To measure the quality of base table cardinality estimates, we use the q-error, which is the factor by which an estimate differs from the true cardinality"

> "The q-error furthermore provides a theoretical upper bound for the plan quality if the q-errors of a query are bounded"

> "The estimates of the other systems are worse and seem to be based on per-attribute histograms, which do not work well for many predicates and cannot detect (anti-)correlations between attributes" (Including PostgreSQL)

> "For PostgreSQL 16% of the estimates for 1 join are wrong by a factor of 10 or more. This percentage increases to 32% with 2 joins, and to 52% with 3 joins"

> "Given the simplicity of PostgreSQL’s join estimation formula and the fact that its estimates are nevertheless competitive with the commercial systems, we can deduce that the current join size estimators are based on the independence assumption."

> "Clearly, the TPC-H query workload does not present many hard challenges for cardinality estimators. In contrast, our workload contains queries that routinely lead to severe overestimation and underestimation errors, and hence can be considered a challenging benchmark for cardinality estimation."

> "PostgreSQL’s optimizer decides to introduce a nested-loop join (without an index lookup) because of a very low cardinality estimate, whereas in reality the true cardinality is larger"

> "The underlying reason why PostgreSQL chooses nested-loop joins is that it picks the join algorithm on a purely cost-based basis"

Tbd Good Plans Despite Bad Cardinalities
