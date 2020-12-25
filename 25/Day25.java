public class Day25 {

    private static final int MOD = 20201227;

    public static void main(String[] args) {
        System.out.println(part1(6270530, 14540258));
    }

    private static int part1(final int card, final int door) {
        final int n_door = transform(door, 7);
        final int key = transformN(n_door, card);

        assert transformN(transform(card, 7), door) == key;
        return key;
    }

    private static int transformN(final int n, final int subjectNumber) {
        return transformN(n, subjectNumber, MOD);
    }

    private static int transformN(final int n, final int subjectNumber, final int mod) {
        long value = 1;
        for (int i = 0; i < n; i++) {
            value *= subjectNumber;
            value %= mod;
        }
        return (int) value;
    }

    private static int transform(final int n, final int subjectNumber) {
        return transform(n, subjectNumber, MOD);
    }

    private static int transform(final int target, final int subjectNumber, final int mod) {
        long value = 1;
        int i = 0;
        while (value != target) {
            value *= subjectNumber;
            value %= mod;
            i++;
        }
        return i;
    }
}