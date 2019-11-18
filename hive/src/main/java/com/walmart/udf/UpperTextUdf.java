package com.walmart.udf;

import org.apache.hadoop.hive.ql.exec.Description;
import org.apache.hadoop.hive.ql.exec.UDF;
import org.apache.hadoop.io.Text;


@Description(
    name = "uppertextudf",
    value = "_FUNC_(string) - upper text "
)
public class UpperTextUdf extends UDF {

    public Text evaluate(final Text s) {
        if (s == null) {
            return null;
        }
        final String cleaned = s.toString().toUpperCase();
        return new Text(cleaned);
    }
}
