import java.io.BufferedReader;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileWriter;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.UnsupportedEncodingException;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

import org.kohsuke.args4j.CmdLineException;
import org.kohsuke.args4j.CmdLineParser;

public class Main {
    private static List<Integer> readNumbers(File source) {
        List<Integer> numbers = new ArrayList<Integer>();
        if (source.canRead()) {
            try {
                String line;
                FileInputStream fis = new FileInputStream(source);
                InputStreamReader in = new InputStreamReader(fis, "UTF-8");
                BufferedReader br = new BufferedReader(in);
                while ((line = br.readLine()) != null) {
                    numbers.add(Integer.parseInt(line));
                }
            } catch (FileNotFoundException e) {
                System.err.println("File was not found");
            } catch (UnsupportedEncodingException e) {
                System.err.println("Encoding was not supported");
                System.err.println(e);
            } catch (IOException e) {
                System.err.println("IOException");
                System.err.println(e);
            }
        }
        return numbers;
    }

    private static void writeNumbers(List<Integer> numbers, File dest) {
        try {
            FileWriter writer = new FileWriter(dest);
            for (int str : numbers) {
                writer.write(str + "\n");
            }
            writer.close();
        } catch (IOException e) {
            System.err.println("IOException");
            System.err.println(e);
        }
    }

    /**
     * @param args
     */
    public static void main(String[] args) {
        CommandLineValues values = new CommandLineValues(args);
        CmdLineParser parser = new CmdLineParser(values);

        try {
            parser.parseArgument(args);
        } catch (CmdLineException e) {
            System.exit(1);
        }

        System.out.println("Read numbers");
        List<Integer> numbers = readNumbers(values.getInput());
        Collections.sort(numbers);
        System.out.println("Write numbers");
        writeNumbers(numbers, values.getOuput());
        System.out.println("Finished");
    }
}
