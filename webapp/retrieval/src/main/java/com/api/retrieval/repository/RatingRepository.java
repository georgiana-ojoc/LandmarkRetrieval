package com.api.retrieval.repository;

import com.api.retrieval.model.Rating;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface RatingRepository extends JpaRepository<Rating, Long> {
    List<Rating> findRatingsByModel(String model);

//    @Query(value = "SELECT AVG(r.score) FROM Rating r where r.model = :model")
//    Double getAverageByModel(String model);

    @Query(value = "SELECT AVG(r.score) FROM ratings r WHERE r.MODEL = :model", nativeQuery = true)
    Double getAverageByModel(String model);

}
