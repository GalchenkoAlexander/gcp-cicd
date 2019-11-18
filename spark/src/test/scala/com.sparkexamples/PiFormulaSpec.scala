package com.sparkexamples

import org.scalatest.{FlatSpec, Matchers}

class PiFormulaSpec extends FlatSpec with Matchers {

  "PiFormula" should "calculate pi" in {
    val f = new PiFormula with SparkFactory  {
    }

    f.calcPi(100, 2) shouldBe 400D
  }

}
