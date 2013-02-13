import java.io.BufferedInputStream;
import java.io.BufferedReader;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileWriter;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.UnsupportedEncodingException;
import java.util.ArrayList;
import java.util.List;

public class SimpleSorting {
    /**
     * Get the number of lines of a textfile.
     *
     * @param source a text file
     * @author http://stackoverflow.com/a/453067/562769
     * @return the number of lines of source
     * @throws IOException
     */
    public static int count(File source) throws IOException {
        FileInputStream fis = new FileInputStream(source);
        InputStream is = new BufferedInputStream(fis);
        try {
            byte[] c = new byte[1024];
            int count = 0;
            int readChars = 0;
            boolean empty = true;
            while ((readChars = is.read(c)) != -1) {
                empty = false;
                for (int i = 0; i < readChars; ++i) {
                    if (c[i] == '\n')
                        ++count;
                }
            }
            return (count == 0 && !empty) ? 1 : count;
        } finally {
            is.close();
        }
    }

    public static int[] readNumbersInArray(File source) {
        int lines;
        try {
            lines = count(source);
        } catch (IOException e) {
            System.err.println("IOException");
            System.err.println(e);
            return new int[0];
        }

        int[] numbers = new int[lines];

        if (source.canRead()) {
            try {
                String line;
                FileInputStream fis = new FileInputStream(source);
                InputStreamReader in = new InputStreamReader(fis, "UTF-8");
                BufferedReader br = new BufferedReader(in);
                int i = 0;
                while ((line = br.readLine()) != null) {
                    numbers[i] = Integer.parseInt(line);
                    i++;
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
            } catch (java.lang.OutOfMemoryError e) {
                System.err.println("Not enough heap space.");
                System.err.println("Got " + numbers.size() + " numbers.");
                System.err.println(e);
            }
        }
        return numbers;
    }

    public static void writeNumbers(List<Integer> numbers, File dest) {
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

    public static void writeNumbers(int[] numbers, File dest) {
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
     * Sorts the file by repeatedly searching for the minimum.
     *
     * CAUTION! THIS METHOD CALL IS BAD FOR YOU DISK
     * @param src
     * @param dst
     * @throws IOException
     */
    public static void findMinSort(File src, File dst) throws IOException {
        FileWriter sorted = new FileWriter(dst);

        while (count(src) > 0) {
            FileInputStream fis = new FileInputStream(src);
            InputStreamReader in = new InputStreamReader(fis, "UTF-8");
            BufferedReader br = new BufferedReader(in);

            File tmp = File.createTempFile("remainingSortFile", null);
            FileWriter tmpWriter = new FileWriter(tmp);

            String line;
            int[] number = new int[2];
            int read = 0;

            // read the big file and seach for one minimum
            // at the end, the minimum will be in number[0]
            // and the file tmp will have all numbers except for the
            // minimum
            while ((line = br.readLine()) != null && line != "") {
                number[read] = Integer.parseInt(line);
                if (read == 1) {
                    read = 0;
                    if (number[0] < number[1]) {
                        String wline = Integer.toString(number[1]) + "\n";
                        tmpWriter.write(wline);
                    } else {
                        String wline = Integer.toString(number[0]) + "\n";
                        tmpWriter.write(wline);
                        number[0] = number[1];
                    }
                }
                read++;
            }
            String wline = Integer.toString(number[0]);
            sorted.write(wline + "\n");
            tmpWriter.close();
            src = tmp;

            br.close();
            in.close();
            fis.close();
        }
        sorted.close();
    }
}
