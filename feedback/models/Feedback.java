public class Feedback {
    public int Id;
    public String message;
    public int rating;
    public int requestId;

    public Feedback(String message, int rating, int requestId) {
        this.message = message;
        this.rating = rating;
        this.requestId = requestId;
    }
}
