package com.api.retrieval.repository;


import com.api.retrieval.model.domain.Rating;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;

import java.util.List;

import static org.junit.jupiter.api.Assertions.*;

@SpringBootTest
public class RatingRepositoryTests {

    @Autowired
    RatingRepository ratingRepository;

    private Rating rating3;

    @BeforeEach
    void setUp() {
        Rating rating1 = new Rating(8.0, "model1");
        Rating rating2 = new Rating(9.0, "model2");
        Rating rating4 = new Rating(5.0, "model1");
        rating3 = new Rating(10.0, "model3");
        ratingRepository.save(rating1);
        ratingRepository.save(rating2);
        ratingRepository.save(rating4);
    }

    @Test
    public void TestFindAllRatings() {
        List<Rating> ratings = ratingRepository.findAll();
        assertTrue(ratings.size() > 0);
    }

    @Test
    public void TestFindByModelRatings() {
        List<Rating> ratingsFound = ratingRepository.findRatingsByModel("model1");
        assertTrue(ratingsFound.size() > 0);

    }

    @Test
    public void TestCreateRating() {
        Rating savedRating = ratingRepository.save(rating3);
        assertNotNull(savedRating);
        assertEquals(10.0, savedRating.getScore());
    }

    @Test
    public void TestUpdateRating() {
        Rating savedRating = ratingRepository.save(rating3);
        savedRating.setScore(5.0);

        Rating updatedRating = ratingRepository.save(savedRating);
        assertNotNull(updatedRating);
        assertEquals(5.0, updatedRating.getScore());
    }

    @Test
    public void TestGetAverageRatingByModel() {
        Double average = ratingRepository.getAverageByModel("model1");
        assertEquals(6.5, average);
    }
}
