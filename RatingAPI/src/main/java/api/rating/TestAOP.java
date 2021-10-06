package api.rating;

import api.rating.model.domain.Rating;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpMethod;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.client.RestTemplate;

import java.util.Arrays;
import java.util.HashMap;
import java.util.Map;

public class TestAOP {
    private static final String RATINGS_URL = "http://localhost:8080/api/v1/ratings";
    private static RestTemplate restTemplate = new RestTemplate();

    public static void main(String[] args) {
        TestAOP client = new TestAOP();

        client.createRating();
        client.getRatings();
        client.updateRating("1");

    }

    private void getRatings() {

        HttpHeaders headers = new HttpHeaders();
        headers.setAccept(Arrays.asList(MediaType.APPLICATION_JSON));
        HttpEntity<String> entity = new HttpEntity<String>("parameters", headers);

        ResponseEntity<String> result = restTemplate.exchange(RATINGS_URL, HttpMethod.GET, entity,
                String.class);

        System.out.println(result);
    }

    private void createRating() {

        Rating rating = new Rating(8.0, "ResNet");

        RestTemplate restTemplate = new RestTemplate();
        Rating result = restTemplate.postForObject(RATINGS_URL, rating, Rating.class);

        System.out.println(result);
    }

    private void updateRating(String id) {
        Map<String, String> params = new HashMap<String, String>();
        params.put("id", id);
        Rating rating = new Rating(6.0, "ResNet");
        RestTemplate restTemplate = new RestTemplate();
        restTemplate.put(RATINGS_URL + "/{id}", rating, params);
    }
}
