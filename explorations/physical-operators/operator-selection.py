import postbound as pb


class BasicOperatorSelection(pb.PhysicalOperatorSelection):
    def __init__(self) -> None:
        super().__init__()

    def select_physical_operators(
        self,
        query: pb.SqlQuery,
        join_order: Optional[pb.JoinTree]
    ) -> pb.PhysicalOperatorAssignment:
        # Mode 2: no join order provided — generate all possible table combinations
        # and assign operators to all of them to restrict the native optimizer
        if join_order is None:
            joins = (intermediate for intermediate in pb.util.powerset(query.tables()) if len(intermediate) > 1)
        # Mode 1: join order provided — iterate through each join in the given order
        else:
            joins = (node.tables() for node in join_order.iterjoins())

        # create an empty assignment object to store our operator decisions
        assignment = pb.PhysicalOperatorAssignment()

        # assign sequential scan to every table in the query
        for tab in query.tables():
            assignment.add(pb.ScanOperator.SequentialScan, tab)

        # assign hash join to every join in the query
        for join in joins:
            assignment.add(pb.JoinOperator.HashJoin, join)

        # return the completed assignment — PostBOUND will translate this into hints
        return assignment


# --- Test ---

# connect to the local PostgreSQL container
pg = pb.postgres.connect(config_file="/Users/farahsomrani/BachelorArbeit/.psycopg_connection_job")

# parse query
query_parsed = pb.parse_query("""
    SELECT *
    FROM title t
    JOIN movie_info mi ON t.id = mi.movie_id
    JOIN cast_info ci ON t.id = ci.movie_id
""")

# check what operators got assigned
selector = BasicOperatorSelection()
assignment = selector.select_physical_operators(query_parsed, None)
print("Assignment:", assignment)

# build pipeline with our operator selection
pipeline = pb.MultiStageOptimizationPipeline(pg)
pipeline.setup_physical_operator_selection(BasicOperatorSelection())
pipeline = pipeline.build()

# optimize the query
result = pipeline.optimize_query(query_parsed)
print("Optimized query result:")
print(result)