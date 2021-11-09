package com.api.retrieval.model;

import javax.persistence.*;

import javax.persistence.GeneratedValue;

@Entity
@Table(name = "ratings")
public class Rating {
    private long id;
    private int score;
    private String model;

    public Rating() {

    }

    public Rating(int score, String model) {
        this.score = score;
        this.model = model;
    }

    @Id
    @GeneratedValue(strategy = GenerationType.AUTO)
    public long getId() {
        return id;
    }

    public void setId(long id) {
        this.id = id;
    }

    @Column(name = "score", nullable = false)
    public int getScore() {
        return score;
    }

    public void setScore(int score) {
        this.score = score;
    }

    @Column(name = "model", nullable = false)
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
