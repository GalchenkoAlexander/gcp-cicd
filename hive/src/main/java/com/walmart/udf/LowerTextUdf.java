package com.walmart.udf;

import org.apache.hadoop.hive.ql.exec.Description;
import org.apache.hadoop.hive.ql.exec.UDF;
import org.apache.hadoop.io.Text;


@Description(
    name = "lowertextudf",
    value = "_FUNC_(string) - lower text "
)
public class LowerTextUdf extends UDF {

    public Text evaluate(final Text s) {
        if (s == null) {
            return null;
        }
        final String cleaned = s.toString().toLowerCase();
        return new Text(cleaned);
    }
}
