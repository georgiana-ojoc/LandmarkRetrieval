package api.rating.aspect;

import org.aspectj.lang.JoinPoint;
import org.aspectj.lang.annotation.After;
import org.aspectj.lang.annotation.AfterReturning;
import org.aspectj.lang.annotation.AfterThrowing;
import org.aspectj.lang.annotation.Aspect;
import org.aspectj.lang.annotation.Before;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Component;

import java.util.Arrays;


@Aspect
@Component
public class LoggingAspect {

    public final Logger log = LoggerFactory.getLogger(this.getClass());

    /**
     * Run before the method execution.
     */
    @Before("execution(* api.rating.service.RatingService.addRating(..))")
    public void logBeforeAddRating(JoinPoint joinPoint) {
        log.debug("Add rating was called...");
        log.debug("Before Called {}() -> {}", joinPoint.getSignature().getDeclaringTypeName(),
                joinPoint.getSignature().getName(), Arrays.toString(joinPoint.getArgs()));

    }

    /**
     * Run after the method returned a result.
     */
    @After("execution(* api.rating.service.RatingService.addRating(..))")
    public void logAfterAddRating(JoinPoint joinPoint) {
        log.debug("Add rating has finished...");
        log.debug("After called {}() -> {}", joinPoint.getSignature().getDeclaringTypeName(),
                joinPoint.getSignature().getName(), Arrays.toString(joinPoint.getArgs()));
    }

    @Before("execution(* api.rating.service.RatingService.updateRating(..))")
    public void logBeforeUpdateRating(JoinPoint joinPoint) {
        log.debug("Update rating was called...");
        log.debug("Before called {}() -> {}", joinPoint.getSignature().getDeclaringTypeName(),
                joinPoint.getSignature().getName(), Arrays.toString(joinPoint.getArgs()));

    }

    @After("execution(* api.rating.service.RatingService.updateRating(..))")
    public void logAfterUpdateRatingg(JoinPoint joinPoint) {
        log.debug("Update rating has finished...");
        log.debug("After for called {}() -> {}", joinPoint.getSignature().getDeclaringTypeName(),
                joinPoint.getSignature().getName(), Arrays.toString(joinPoint.getArgs()));
    }

    @AfterReturning(pointcut = "execution(* api.rating.service.RatingService.getAllRatings())", returning = "result")
    public void logAfterReturningAll(JoinPoint joinPoint, Object result) {
        log.debug("Get all ratings finished...");
        log.debug("Values returned..." + String.valueOf(result));
    }

    @AfterReturning(pointcut = "execution(* api.rating.service.RatingService.getRatingsForModel(..))", returning = "result")
    public void logAfterReturningForModel(JoinPoint joinPoint, Object result) {
        log.debug("Get ratings for given model...");
        log.debug("Values returned..." + String.valueOf(result));
    }

    @AfterThrowing(pointcut = "execution(* api.rating.service.RatingService.updateRating(..))", throwing = "error")
    public void logAfterUpdateThrowsException(JoinPoint joinPoint, Throwable error) {
        log.debug("Exception thrown in update rating...");
        log.error("Exception in {}.{}() with cause = {}", joinPoint.getSignature().getDeclaringTypeName(),
                joinPoint.getSignature().getName(), error.getCause() != null ? error.getCause() : "NULL");
    }
}