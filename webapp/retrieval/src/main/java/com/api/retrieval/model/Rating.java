package com.api.retrieval.model;

import com.fasterxml.jackson.annotation.JsonProperty;

import javax.persistence.*;

import javax.persistence.GeneratedValue;
import javax.validation.constraints.Max;
import javax.validation.constraints.Min;
import javax.validation.constraints.NotBlank;
import javax.validation.constraints.NotNull;

@Entity
@Table(name = "ratings")
public class Rating {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    @Column(name = "score")
    @Min(value = 1)
    @Max(value = 10)
    @JsonProperty(required = true)
    @NotNull(message = "Score is mandatory")
    private Double score;
    @Column(name = "model")
    @NotBlank(message = "Model is mandatory")
    private String model;

    public Rating() {

    }

    public Rating(Double score, String model) {
        this.score = score;
        this.model = model;
    }

    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public Double getScore() {
        return score;
    }

    public void setScore(Double score) {
        this.score = score;
    }

    public String getModel() {
        return model;
    }

    public void setModel(String model) {
        this.model = model;
    }

    @Override
    public String toString() {
        return "Rating{" +
                "id=" + id +
                ", score=" + score +
                ", model='" + model + '\'' +
                '}';
    }
}
