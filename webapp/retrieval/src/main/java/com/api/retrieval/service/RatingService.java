package com.api.retrieval.service;

import com.api.retrieval.exceptions.ModelNotFoundException;
import com.api.retrieval.model.Rating;
import com.api.retrieval.repository.RatingRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;

@Service
public class RatingService {
    @Autowired
    private RatingRepository ratingRepository;

    public List<Rating> getAllRatings() {
        return ratingRepository.findAll();
    }

    public List<Rating> getRatingsForModel(String model) {
        return ratingRepository.findRatingsByModel(model);
    }

    @Transactional
    //https://docs.spring.io/spring-framework/docs/4.2.x/spring-framework-reference/html/transaction.html#transaction-declarative
    //The Spring Framework’s declarative transaction management already uses AOP
    // For example, you can insert custom behavior in the case of transaction rollback. You can also add arbitrary advice, along with the transactional advice.
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
