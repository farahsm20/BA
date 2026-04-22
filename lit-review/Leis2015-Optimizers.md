# [How good are query optimizers, really?](https://www.vldb.org/pvldb/vol9/p204-leis.pdf)

## Summary
Main Point 

## Key Takeaways 
* Cardinality estimation is weak : - Databases often guess row counts very inaccurately
                                   - Errors grow with more joins (factors of 1000 or more)
                                   - Estimation errors may occasionally offset, giving acceptable plans despite inaccuracies
                                   - Correlations between tables are a major cause of these errors
* Cost model is less critical :  Even simple cost models perform well
                                The real problem is inaccurate cardinality estimates
  
* Join order matters :             - Different join orders → large performance differences
                                   - Finding a good join order is essential.
* Exhaustive search helps :        - Trying all bushy tree plans is better than shortcuts or heuristics (like "Greedy Operator Ordering")

## Quotes
>"In reality, cardinality estimates are usually computed based on simplifying assumptions like uniformity and independence. In realworld data sets, these assumptions are frequently wrong, which may lead to sub-optimal and sometimes disastrous plans.

> "Even exhaustive join order enumeration and a perfectly accurate cost model are worthless unless the cardinality estimates are (roughly) correct
                                                                           "
> "To measure the quality of base table cardinality estimates, we use the q-error, which is the factor by which an estimate differs from the true cardinality"

> "The q-error furthermore provides a theoretical upper bound for the plan quality if the q-errors of a query are bounded"

> "The estimates of the other systems are worse and seem to be based on per-attribute histograms, which do not work well for many predicates and cannot detect (anti-)correlations between attributes" (Including PostgreSQL)

> "For PostgreSQL 16% of the estimates for 1 join are wrong by a factor of 10 or more. This percentage increases to 32% with 2 joins, and to 52% with 3 joins"

> "Given the simplicity of PostgreSQL’s join estimation formula and the fact that its estimates are nevertheless competitive with the commercial systems, we can deduce that the current join size estimators are based on the independence assumption."

> tbd Estimates for TPC-H 
