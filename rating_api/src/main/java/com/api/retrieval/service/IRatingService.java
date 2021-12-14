package com.api.retrieval.service;

import com.api.retrieval.exceptions.ModelNotFoundException;
import com.api.retrieval.model.domain.Rating;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public interface IRatingService {

    List<Rating> getAllRatings();

    List<Rating> getRatingsForModel(String model);

    Double getAverageRatingForModel(String model);

    Rating addRating(Rating rating);

    Rating updateRating(Long id, Rating newRating) throws ModelNotFoundException;
}
