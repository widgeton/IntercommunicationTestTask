from .data import *
from .steps import *

DATATYPES = {
    'CarDetection': CarDetection,
}

STEPS = {
    'ImageHandler': ImageHandler,
    'MachineLearningModelRequest': MachineLearningModelRequest,
    'SaveCarDetection': SaveCarDetection,
}
