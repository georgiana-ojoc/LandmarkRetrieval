package com.api.retrieval.controller;

import com.api.retrieval.aspect.annotations.MonitorTime;
import com.api.retrieval.exceptions.ModelNotFoundException;
import com.api.retrieval.model.Rating;
import com.api.retrieval.service.RatingService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/v1/ratings")
public class RatingController {

    @Autowired
    private RatingService ratingService;

    @GetMapping()
    @MonitorTime
    public List<Rating> getAllRatings() {
        return ratingService.getAllRatings();
    }

    @GetMapping("/{model}")
    @MonitorTime
    public List<Rating> getRatingsForModel(String model) {
        return ratingService.getRatingsForModel(model);
    }

    @PostMapping()
    @MonitorTime
    public Rating createRating(@RequestBody Rating rating) {
        return ratingService.addRating(rating);
    }

    @PutMapping("/{id}")
    public ResponseEntity<Rating> updateRating(@PathVariable(value = "id") Long id,
                                               @RequestBody Rating newRating) throws ModelNotFoundException {
        Rating rating = ratingService.updateRating(id, newRating);
        return ResponseEntity.ok(rating);
    }
}
