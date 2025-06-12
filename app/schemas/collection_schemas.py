# collection_field_definitions = {
#     "analysis": [
#         {"name": "name", "type": "string"},
#         {"name": "analytics_type", "type": "string"},
#         {"name": "analytics_goal", "type": "string"},
#         {"name": "input_features", "type": "list"},
#         {"name": "preprocess_actions", "type": "json"},
#         {"name": "datasets", "type": "list"},
#         {"name": "model", "type": "string"},
#         {"name": "results_type_conf", "type": "list"},
#         {"name": "filters", "type": "list"},
#     ],

#     "dataset": [
#         {"name": "name", "type": "string"},
#         {"name": "db_name", "type": "string"},
#         {"name": "collection_name", "type": "string"},
#         {"name": "id_name", "type": "string"},
#         {"name": "last_id", "type": "string"},  # or "int" if you add type coercion
#         {"name": "attributes", "type": "list"}
#     ],

#     "deployment": [
#         {"name": "name", "type": "string"},
#         {"name": "analysis", "type": "string"},  # ObjectId → will be string input
#         {"name": "last_id", "type": "json"},     # JSON: key-value mapping
#         {"name": "deployment_conf", "type": "string"},  # ObjectId
#         {"name": "info", "type": "json"}         # Nested object
#         # {"name": "name", "type": "string"},
#         # {"name": "analysis", "type": "reference", "collection": "analysis", "label_field": "name"},
#         # {"name": "last_id", "type": "json"},
#         # {"name": "deployment_conf", "type": "reference", "collection": "deployment_conf", "label_field": "name"},
#         # {"name": "info", "type": "json"}
#     ],

#     "deployment_conf": [
#         {"name": "name", "type": "string"},
#         {"name": "analysis", "type": "string"},          # ObjectId
#         {"name": "deployment_mode", "type": "string"}
#         # {"name": "name", "type": "string"},
#         # {"name": "analysis", "type": "reference", "collection": "analysis", "label_field": "name"},
#         # {"name": "deployment_mode", "type": "choice", "category": "deployment_mode"}
#     ],

#     "model": [
#         {"name": "name", "type": "string"},
#         {"name": "algorithm", "type": "string"},
#         {"name": "resolver", "type": "string"},
#         {"name": "input_attributes", "type": "list"},
#         {"name": "model_data", "type": "json"},
#         {"name": "status", "type": "string"},
#         {"name": "train", "type": "string"}  # or "bool" if you handle it
#     ],

#     "project": [
#         {"name": "name", "type": "string"},
#         {"name": "category", "type": "string"},
#         {"name": "value", "type": "list"}  # comma-separated in form
#     ],

#     "results": [
#         {"name": "name", "type": "string"},
#         {"name": "type", "type": "list"},
#         {"name": "attributes", "type": "json"},     # dict of field names and types
#         {"name": "input_values", "type": "list"},   # could be empty or full in future
#         {"name": "results", "type": "string"},
#         {"name": "deployment", "type": "string"}    # ObjectId as string
#     ],
# }
collection_field_definitions = {
    "analysis": [
        {"name": "name", "type": "string"},
        {"name": "analytics_type", "type": "choice", "category": "analytics_types"},
        {"name": "analytics_goal", "type": "choice", "category": "analytics_goals"},
        {"name": "input_features", "type": "list"},
        {"name": "preprocess_actions", "type": "json"},
        {"name": "datasets", "type": "reference", "collection": "dataset", "label_field": "name"},
        {"name": "model", "type": "reference", "collection": "model", "label_field": "name"},
        {"name": "results_type_conf", "type": "choice", "category": "result_type"},
        {"name": "filters", "type": "choice", "category": "analytics_filters"}
    ],

    "dataset": [
        {"name": "name", "type": "string"},
        {"name": "db_name", "type": "string"},
        {"name": "collection_name", "type": "string"},
        {"name": "id_name", "type": "string"},
        {"name": "last_id", "type": "string"},  # or "int" if coercion used
        {"name": "attributes", "type": "list"}
    ],

    "deployment": [
        {"name": "name", "type": "string"},
        {"name": "analysis", "type": "reference", "collection": "analysis", "label_field": "name"},
        {"name": "last_id", "type": "json"},
        {"name": "deployment_conf", "type": "reference", "collection": "deployment_conf", "label_field": "name"},
        {"name": "info", "type": "json"}
    ],

    "deployment_conf": [
        {"name": "name", "type": "string"},
        {"name": "analysis", "type": "reference", "collection": "analysis", "label_field": "name"},
        {"name": "deployment_mode", "type": "choice", "category": "deployment_mode"}
    ],

    "model": [
        {"name": "name", "type": "string"},
        {"name": "algorithm", "type": "choice", "category": "model_algorithm"},
        {"name": "resolver", "type": "choice", "category": "model_resolvers"},
        {"name": "input_attributes", "type": "list"},
        {"name": "model_data", "type": "json"},
        {"name": "status", "type": "choice", "category": "model_status"},
        {"name": "train", "type": "string"}  # could be bool if cast
    ],

    "project": [
        {"name": "name", "type": "string"},
        {"name": "category", "type": "string"},
        {"name": "value", "type": "list"}
    ],

    "results": [
        {"name": "name", "type": "string"},
        {"name": "type", "type": "choice", "category": "result_type"},
        {"name": "attributes", "type": "json"},
        {"name": "input_values", "type": "list"},
        {"name": "results", "type": "string"},
        {"name": "deployment", "type": "reference", "collection": "deployment", "label_field": "name"}
    ]
}
