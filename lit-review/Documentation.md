#   [Postbound Documentation](https://postbound.readthedocs.io/en/latest/index.html)
## **Optimization Pipelines**

Core of PostBOUND; each pipeline provides interfaces to customize different parts of the optimization process ( *stages*). Implementing
a new algorithm means selecting the appropriate pipeline and stage.

**TextBookOptimizationPipeline**
- Modelled after the traditional query optimizer architecture
- Uses a `PlanEnumerator` to produce and select candidate plans
- Uses a `CostModel` to assess plan quality
- Cost model typically relies on a `CardinalityEstimator` to estimate row counts per operator
  <img width="600" height="450" alt="image" src="https://github.com/user-attachments/assets/4712aa2b-167b-4480-9630-364a50cdd9fe" />


**MultiStageOptimizationPipeline**
- Performs optimization in sequential steps:
    1. `JoinOrderOptimization` : computes a join order
    2. `PhysicalOperatorSelection` : selects best physical operators
    3. `ParameterGeneration` : adds additional metadata to the plan
- Well-suited for scenarios where only part of the native optimizer decisions are overridden
- Example: implement your own join ordering and cardinality estimator, leave operator selection to the database
  
  <img width="435" height="521" alt="image" src="https://github.com/user-attachments/assets/de1d848c-fbad-4cc8-b771-010f408fa9af" />


> **Note:** Users do not need to implement all stages, PostBOUND fills gaps with reasonable defaults.




---





## **Hinting**

This is how PostBOUND actually forces PostgreSQL to use a specific plan.

**The core idea:**
PostBOUND makes optimization decisions in Python, then translates them into SQL query hints that force PostgreSQL to follow those decisions
when executing the query.

**How it works:**
1. PostBOUND generates a query plan (or partial decisions)
2. The hinting backend converts those decisions into database-specific hints
3. The hints are embedded in the SQL query as block comments
4. PostgreSQL executes the query following those hints
<img width="815" height="705" alt="Screenshot 2026-04-23 at 23 03 39" src="https://github.com/user-attachments/assets/67c7cc4d-bd88-4b05-9336-bbc6d39ccf13" />

**Example hint:**
```sql
/*+ HashJoin(t mi) */
SELECT * FROM title t JOIN movie_info mi ...
```

**Partial hints **
Hints don't have to cover the entire plan. You can enforce only join order and cardinality estimates and let PostgreSQL decide the
physical operators. This is the "fill the gaps" principle: you control what you want to study, PostgreSQL handles the rest.

**PostgreSQL specifics:**
PostgreSQL doesn't support hints natively : PostBOUND uses the `pg_hint_plan` extension. One limitation: `pg_hint_plan` doesn't support cardinality hints for base tables.

> **Key takeaway :** The `MultiStageOptimizationPipeline` uses partial hints extensively, making it the preferred pipeline when you only want to control specific optimization decisions.


**Implementing an Optimizer Prototype**

Developing a new optimization algorithm revolves around **optimization stages** and **optimization pipelines**. Implementing a prototype means mapping your idea to the best-fitting stage and combining it into the corresponding pipeline.

> **Note:** You do not need to implement all stages : PostBOUND fills gaps with reasonable defaults or falls back to the native optimizer.



---




## **Available Optimization Stages**

**Cardinality Estimation**  `CardinalityEstimator`
- Implement `calculate_estimate(query, intermediate)`: returns a cardinality estimate for a given intermediate result
- Usable in both `TextBookOptimizationPipeline` and `MultiStageOptimizationPipeline`
- In `MultiStageOptimizationPipeline`, acts as a plan parameterization stage

**Cost Models**  `CostModel`
- Implement `estimate_cost(query, plan)` — returns cost for a given subplan
- Only usable in `TextBookOptimizationPipeline`
- Cost model is a pure function — does not modify the plan directly

**Plan Enumeration**   `PlanEnumerator`
- Implement `generate_execution_plan(query, cost_model, cardinality_estimator)`
- Generates complete candidate plans including join order and physical operators
- Only usable in `TextBookOptimizationPipeline`

**Join Ordering**   `JoinOrderOptimization`
- Implement `optimize_join_order(query)` — returns a join order without physical operators
- Only usable in `MultiStageOptimizationPipeline` as the first step

**Physical Operator Selection**   `PhysicalOperatorSelection`
- Implement `select_physical_operators(query, join_order)`   assigns scan and join operators
- Only usable in `MultiStageOptimizationPipeline` as the second step
- Two modes: with or without a prior join ordering stage

**Plan Parameterization**   `ParameterGeneration`
- Implement `generate_plan_parameters(query, join_order, operator_assignment)`
- Handles cardinality estimates, parallelization, and database-specific settings
- Only usable in `MultiStageOptimizationPipeline` as the final step
- Can be used standalone to only override cardinality estimates

**Complete Plan Generation**   `CompleteOptimizationAlgorithm`
- Implement `optimize_query(query)` :returns a complete execution plan
- Useful when receiving plans from external components (e.g. learned optimizers)



**Best practices for all stages:**
- Call `super().__init__()` in constructor
- Implement `describe()` for introspection
- Implement `pre_check()` to restrict supported query types



**Advanced Scenarios**
- Combine multiple stages in one pipeline (preferred approach)
- Use Python multiple inheritance to implement multiple stages in a single class
- Implement a full `PlanEnumerator` if you need more control than individual stages provide
- Implement a custom `OptimizationPipeline` subclass if no built-in pipeline fits
