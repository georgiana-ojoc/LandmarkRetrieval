package api.rating.controller;

import api.rating.aspect.annotations.MonitorTime;
import api.rating.exceptions.ModelNotFoundException;
import api.rating.model.domain.Rating;
import api.rating.model.dto.RatingDTO;
import api.rating.service.IRatingService;
import org.modelmapper.ModelMapper;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import javax.validation.Valid;
import java.util.List;
import java.util.stream.Collectors;

@RestController
@RequestMapping("/api/v1/ratings")
@Validated
@CrossOrigin
public class RatingController {

    @Autowired
    private IRatingService ratingService;

    @Autowired
    private ModelMapper modelMapper;

    @GetMapping()
    @MonitorTime
    public ResponseEntity<List<RatingDTO>> getAllRatings() {
        List<Rating> ratings = ratingService.getAllRatings();
        return ResponseEntity.ok(ratings.stream().map(rating -> modelMapper.map(rating, RatingDTO.class)).collect(Collectors.toList()));
    }

    @GetMapping("/{model}")
    @MonitorTime
    public ResponseEntity<List<RatingDTO>> getRatingsForModel(@PathVariable(value = "model") String model) {

        List<Rating> ratings = ratingService.getRatingsForModel(model);
        return ResponseEntity.ok(ratings.stream().map(rating -> modelMapper.map(rating, RatingDTO.class)).collect(Collectors.toList()));
    }

    @GetMapping("/{model}/average")
    public ResponseEntity<?> getAverageRating(@PathVariable(value = "model") String model) {
        Double average = ratingService.getAverageRatingForModel(model);
        return ResponseEntity.ok(average);
    }

    @PostMapping("")
    @MonitorTime
    public ResponseEntity<RatingDTO> createRating(@Valid @RequestBody Rating rating) {

        //extract variable
        Rating savedRating = ratingService.addRating(rating);
        return ResponseEntity.status(HttpStatus.CREATED).body((modelMapper.map(savedRating, RatingDTO.class)));
    }

    @PutMapping("/{id}")
    public ResponseEntity<RatingDTO> updateRating(@PathVariable(value = "id") Long id,
                                                  @Valid @RequestBody Rating newRating) throws ModelNotFoundException {
        Rating rating = ratingService.updateRating(id, newRating);
        return ResponseEntity.ok(modelMapper.map(rating, RatingDTO.class));
    }
}
