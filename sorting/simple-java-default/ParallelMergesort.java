import java.io.BufferedReader;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileWriter;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.UnsupportedEncodingException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

public class ParallelMergesort {
    private static String getPrefix() {
        Main.fileCounter++;
        String prefix = Integer.toString(Main.fileCounter);
        int i = prefix.length();
        while (3 - i >= 0) {
            prefix = "0" + prefix;
            i = prefix.length();
        }

        return prefix;
    }

    private static File mergeTwoFiles(File one, File two)
            throws FileNotFoundException, UnsupportedEncodingException,
            IOException {
        FileInputStream fis1 = new FileInputStream(one);
        InputStreamReader in1 = new InputStreamReader(fis1, "UTF-8");
        BufferedReader br1 = new BufferedReader(in1);
        FileInputStream fis2 = new FileInputStream(two);
        InputStreamReader in2 = new InputStreamReader(fis2, "UTF-8");
        BufferedReader br2 = new BufferedReader(in2);
        File myMergedFile = File.createTempFile(getPrefix(), null);

        FileWriter writer = new FileWriter(myMergedFile);

        String line1 = br1.readLine(), line2 = br2.readLine();
        int number1, number2, minNumber;
        if (line1 != null) {
            number1 = Integer.parseInt(line1);
        } else {
            number1 = Integer.MAX_VALUE;
        }

        if (line2 != null) {
            number2 = Integer.parseInt(line2);
        } else {
            number2 = Integer.MAX_VALUE;
        }

        while (line1 != null || line2 != null) {

            if (number1 < number2) {
                minNumber = number1;
                line1 = br1.readLine();
                if (line1 == null) {
                    throw new IllegalStateException();
                }
                number1 = Integer.parseInt(line1);
            } else {
                minNumber = number2;
                line2 = br2.readLine();
                if (line2 == null) {
                    throw new IllegalStateException();
                }
                number2 = Integer.parseInt(line2);
            }

            writer.write(minNumber);
        }

        fis1.close();
        fis2.close();
        in1.close();
        in2.close();
        br1.close();
        br2.close();

        return myMergedFile;
    }

    public static void parallelSorting(File src, File dest) throws IOException {
        long nrOfLines = SimpleSorting.count(src);
        long currentLine = 0;
        int[] part = new int[10000];

        FileInputStream fis = new FileInputStream(src);
        InputStreamReader in = new InputStreamReader(fis, "UTF-8");
        BufferedReader br = new BufferedReader(in);

        int workingSets = 0;
        List<File> workingFiles = new ArrayList<File>();
        while (currentLine < nrOfLines) {
            for (int i = 0; i < 10000; i++) {
                String line = br.readLine();
                if (line == null) {
                    throw new IllegalStateException();
                }
                part[i] = Integer.parseInt(line);
                currentLine++;
            }
            Arrays.sort(part);
            workingFiles.add(File.createTempFile(getPrefix(), null));
            workingSets++;
        }

        {
            int i = 0;
            while (workingFiles.size() > 1) {
                i++;
                workingFiles.add(mergeTwoFiles(workingFiles.get(0),
                        workingFiles.get(1)));
                workingFiles.remove(0);
                workingFiles.remove(0);
                System.out.println("Merge " + i);
            }
        }

        fis = new FileInputStream(workingFiles.get(0));
        in = new InputStreamReader(fis, "UTF-8");
        br = new BufferedReader(in);
        FileWriter writer = new FileWriter(dest);

        for (int i = 0; i < workingSets; i++) {
            String line = br.readLine();
            if (line != null) {
                writer.write(line);
            }
        }
    }
}
