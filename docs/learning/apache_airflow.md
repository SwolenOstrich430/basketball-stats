# Definitions and Concepts
* <b>Directed Acyclic Graph (DAG)</b>: how pipelines are defined in Airflow. 
    * E.g., One thing -> leads to another -> processes that output -> puts it in storgage -> validate -> end.
* <b>Connections</b>: essentially set of parameters - such as username, password and hostname - along with the type of system that it connects to, and a unique name, called the conn_id.
* <b>Operators</b>: Similar to Hooks, Operators abstract away a specific unit of work in a pipeline. However, they exist a step higher than Hooks and define individual <b>Tasks</b> within a pipeline.
* <b>Hooks</b>: classes that act as helper functions to perform common tasks. There are many [built-in Hooks](https://airflow.apache.org/docs/apache-airflow/stable/public-airflow-interface.html#pythonapi-hooks) like S3 and Postgres related ones that allow for easy file-handling and data manipulation, etc.
* <b>Providers</b>: can contain operators, hooks, sensor, and transfer operators to communicate with a multitude of external systems, but they can also extend Airflow core with new capabilities. I.e., modules/packages/libraries. 
* <b>Sensors</b>: Sensors are a special type of Operator that are designed to do exactly one thing - wait for something to occur. It can be time-based, or waiting for a file, or an external event, but all they do is wait until something happens, and then succeed so their downstream tasks can run.
* <b>Templates</b>: variables, macros, and filters that are available at runtime either through context or available modules, like Pendulum, or user-provided arguments.

## DAG Class 
### Constructor
* <b>dag_id</b>: unique identifier for the pipeline that will be displayed in UI
* <b>schedule_interval</b>: cron-style string representing when the pipeline should be run
* <b>start_date</b>: defines when the pipeline should've started historically.
* <b>catchup</b>: determines how the Airflow scheduler handles past, unexecuted data intervals when a DAG is first activated or unpaused. I.e., if it started a week ago and never ran, a value fo true will rerun all days.

## Operators 
* <b>BashOperator</b>: takes a Bash command as a string as its only argument. 
* <b>PythonOperator</b>: requires a `task_id`, `python_callable` (Python function), and `dag` (the associated DAG as a variable).
    * Can't be Jinja templated 
        * but does get access to all context variables 

