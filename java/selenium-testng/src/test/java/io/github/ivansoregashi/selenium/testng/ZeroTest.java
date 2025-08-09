package io.github.ivansoregashi.selenium.testng;
import org.testng.annotations.Test;
import static org.testng.Assert.assertTrue;

public class ZeroTest {
    @Test
    public void testNothing() {
        System.out.println("running testNothing");
        assertTrue((1 == 1));
    }
}
