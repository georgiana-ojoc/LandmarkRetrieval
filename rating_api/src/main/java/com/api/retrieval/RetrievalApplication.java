package com.api.retrieval;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.autoconfigure.domain.EntityScan;
import org.springframework.data.jpa.repository.config.EnableJpaRepositories;

@SpringBootApplication
@EnableJpaRepositories("com.api.retrieval.repository")
@EntityScan("com.api.retrieval.model")
public class RetrievalApplication {

	public static void main(String[] args) {
		SpringApplication.run(RetrievalApplication.class, args);
	}

}
