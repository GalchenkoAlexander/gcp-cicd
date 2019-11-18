package com.sparkexamples



import org.apache.spark.sql.SparkSession

import scala.math.random


/**
  * Pi calculation is taken from
  * <a href="https://github.com/apache/spark/blob/master/examples/src/main/scala/org/apache/spark/examples/SparkPi.scala">SparkPi.scala</a>
  * official example.
  *
  * Code was refactored to simulate some Spark pipeline with kind of logic to show unit and integration tests also.
  */
object SparkPi extends SparkFactory  with PiFormula {

  def main(args: Array[String]): Unit = {

    val slices = if (args.length > 0) args(0).toInt else 2
    val n = math.min(100000L * slices, Int.MaxValue).toInt // avoid overflow

    val count = estimateCount(n, slices)
    val pi = calcPi(count, n)

    println(s"Pi is roughly $pi")

    spark.stop()
  }

  def estimateCount(n: Int, slices: Int): Int = spark.sparkContext.parallelize(1 until n, slices).map { _ =>
    val x = random * 2 - 1
    val y = random * 2 - 1
    if (x*x + y*y <= 1) 1 else 0
  }.reduce(_ + _)

}


trait SparkFactory {

  lazy val spark: SparkSession = SparkSession
    .builder
    .appName("Spark Pi")
    .getOrCreate()

}


trait PiFormula { this: SparkFactory =>

  def calcPi(count: Int, n: Int): Double = 4.0 * count / (n - 1)

}
