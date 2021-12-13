package com.api.retrieval.controller;

import com.api.retrieval.model.Rating;
import com.api.retrieval.repository.RatingRepository;
import lombok.RequiredArgsConstructor;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.http.MediaType;
import org.springframework.test.web.reactive.server.WebTestClient;
import reactor.core.publisher.Mono;

@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
@RequiredArgsConstructor(onConstructor_ = @Autowired)
class RatingControllerTests {
    private final RatingRepository ratingRepository;
    private final WebTestClient webTestClient;

    @BeforeEach
    void populateRatingTable() {
        ratingRepository.save(Rating.builder()
                .model("EfficientNet")
                .score(8d)
                .build());
        ratingRepository.save(Rating.builder()
                .model("ResNet")
                .score(9.5)
                .build());
        ratingRepository.save(Rating.builder()
                .model("EfficientNet")
                .score(9.75)
                .build());
        ratingRepository.save(Rating.builder()
                .model("ResNet")
                .score(8.5)
                .build());
    }

    @AfterEach
    void clearRatingTable() {
        ratingRepository.deleteAll();
    }

    @Test
    void whenGetAllRatings_thenShouldReturnRatingList() {
        // Act and Assert
        webTestClient.get()
                .uri("/api/v1/ratings")
                .exchange()
                .expectStatus().isOk()
                .expectBodyList(Rating.class)
                .hasSize(4);
    }

    @Test
    void whenGetRatingsForModel_thenShouldReturnRatingList() {
        // Act and Assert
        webTestClient.get()
                .uri("/api/v1/ratings/EfficientNet")
                .exchange()
                .expectStatus().isOk()
                .expectBodyList(Rating.class)
                .hasSize(2);
    }

    @Test
    void whenGetAverageRatingForModel_thenShouldReturnDouble() {
        // Act and Assert
        webTestClient.get()
                .uri("/api/v1/ratings/EfficientNet/average")
                .exchange()
                .expectStatus().isOk()
                .expectBody(Double.class)
                .isEqualTo(8.875);
    }

    @Test
    void givenRating_whenAddRating_thenShouldReturnRating() {
        // Arrange
        Rating rating = Rating.builder()
                .id(13L)
                .model("EfficientNet")
                .score(8.5)
                .build();

        // Act and Assert
        webTestClient.post()
                .uri("/api/v1/ratings")
                .contentType(MediaType.APPLICATION_JSON)
                .body(Mono.just(rating), Rating.class)
                .exchange()
                .expectStatus().isCreated()
                .expectBody(Rating.class)
                .isEqualTo(rating);
    }

    @Test
    void givenRating_whenUpdateRating_thenShouldReturnRating() {
        // Arrange
        Rating rating = Rating.builder()
                .id(1L)
                .model("EfficientNet")
                .score(8.5)
                .build();

        // Act and Assert
        webTestClient.put()
                .uri("/api/v1/ratings/1")
                .contentType(MediaType.APPLICATION_JSON)
                .body(Mono.just(rating), Rating.class)
                .exchange()
                .expectStatus().isOk()
                .expectBody(Rating.class)
                .isEqualTo(rating);
    }
}
