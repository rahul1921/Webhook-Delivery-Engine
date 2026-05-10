from fastapi import FastAPI, Request, HTTPException
import asyncio
import random

app = FastAPI()

# In-memory state
request_counter = 0


@app.post("/webhook")
async def receive_webhook(
    request: Request,
    fail_mode: str = "none"
):

    global request_counter
    request_counter += 1

    payload = await request.json()

    print("\n========================")
    print(f"Request Number: {request_counter}")
    print("Payload:")
    print(payload)

    print("Headers:")
    print(dict(request.headers))
    print("========================\n")

    # --------------------------------
    # MODE 1 -> ALWAYS SUCCESS
    # --------------------------------
    if fail_mode == "none":

        return {
            "status": "received"
        }

    # --------------------------------
    # MODE 2 -> ALWAYS FAIL
    # --------------------------------
    elif fail_mode == "always_fail":

        raise HTTPException(
            status_code=500,
            detail="Simulated server failure"
        )

    # --------------------------------
    # MODE 3 -> FAIL FIRST 3 TIMES
    # Useful for retry testing
    # --------------------------------
    elif fail_mode == "fail_first_3":

        if request_counter <= 3:

            raise HTTPException(
                status_code=500,
                detail=f"Failing attempt {request_counter}"
            )

        return {
            "status": "recovered"
        }

    # --------------------------------
    # MODE 4 -> RANDOM FAILURE
    # Useful for flaky network simulation
    # --------------------------------
    elif fail_mode == "random":

        if random.choice([True, False]):

            raise HTTPException(
                status_code=500,
                detail="Random failure"
            )

        return {
            "status": "random_success"
        }

    # --------------------------------
    # MODE 5 -> SLOW RESPONSE
    # Useful for timeout testing
    # --------------------------------
    elif fail_mode == "slow":

        await asyncio.sleep(10)

        return {
            "status": "slow_success"
        }

    # --------------------------------
    # DEFAULT
    # --------------------------------
    return {
        "status": "unknown_mode"
    }