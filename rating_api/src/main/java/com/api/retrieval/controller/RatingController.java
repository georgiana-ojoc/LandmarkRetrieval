package com.api.retrieval.controller;

import com.api.retrieval.aspect.annotations.MonitorTime;
import com.api.retrieval.exceptions.ModelNotFoundException;
import com.api.retrieval.model.Rating;
import com.api.retrieval.service.RatingService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.*;

import javax.validation.Valid;
import java.util.List;

@RestController
@RequestMapping("/api/v1/ratings")
@Validated
@CrossOrigin
public class RatingController {

    @Autowired
    private RatingService ratingService;

    @GetMapping()
    @MonitorTime
    public ResponseEntity<List<Rating>> getAllRatings() {
        List<Rating> ratings = ratingService.getAllRatings();
        return ResponseEntity.ok(ratings);
    }

    @GetMapping("/{model}")
    @MonitorTime
    public ResponseEntity<List<Rating>> getRatingsForModel(@PathVariable(value = "model") String model) {

        List<Rating> ratings = ratingService.getRatingsForModel(model);
        return ResponseEntity.ok(ratings);
    }

    @GetMapping("/{model}/average")
    public ResponseEntity<?> getAverageRating(@PathVariable(value = "model") String model) {
        Double average = ratingService.getAverageRatingForModel(model);
        System.out.println(average);
        return ResponseEntity.ok(average);
    }

    @PostMapping("")
    @MonitorTime
    public ResponseEntity<Rating> createRating(@Valid @RequestBody Rating rating) {

        Rating savedRating = ratingService.addRating(rating);
        return ResponseEntity.status(HttpStatus.CREATED).body(savedRating);
    }

    @PutMapping("/{id}")
    public ResponseEntity<Rating> updateRating(@PathVariable(value = "id") Long id,
                                               @Valid @RequestBody Rating newRating) throws ModelNotFoundException {
        Rating rating = ratingService.updateRating(id, newRating);
        return ResponseEntity.ok(rating);
    }
}
