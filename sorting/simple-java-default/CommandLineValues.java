import java.io.File;

import org.kohsuke.args4j.CmdLineException;
import org.kohsuke.args4j.CmdLineParser;
import org.kohsuke.args4j.Option;

/**
 * This class handles the programs arguments.
 */
public class CommandLineValues {
    @Option(name = "-i", aliases = { "--input" }, required = true,
            usage = "input file with random integers seperated by" +
                    "newline \\n characters")
    private File input;

    @Option(name = "-o", aliases = { "--output" }, required = true,
            usage = "sorted output file")
    private File output;

    private boolean errorFree = false;

    public CommandLineValues(String... args) {
        CmdLineParser parser = new CmdLineParser(this);
        parser.setUsageWidth(80);
        try {
            parser.parseArgument(args);

            if (!getInput().isFile()) {
                throw new CmdLineException(parser,
                        "--input is no valid input file.");
            }

            errorFree = true;
        } catch (CmdLineException e) {
            System.err.println(e.getMessage());
            parser.printUsage(System.err);
        }
    }

    /**
     * Returns whether the parameters could be parsed without an
     * error.
     *
     * @return true if no error occurred.
     */
    public boolean isErrorFree() {
        return errorFree;
    }

    /**
     * Returns the source file.
     *
     * @return The source file.
     */
    public File getInput() {
        return input;
    }

    /**
     * Returns the source file.
     *
     * @return The source file.
     */
    public File getOuput() {
        return output;
    }
}