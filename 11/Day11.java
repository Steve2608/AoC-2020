import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.Arrays;
import java.util.List;
import java.util.StringJoiner;

public class Day11 {

    public static void main(String[] args) throws IOException {
        // part1
        System.out.println(convergenceSeats(new Seats(readData())));
        // part2
        System.out.println(convergenceSeats(new VisibleSeats(readData())));
    }

    private static char[][] readData() throws IOException {
        final List<String> lines = Files.readAllLines(Paths.get("11/input.txt"));
        final char[][] data = new char[lines.size()][];
        for (int i = 0; i < data.length; i++) {
            final String line = lines.get(i);
            data[i] = new char[line.length()];
            for (int j = 0; j < data[i].length; j++) {
                data[i][j] = line.charAt(j);
            }
        }
        return data;
    }

    private static int convergenceSeats(final Seats s) {
        Seats prev = s, curr = s.nextGen();

        while(!prev.equals(curr)) {
            prev = curr;
            curr = curr.nextGen();
        }

        return curr.seats();
    }

}

class Seats {

    static final char FLOOR = '.', SEAT = '#', EMPTY = 'L';
    final char[][] seats;

    Seats(char[][] seats) {
        this.seats = seats.clone();
    }

    /**
     * @return pointer to seats array
     */
    char[][] getSeats() {
        return seats;
    }

    private int sum(final char target) {
        int sum = 0;
        for (final char[] line : seats) {
            for (final char c : line) {
                if (c == target)
                    sum++;
            }
        }
        return sum;
    }

    int seats() {
        return sum(SEAT);
    }

    int floors() {
        return sum(FLOOR);
    }

    int empty() {
        return sum(EMPTY);
    }

    @Override
    public int hashCode() {
        final int prime = 31;
        int result = 1;
        result = prime * result + Arrays.deepHashCode(seats);
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
        Seats other = (Seats) obj;
        if (!Arrays.deepEquals(seats, other.seats))
            return false;
        return true;
    }

    @Override
    public String toString() {
        final StringJoiner sj = new StringJoiner("\n");
        for (final char[] line : seats) {
            sj.add(new String(line));
        }
        return sj.toString();
    }

    Seats nextGen() {
        final char[][] next = new char[seats.length][];
        for (int i = 0; i < seats.length; i++) {
            next[i] = new char[seats[i].length];
            for (int j = 0; j < seats[i].length; j++) {
                next[i][j] = nextGenSeat(i, j);
            }
        }
        return new Seats(next);
    }

    char nextGenSeat(final int i, final int j) {
        final char seat = seats[i][j];
        if (seat == FLOOR)
            return FLOOR;

        final int n = countNeighbors(i, j);
        if (seat == EMPTY && n == 0)
            return SEAT;
        if (seat == SEAT && n >= 4)
            return EMPTY;
        return seat;
    }

    int countNeighbors(final int i, final int j) {
        int n = 0;
        for (int x = i - 1; x < i + 2; x++) {
            if (0 <= x && x < seats.length) {
                for (int y = j - 1; y < j + 2; y++) {
                    if (0 <= y && y < seats[x].length) {
                        if ((x != i || y != j) && seats[x][y] == SEAT) {
                            n++;
                        }
                    }
                }
            }
        }
        return n;
    }

}

class VisibleSeats extends Seats {

    VisibleSeats(char[][] seats) {
        super(seats);
    }

    @Override
    VisibleSeats nextGen() {
        final char[][] next = new char[seats.length][];
        for (int i = 0; i < seats.length; i++) {
            next[i] = new char[seats[i].length];
            for (int j = 0; j < seats[i].length; j++) {
                next[i][j] = nextGenSeat(i, j);
            }
        }
        return new VisibleSeats(next);
    }

    @Override
    char nextGenSeat(final int i, final int j) {
        final char seat = seats[i][j];
        if (seat == FLOOR)
            return FLOOR;

        final int n = countNeighbors(i, j);
        if (seat == EMPTY && n == 0)
            return SEAT;
        if (seat == SEAT && n >= 5)
            return EMPTY;
        return seat;
    }

    char seatInDirection(final int i, final int j, final int x, final int y) {
        if (x == 0 && y == 0) {
            throw new IllegalArgumentException(String.format("No direction was given! (%d, %d)", x, y));
        }

        for (int currX = i + x, currY = j + y; 0 <= currX && currX < seats.length && 0 <= currY
                && currY < seats[currX].length; currX += x, currY += y) {
            final char pos = seats[currX][currY];
            if (pos != FLOOR)
                return pos;
        }
        return FLOOR;
    }

    @Override
    int countNeighbors(final int i, final int j) {
        int n = 0;
        for (int x = -1; x < 2; x++) {
            for (int y = -1; y < 2; y++) {
                if ((x != 0 || y != 0) && seatInDirection(i, j, x, y) == SEAT) {
                    n++;
                }
            }
        }
        return n;
    }

}