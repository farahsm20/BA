
# Bachelor Thesis: Empirical Evaluation of Query Optimization Techniques Using Controlled Execution Plans 

- Use PostBOUND to implement different query optimization techniques
- Force PostgreSQL to use a specific query plan
- Incrementally enable optimizations in different combinations
- Measure impact on query performance

## Metrics
- Query execution time
- Buffer usage (using EXPLAIN ANALYZE)
- Possibly CPU or IO stats

## Optimizations

- Determine first what parts of the query plan are controllable by PostBOUND
- Check text books and classical papers for implementations
- Possibly
    - Join ordering
        - Exhaustive Search using Dynamic Programming
        - Greedy
        - Local search with heuristics
    - Predicate pushdown
    - Projection pruning
    - Join algorithm selection
    - Index usage
    - Table scan selection
    - Cardinality estimation
        - Simulate statistics or use from Postgres
        - Estimated vs. exact cardinalities

## Benchmark Datasets

- TPC-H
- Join Order Benchmark
- Star Schema Benchmark
    - Subqueries

## Results

- Show comparison to Postgres native query plan and random join order selection
- Show impact of optimization techniques
    - Identify query types that benefit most
    - Impact between logical and physicial optimizations
    - What techniques habe the most impact? complexity vs. reward?


