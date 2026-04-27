# [Reproducible Prototyping of Query Optimizer Components](https://dl.acm.org/doi/pdf/10.1145/3722212.3725637)



## Key Takeaways 

- **The textbook query optimizer has three components:**

   - Plan enumerator: constructs candidate plans that encode different access paths to various (intermediate) relations
   - Cost model: uses cardinalities of the child relations as a primary input
   - Cardinality estimator: computes the size of intermediate results as crucial input to the cost model
 
     <img width="562" height="425" alt="Screenshot 2026-04-27 at 17 27 17" src="https://github.com/user-attachments/assets/8dff2cfe-eb83-4007-bf35-f86c92459577" />


- **How prototypes are implemented:**

   - Patch: offers the best performance, but is the most technically challenging and the least accessible approach for external researchers. Patch-based prototypes are typically not usable across different PG versions
     
   - PG Extension: encapsulates modifications more cleanly and allows to use the extension across multiple PG versions, but relying on the public API makes certain changes to the optimizer impossible
   - Framework:  can accelerate prototyping and enhance the portability of algorithms across system versionsQuery optimization has three components: plan enumerator, cost model, and cardinality estimator (most research focuses on improving one of these three components)

- **Three key challenges:**

  - C1: Novel optimization concepts have to be evaluated in an end-to-end benchmark, since improvements under lab conditions do not necessarily translate into actual improvements of the query plans
  - C2: Prototypes should be implemented in a way that results can be easily reproduced, especially with respect to later PG versions
  - C3: Prototypes should be easily shareable, enabling researchers to integrate them into benchmarks with minimal effort

- **Optimizer Frameworks:**
  - PostBOUND: Has been reworked to model different kinds of optimization strategies as well as to benchmark and analyze them in a transparent and reproducible manner
  - Other frameworks (honorable mention :) ):

     - Apache Calcite: industry framework for building optimizers, but focused on Java ecosystem and cannot execute plans in actual relational databases like PostgreSQL. Benchmarks have to be conducted in a "lab" setting
      - LingoDB: MLIR-based optimizer with strong extensibility, but requires an entirely different mental model and benchmarking is limited to a prototypical system rather than a full-fledged relational database
      - PilotScope: framework specifically for learned methods, great flexibility across database systems, but its focus on learned algorithms excludes a large portion of different approaches

- **Reproducible Prototyping with PostBOUND**
    - PostBOUND's core structure:

      - Structured around optimization pipelines: each pipeline models a specific workflow and allows researchers to specify their own optimization strategies at different points
      - Two main pipelines: the textbook pipeline (cost model + cardinality estimator + plan enumerator) and the two-stage pipeline (join order first, then physical operator selection)
      - Researchers are free to provide their own algorithms for precisely those parts of the pipelines that they are concerned with. The framework then either selects reasonable defaults for components that the researcher did not specify or leaves the decision up to the target database
     
   - Hinting:
       - PostBOUND uses query hints instead of interfering with the target database directly
       - For PostgreSQL: supports both pg_hint_plan and pg_lab
       - pg_lab additionally allows to inject cardinalities for base tables and supports additional hints for physical operators
   - Benchmarking:
       - PostBOUND ensures all queries are executed on a database system in a well-defined state
       - Execution utilities gather extensive additional data relating the overall system state, the pipeline configuration etc.
       - Allows comparing a custom optimizer directly against the native PostgreSQL baseline

## Quotes
>"Novel optimization concepts have to be evaluated in an end-to-end benchmark, since improvements under 'lab conditions' do not necessarily translate into actual improvements of the query plans"


>"Prototypes should be implemented in a way that results can be easily reproduced, especially with respect to later PG versions"


>"Prototypes should be easily shareable, enabling researchers to integrate them into benchmarks with minimal effort"

>"a Python framework that models the query optimization process using abstract optimization stages"


>"allows researchers to inject their own strategies at specific stages, such as for cardinality estimation, or when selecting physical operators"


>"PostBOUND well-suited for both a rapid implementation of novel prototypes and for an open comparison of different approaches"
>"researchers are free to provide their own algorithms for precisely those parts of the pipelines that they are concerned with"


>"PostBOUND uses query hints instead of interfering with the target database directly"


>"the standardized preparation step ensures that all queries are executed on a database system in a well-defined state"


>"raise the participants' awareness of the importance of reproducible and openly accessible prototypes and equal assessments"

