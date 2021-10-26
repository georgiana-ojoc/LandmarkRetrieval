import java.util.Optional;

public class FeedbackService {
    private final FeedbackRepository feedbackRepository;

    public FeedbackService(FeedbackRepository feedbackRepository) {
        this.feedbackRepository = feedbackRepository;
    }

    public Optional<Feedback> get() {
        ;
    }

    /** Spring AOP will create a proxy class and will wrap the annotated method -> What happens behind the scenes:
     public class FeedbackServiceProxy extends FeedbackService {
        Transaction tx = entityManager.getTransaction();

        @Override
        public void create(Feedback feedback) {
            try {
                tx.createANewTransactionIfNecessary();

                super.create(feedback);

                tx.commitTransaction();
                }
            catch(RuntimeException e) {
                tx.rollbackTransaction();
            }
        }
     }
     **/
    @Transactional
    public void create(Feedback feedback) {
         /*  ....
            feedbackRepository.create(feedback)
         */
    }
}
