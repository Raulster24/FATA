import time
import logging
from fastapi import Request
from common.messaging import publish_anomaly, publish_candidate_test
import common.update_consumer as uc  # Import entire module to reference updated variable

async def monitoring_middleware(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time

    logging.info(f"[Monitoring] {request.method} {request.url} processed in {process_time:.3f}s")
    
    # Use the dynamic threshold from update_consumer
    threshold = uc.current_threshold
    if process_time > threshold:
        anomaly_data = {
            "method": request.method,
            "url": str(request.url),
            "processing_time": process_time,
            "threshold": threshold
        }
        logging.warning(f"[Anomaly Detected] {anomaly_data}")
        publish_anomaly(anomaly_data)
        
        # For our candidate test, we simply use the anomaly data
        candidate_test_data = {
            "test_case": f"Verify {request.method} {request.url} under high load",
            "expected_response_time": process_time,
            "detected_threshold": threshold,
            "anomaly_data": anomaly_data
        }
        publish_candidate_test(candidate_test_data)
    
    return response
