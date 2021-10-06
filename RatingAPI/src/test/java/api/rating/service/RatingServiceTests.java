package api.rating.service;

import api.rating.exceptions.ModelNotFoundException;
import api.rating.model.domain.Rating;
import api.rating.repository.RatingRepository;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import java.util.ArrayList;
import java.util.List;
import java.util.Optional;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.mockito.Mockito.when;

@ExtendWith(value = MockitoExtension.class)
class RatingServiceTests {
    @Mock
    private RatingRepository ratingRepository;

    @InjectMocks
    private RatingService ratingService;

    @Test
    void whenGetAllRatings_thenShouldReturnRatingList() {
        // Arrange
        List<Rating> ratings = new ArrayList<>();
        ratings.add(Rating.builder()
                .id(1L)
                .model("EfficientNet")
                .score(8d)
                .build());
        ratings.add(Rating.builder()
                .id(2L)
                .model("ResNet")
                .score(9d)
                .build());

        when(ratingRepository.findAll()).thenReturn(ratings);

        // Act and Assert
        assertEquals(ratings, ratingService.getAllRatings());
    }

    @Test
    void whenGetRatingsForModel_thenShouldReturnRatingList() {
        // Arrange
        List<Rating> ratings = new ArrayList<>();
        ratings.add(Rating.builder()
                .id(1L)
                .model("EfficientNet")
                .score(8d)
                .build());
        ratings.add(Rating.builder()
                .id(2L)
                .model("EfficientNet")
                .score(9d)
                .build());

        when(ratingRepository.findRatingsByModel("EfficientNet")).thenReturn(ratings);

        // Act and Assert
        assertEquals(ratings, ratingService.getRatingsForModel("EfficientNet"));
    }

    @Test
    void whenGetAverageRatingForModel_thenShouldReturnDouble() {
        // Arrange
        when(ratingRepository.getAverageByModel("EfficientNet")).thenReturn(8.5);

        // Act and Assert
        assertEquals(8.5, ratingService.getAverageRatingForModel("EfficientNet"));
    }

    @Test
    void givenRating_whenAddRating_thenShouldReturnRating() {
        // Arrange
        Rating rating = Rating.builder()
                .id(1L)
                .model("EfficientNet")
                .score(8d)
                .build();

        when(ratingRepository.save(rating)).thenReturn(rating);

        // Act and Assert
        assertEquals(rating, ratingService.addRating(rating));
    }

    @Test
    void givenNonExistingRating_whenUpdateRating_thenShouldThrowModelNotFound() {
        // Arrange
        Rating rating = Rating.builder()
                .id(1L)
                .model("EfficientNet")
                .score(8d)
                .build();

        when(ratingRepository.findById(1L)).thenReturn(Optional.empty());

        // Act and Assert
        assertThrows(ModelNotFoundException.class, () -> ratingService.updateRating(1L, rating));
    }

    @Test
    void givenRating_whenUpdateRating_thenShouldReturnRating() throws ModelNotFoundException {
        // Arrange
        Rating oldRating = Rating.builder()
                .id(1L)
                .model("EfficientNet")
                .score(8d)
                .build();
        Rating newRating = Rating.builder()
                .id(1L)
                .model("EfficientNet")
                .score(9d)
                .build();

        when(ratingRepository.findById(1L)).thenReturn(Optional.of(oldRating));

        oldRating.setScore(newRating.getScore());
        when(ratingRepository.save(oldRating)).thenReturn(newRating);

        // Act and Assert
        assertEquals(newRating, ratingService.updateRating(1L, oldRating));
    }
}
