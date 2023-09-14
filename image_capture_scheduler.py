import schedule
import time
from capture_image import capture_image

schedule.every(0.5).minutes.do(capture_image)
