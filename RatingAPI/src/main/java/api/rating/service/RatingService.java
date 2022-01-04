package api.rating.service;

import api.rating.exceptions.ModelNotFoundException;
import api.rating.model.domain.Rating;
import api.rating.repository.RatingRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;

@Service
public class RatingService implements IRatingService {
    @Autowired
    private RatingRepository ratingRepository;

    public List<Rating> getAllRatings() {
        return ratingRepository.findAll();
    }

    public List<Rating> getRatingsForModel(String model) {
        return ratingRepository.findRatingsByModel(model);
    }

    public Double getAverageRatingForModel(String model) {
        return ratingRepository.getAverageByModel(model);
    }

    @Transactional
    public Rating addRating(Rating rating) {
        return ratingRepository.save(rating);
    }

    @Transactional
    public Rating updateRating(Long id, Rating newRating) throws ModelNotFoundException {
        Rating rating = ratingRepository.findById(id)
                .orElseThrow(() -> new ModelNotFoundException("Rating not found " + id));

        rating.setScore(newRating.getScore());
        return ratingRepository.save(rating);
    }
}
