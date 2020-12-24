import java.util.Arrays;
import java.util.StringJoiner;
import java.util.stream.IntStream;

public class Day23 {

    public static void main(String[] args) {
        assert "92658374".equals(part1(new int[] { 3, 8, 9, 1, 2, 5, 4, 6, 7 }, 10));
        assert "67384529".equals(part1(new int[] { 3, 8, 9, 1, 2, 5, 4, 6, 7 }, 100));

        assert 149245887792L == part2(new int[] { 3, 8, 9, 1, 2, 5, 4, 6, 7 }, 10_000_000);

        System.out.println(part1(new int[] { 6, 5, 3, 4, 2, 7, 9, 1, 8 }, 100));
        System.out.println(part2(new int[] { 6, 5, 3, 4, 2, 7, 9, 1, 8 }, 10_000_000));
    }

    private static String part1(final int[] data, final int nMoves) {
        final CrabList cl = new CrabList(data);
        for (int i = 0; i < nMoves; i++) {
            cl.move();
        }
        return cl.labels();
    }

    private static long part2(final int[] data, final int nMoves) {
        final int[] million = IntStream.rangeClosed(1, 1_000_000).toArray();
        for (int i = 0; i < data.length; i++) {
            million[i] = data[i];
        }

        final CrabList cl = new CrabList(million);
        for (int i = 0; i < nMoves; i++) {
            cl.move();
        }
        return cl.stars();
    }

}

class CrabList {

    private Node head;
    private final int max;
    private final int min;
    private final Node[] lookup;

    CrabList(final int[] values) {
        min = Arrays.stream(values).min().getAsInt();
        max = Arrays.stream(values).max().getAsInt();
        lookup = new Node[max - min + 1];

        lookup[values[0] - min] = head = new Node(values[0]);
        Node prev = head;
        for (int i = 1; i < values.length; i++) {
            final int v = values[i];
            prev.next = new Node(v);

            lookup[v - min] = prev = prev.next;
        }
        prev.next = head;
    }

    void move() {
        // cut out three nodes
        final Node first = head.next;
        final Node secnd = first.next;
        final Node third = secnd.next;
        head.next = third.next;

        int target = head.value - 1;
        while (target == first.value || target == secnd.value || target == third.value || target < min) {
            target--;
            if (target < min) {
                target = max;
            }
        }

        // find target and re-link nodes
        final Node destination = lookup[target - min];
        third.next = destination.next;
        destination.next = first;

        // next current element
        head = head.next;
    }

    String labels() {
        final StringBuilder sb = new StringBuilder();
        for (Node curr = afterOne(); curr.value != 1; curr = curr.next) {
            sb.append(curr.value);
        }
        return sb.toString();
    }

    private Node afterOne() {
        Node iter = head;
        while (iter.value != 1) {
            iter = iter.next;
        }
        return iter.next;
    }

    long stars() {
        final Node one = afterOne();
        return ((long) one.value) * one.next.value;
    }

    @Override
    public String toString() {
        final StringJoiner sj = new StringJoiner(" ");
        sj.add("(" + head.value + ")");
        for (Node curr = head.next; curr.value != head.value; curr = curr.next) {
            sj.add(Integer.toString(curr.value));
        }
        return sj.toString();
    }

    static class Node {

        final int value;
        Node next;

        Node(final int value) {
            this.value = value;
        }

    }

}
