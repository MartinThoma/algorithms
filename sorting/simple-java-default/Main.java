import java.io.IOException;
import java.util.Arrays;

import org.kohsuke.args4j.CmdLineException;
import org.kohsuke.args4j.CmdLineParser;

public class Main {
    public static String version = "1.0.7";
    public static int fileCounter = 0;

    public static void main(String[] args) {
        CommandLineValues values = new CommandLineValues(args);
        CmdLineParser parser = new CmdLineParser(values);

        try {
            parser.parseArgument(args);
        } catch (CmdLineException e) {
            System.exit(1);
        }

        System.out.println("Version " + version);

        if (values.getMethod().equals("simple")) {
            System.out.println("Read numbers");
            long startTime = System.nanoTime();
            // List<Integer> numbers = readNumbers(values.getInput());
            int[] numbers = SimpleSorting.readNumbersInArray(values.getInput());
            long endTime = System.nanoTime();
            System.out.println("Needed " + (endTime - startTime) / 1000000000.0
                    + " seconds for reading");

            startTime = System.nanoTime();
            // Collections.sort(numbers);
            Arrays.sort(numbers);
            endTime = System.nanoTime();
            System.out.println("Needed " + (endTime - startTime) / 1000000000.0
                    + " seconds for sorting");

            System.out.println("Write numbers");
            startTime = System.nanoTime();
            SimpleSorting.writeNumbers(numbers, values.getOutput());
            endTime = System.nanoTime();
            System.out.println("Needed " + (endTime - startTime) / 1000000000.0
                    + " seconds for writing");
        } else if (values.getMethod().equals("parallel")) {
            long startTime = System.nanoTime();
            try {
                ParallelMergesort.parallelSorting(values.getInput(), values.getOutput());
            } catch (IOException e) {
                System.err.println("IOException occured:");
                System.err.println(e);
            }
            long endTime = System.nanoTime();
            System.out.println("Needed " + (endTime - startTime) / 1000000000.0
                    + " seconds for reading, sorting and writing.");
        } else if (values.getMethod().equals("minSearch")) {
            try {
                SimpleSorting.findMinSort(values.getInput(), values.getOutput());
            } catch (IOException e) {
                System.err.println(e);
            }
        } else {
            System.err.println("You didn't specify a valid sorting "
                    + "procedure.");
        }

        System.out.println("Finished");
    }
}
