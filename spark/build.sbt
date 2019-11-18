import LibraryVersions._


val dependencies = Seq(
  sparkCore,
  sparkSql,
  guava,
  scalaTest,
  junitTest
)

val assemblySettings = Seq(
  /* Exclude Scala from the assembly jar as it's provided by the Spark distribution */
  assemblyOption in assembly := (assemblyOption in assembly).value.copy(includeScala = false),
  assemblyMergeStrategy in assembly := {
    case PathList("example-config.conf") => MergeStrategy.discard // exclude some file from jar
    case PathList("META-INF", "MANIFEST.MF") => MergeStrategy.discard
    case x =>
      val oldStrategy = (assemblyMergeStrategy in assembly).value
      oldStrategy(x)
  },
  assemblyShadeRules in assembly := Seq(
    //
    // Simulate situations where the Spark application’s dependencies conflict with Hadoop’s own dependencies.
    // This conflict results from the fact that Hadoop injects its dependencies into the application’s classpath,
    // and therefore Hadoop’s dependencies take precedence over the application’s dependencies.
    //
    // @see https://cloud.google.com/blog/products/data-analytics/managing-java-dependencies-apache-spark-applications-cloud-dataproc
    //
    ShadeRule.rename("com.google.guava.**" -> "shaded.com.google.guava.@1").inAll
  ),
  assemblyJarName in (IntegrationTest, assembly) := s"${name.value}-${version.value}-assembly.jar"
)


//
// TODO: example how to manage shaded test-jar 
//
//val itTestAssemblySettings = Seq(
//  // exclude scala libs as they are in a classpath
//  assemblyOption in (IntegrationTest, assembly) := (assemblyOption in (IntegrationTest, assembly))
//    .value.copy(includeScala = false),
//
//  assemblyMergeStrategy in (IntegrationTest, assembly) := {
//    case PathList("META-INF", "MANIFEST.MF") => MergeStrategy.discard
//    case x =>
//      val oldStrategy = (assemblyMergeStrategy in assembly).value
//      oldStrategy(x)
//  },
//
//  // Workaround to exclude provided dependencies from
//  // assembled test-jar
//  // see: https://github.com/sbt/sbt-assembly/issues/295
//  // 
//  // Build assembly with only it-test sources and libs with `it` scope
//  //
//  fullClasspath in (IntegrationTest, assembly) := {
//    
//    val testSrc = (fullClasspath in IntegrationTest).value
//      .filter({x => x.data.getPath.contains("it-classes")})
//
//    val testDep = (managedClasspath in IntegrationTest).value.toSet
//    val compileDep = (managedClasspath in Compile).value.toSet
//    val runtimeDep = (managedClasspath in Runtime).value.toSet
//    
//    val providedDep = compileDep -- runtimeDep
//    
//    testSrc ++ (testDep -- providedDep)
//  },
//  assemblyJarName in (IntegrationTest, assembly) := s"${name.value}-${version.value}-assembly-test.jar"
//)
//
// Project
//  .inConfig(IntegrationTest)(baseAssemblySettings ++ itTestAssemblySettings)
//

val settings = Seq(
  organization := "com.sparkexamples",
  name := "root",
  scalaVersion := "2.11.12",
  libraryDependencies ++= dependencies,
  compileOrder in Compile := CompileOrder.Mixed,
  compileOrder in Test := CompileOrder.Mixed,
  fork in run := true,
  fork in Test := true,
  fork in IntegrationTest := true,
  fork in testOnly := true,
  connectInput in run := true,
  parallelExecution in Test := false,
  parallelExecution in IntegrationTest := false
)



val main =
  project
    .in(file("."))
    .configs(IntegrationTest)
    .settings(
      Defaults.itSettings ++ assemblySettings ++ settings: _*
    )
