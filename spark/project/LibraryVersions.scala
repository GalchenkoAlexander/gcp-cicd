

object LibraryVersions {

  import sbt._


  val TestAndIt = "test,it"
  val It = "it"

  val sparkVersion = "2.4.0"
  val scalaTestVersion = "3.0.5"

  val scalaTest = "org.scalatest" %% "scalatest" % scalaTestVersion % TestAndIt
  val junitTest = "junit" % "junit" % "4.12" % TestAndIt
  val sparkCore = "org.apache.spark" %% "spark-core" % sparkVersion % Provided 
  val sparkSql = "org.apache.spark" %% "spark-sql" % sparkVersion % Provided 
  val guava = "com.google.guava" % "guava" % "28.1-jre"
}
