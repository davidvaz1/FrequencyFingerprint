import java.util.Scanner;

public class FrequencyFingerprint {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int arr[] = new int[26];
        System.out.println("Enter a string");
        String str = sc.nextLine().trim();
        str = str.toUpperCase();
        int sl = str.length();
        char c;
        for (int i = 0 ; i < sl; i ++) {
            c = str.charAt(i);
            if (! (Character.isLetter(c)))
                continue;
            else {
                for (char x = 'A', j = 0; x <= 'Z'; x++, j++) {
                    if (x == c) {
                        arr[j]++;
                        break;
                    }
                }
            }
        }
        
        System.out.println("\n" + "Frequency Fingerprint");
        for (int i = 0, x = 'A' ; i < arr.length; i++, x++) {
            System.out.println((char)x + "= \t" + arr[i]);
        }
    }
}
