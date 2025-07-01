from src.logger import get_logger
import sys
# logger = get_logger(__name__)
# logger.info("This is an info message")
# logger.warning("This is a warning message")
# logger.error("This is an error message")

from src.custom_exception import CustomException

logger = get_logger(__name__)
def divide(a, b):
    try:
        result = a / b
        logger.info(f"Division successful: {result}")
        return result
    except Exception as e:
        logger.error(f"Error occurred: {e}")
        raise CustomException("custom Division by zero is not allowed", sys)
    
if __name__ == "__main__":
    try:
        logger.info("Starting the division operation")
        divide(10, 10)
    except CustomException as ce:
        logger.error(f"Custom exception caught: {ce}")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")