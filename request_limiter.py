class RateLimitTracker():
    """
    Allows tracking rate limits for an API that uses the X-RateLimit-* headers

    The class is initialized with the headers from the first response, and then
    updated with the headers from each subsequent response.

    This is not suitable for multi-threaded or multi-process applications, as
    it does not adequately share state, nor account for mulitiple in flight
    requests.

    This is not suitable for APIs that use multiple rate limits.

    This is not suitable for APIs that use a different rate limiting mechanism to
    the X-RateLimit-* headers.

    Usage:
    ```
    rateLimiter = RateLimitTracker()
    while True:
        rateLimiter.delay()
        try:
            response = make_request()
        
        except e:
            raise e 
        
        finally:
            # Ensure the rate limiter is updated even if the request fails
            rateLimiter.update(response.headers)
    ```
    """
    # TODO: introduce a "with" mode that will automatically update the rate limiter
    #  when the block is exited. It will need to be request aware. It may need to be
    #  a context manager or HTTP agent.
    # TODO: Support for mutliple rate limits, e.g. X-RateLimit-Remaining-Search
    # TODO: Support for 


    def __init__(self, headers: dict = {}):
        self.requests_since_update = 0
        self.last_response_time = None
        self.reset_time = None
        self.limit = None
        self.remaining = None

        self.update(headers)

    def update(self, headers: dict):
        self.last_response_time = time.time()

        X_RateLimit_Remaining = headers.get('X-RateLimit-Remaining', None)
        if X_RateLimit_Remaining is not None:
            self.requests_since_update = 0
            self.remaining = int(X_RateLimit_Remaining)

        X_RateLimit_Limit = headers.get('X-RateLimit-Limit', None)
        if X_RateLimit_Limit is not None:
            self.limit = int(X_RateLimit_Limit)

        X_RateLimit_Reset = headers.get('X-RateLimit-Reset', None)
        if X_RateLimit_Reset is not None:
            self.reset_time = int(X_RateLimit_Reset)

    def __delay_until_reset(self):
        if self.reset_time is None:
            return

        delay = self.reset_time - time.time()
        if delay > 0:
            print(f"Rate limit reached. Waiting {delay} seconds")
            time.sleep(delay)
            self.remaining = None
            self.limit = None
            self.reset_time = None
            # Not strictly true
            self.requests_since_update = 0


    def delay(self):
        # If we don't know the remaining requests, we can't make a decision
        #  so we'll play safe and wait for 0.3 seconds
        # The way this is written we'll always end up waiting 0.3 seconds
        #  for the first request.
        if self.remaining == None:
            print("No rate limit information available. Waiting 0.3 seconds")
            time.sleep(0.3)
            return

        # If we have remaining requests, we can make a request
        if self.remaining - self.requests_since_update > 0:
            self.requests_since_update += 1
        else:
            self.__delay_until_reset()


    def status(self):
        remaining = self.remaining
        if remaining is None:
            remaining = "Unknown"
        
        limit = self.limit
        if limit is None:
            limit = "Unknown"

        reset_time = self.reset_time
        seconds_until_reset = "Unknown"
        if reset_time is not None:
            seconds_until_reset = reset_time - time.time()
        
        return f"{remaining}/{limit} requests remaining. Resets in {seconds_until_reset} seconds"


dictionaryapi_rate_limit = RateLimitTracker()