package com.api.retrieval.repository;

import com.api.retrieval.model.Rating;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;

public interface RatingRepository extends JpaRepository<Rating, Long> {
    List<Rating> findRatingsByModel(String model);
}
