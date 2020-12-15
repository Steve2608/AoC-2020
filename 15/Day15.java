import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.HashMap;
import java.util.List;

public class Day15 {

    private static final int PART1 = 2020;
    private static final int PART2 = 30_000_000;

    public static void main(String[] args) throws IOException {
        final int[] data = readData();

        System.out.println(part1(data));
        System.out.println(part2(data));
    }

    private static int[] readData() throws IOException {
        final String s = Files.readAllLines(Paths.get("15/input.txt")).get(0);
        final String[] parts = s.split(",");
        final int[] data = new int[parts.length];

        for (int i = 0; i < data.length; i++) {
            data[i] = Integer.parseInt(parts[i]);
        }
        return data;
    }

    private static int part1(final int[] data) {
        return memoryGame(data, PART1);
    }

    private static int part2(final int[] data) {
        return memoryGame(data, PART2);
    }

    private static int memoryGame(final int[] data, final int target) {
        final HashMap<Integer, Tup2> memory = new HashMap<>();
        for (int i = 0; i < data.length; i++) {
            memory.put(data[i], new Tup2(i + 1));
        }

        int prev = data[data.length - 1];
        for (int i = data.length + 1; i <= target; i++) {
            final Tup2 tup = memory.get(prev);

            if (tup.getSecnd() == 0) {
                memory.get(prev = 0).rotate(i);
            } else {
                final Tup2 secondPlus = memory.get(prev = tup.diff());
                if (secondPlus != null) {
                    secondPlus.rotate(i);
                } else {
                    memory.put(prev, new Tup2(i));
                }
            }
        }
        return prev;
    }

}

class Tup2 {

    private int first;
    private int secnd;

    Tup2(final int first) {
        this(first, 0);
    }

    Tup2(final int first, final int secnd) {
        this.first = first;
        this.secnd = secnd;
    }

    public int getFirst() {
        return first;
    }

    public int getSecnd() {
        return secnd;
    }

    public int diff() {
        return first - secnd;
    }

    public void rotate(final int new_first) {
        secnd = first;
        first = new_first;
    }

    @Override
    public int hashCode() {
        final int prime = 31;
        int result = 1;
        result = prime * result + first;
        result = prime * result + secnd;
        return result;
    }

    @Override
    public boolean equals(Object obj) {
        if (this == obj)
            return true;
        if (obj == null)
            return false;
        if (getClass() != obj.getClass())
            return false;
        Tup2 other = (Tup2) obj;
        if (first != other.first)
            return false;
        if (secnd != other.secnd)
            return false;
        return true;
    }

    @Override
    public String toString() {
        return "Tup2 [first=" + first + ", secnd=" + secnd + "]";
    }

}