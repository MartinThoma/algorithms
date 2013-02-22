import static org.junit.Assert.assertEquals;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;

import org.junit.BeforeClass;
import org.junit.Ignore;
import org.junit.Test;

public class StringMatchingTest {
    private static String text;

    @BeforeClass
    public static void testSetup() {
        String path = "/home/moose/workspace/String-Matching/src/bible.txt";
        File file = new File(path);

        if (!file.exists()) {
            System.err.print("The bible.txt was does not exist in ");
            System.err.println(file.getAbsoluteFile());
            System.exit(1);
        }

        try {
            FileReader fr = new FileReader(file);
            BufferedReader br = new BufferedReader(fr);
            StringBuilder sb = new StringBuilder();
            String line = br.readLine();

            while (line != null) {
                sb.append(line);
                sb.append("\n");
                line = br.readLine();
            }
            text = sb.toString();
        } catch (FileNotFoundException e) {
            System.err.print("The bible.txt was not found in ");
            System.err.println(file.getAbsoluteFile());
            System.err.println("Please adjust 'path'.");
            System.exit(1);
        } catch (IOException e) {
            System.err.println(e);
            System.exit(1);
        }
    }

    /* Test naiveStringMatching */
    @Test
    public void testNaiveStringMatching() {
        StringMatching s = new StringMatching(text);
        assertEquals(7, s.naiveStringMatching("beginning"));
    }

    @Test
    public void testNaiveStringMatchingMiddle() {
        StringMatching s = new StringMatching(text);
        assertEquals(1226144, s.naiveStringMatching("whom David"));
    }

    @Test
    public void testNaiveStringMatchingEnd() {
        StringMatching s = new StringMatching(text);
        assertEquals(
                4047354,
                s
                        .naiveStringMatching("Jesus Christ be with you all. Amen. END."));
    }

    @Test
    public void testNaiveStringMatchingNo() {
        StringMatching s = new StringMatching(text);
        assertEquals(-1, s.naiveStringMatching("Fuck."));
    }

    /* Test rabinKarp */

    @Ignore("Takes much time")
    @Test
    public void testRabinKarp() {
        StringMatching s = new StringMatching(text);
        assertEquals(7, s.rabinKarp("beginning", 31));
    }

    @Ignore("Takes much time")
    @Test
    public void testRabinKarpMiddle() {
        StringMatching s = new StringMatching(text);
        assertEquals(1226144, s.rabinKarp("whom David", 31));
    }

    @Ignore("Takes much time")
    @Test
    public void testRabinKarpEnd() {
        StringMatching s = new StringMatching(text);
        assertEquals(4047354, s.rabinKarp(
                "Jesus Christ be with you all. Amen. END.", 31));
    }

    /* Test suffixFunction */
    @Test
    public void testSuffixFunctionScript() {
        // It's private, so make it public first
        try {
            Class myTarget = Class.forName("StringMatching");
            java.lang.reflect.Method method = myTarget.getDeclaredMethod(
                    "suffixFunction", String.class, String.class);
            method.setAccessible(true);

            String pattern = "ab";
            StringMatching s = new StringMatching(text);
            assertEquals(1, method.invoke(s, pattern, "ccaca"));
            assertEquals(2, method.invoke(s, pattern, "ccab"));
            assertEquals(0, method.invoke(s, pattern, "abcc"));
        } catch (Exception e) {
            System.err.println(e);
        }
    }

    /* Test isSuffix */
    @Test
    public void testIsSuffix() {
        // It's private, so make it public first
        try {
            Class myTarget = Class.forName("StringMatching");
            java.lang.reflect.Method method = myTarget.getDeclaredMethod(
                    "isSuffix", String.class, String.class);
            method.setAccessible(true);

            String text = "Ich habe hier einen Text.";
            StringMatching s = new StringMatching(text);
            assertEquals(false, method.invoke(s, text, "Ich"));
            assertEquals(true, method.invoke(s, text, "Text."));
            assertEquals(true, method.invoke(s, text, "."));
        } catch (Exception e) {
            System.err.println(e);
        }
    }

    /* Test stringMatchingAutomaton */
    @Test
    public void testStringMatchingAutomaton() {
        StringMatching s = new StringMatching(text);
        assertEquals(7, s.stringMatchingAutomaton("beginning"));
    }

    @Test
    public void testStringMatchingAutomatonMiddle() {
        StringMatching s = new StringMatching(text);
        assertEquals(1226144, s.stringMatchingAutomaton("whom David"));
    }

    @Test
    public void testStringMatchingAutomatonEnd() {
        StringMatching s = new StringMatching(text);
        assertEquals(
                4047354,
                s
                        .stringMatchingAutomaton("Jesus Christ be with you all. Amen. END."));
    }

    @Test
    public void testStringMatchingAutomatonNo() {
        StringMatching s = new StringMatching(text);
        assertEquals(-1, s.stringMatchingAutomaton("Fuck."));
    }
}
