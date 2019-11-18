## Overview

Spark Pi project with sbt layout. 
Covered concepts:
- unit testing
- uber jar with dependencies shading 
- test-jar 


## Build

Assembly uber jar

`$ sbt assembly`


## Integration testing

TBD

`$ sbt it:assembly`

- assemble sources as uber jar *app-assembly.jar*
- assemble uber jar *app-assembly-test.jar* that contains all *it* test sources with all dependencies with _test_ scope
- submit both jars into classpath. 

Example below expects to have test libs, test sources and main sources in classpath. 

Also `org.scalatest.tools.Runner` will autodetec and run all `Spec`s from specified jar, return code different then 0 shows test failures.  

```
gcloud dataproc jobs submit spark submit \
    --cluster cluster-name --region region \
    --jars gs://path/to/app-assembly.jar,gs://path/to/app-assembly-test.jar \
    --files gs://path/to/app-assembly-test.jar \
    --class org.scalatest.tools.Runner
    -- -R app-assembly-test.jar -o
```
